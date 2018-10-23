import argparse
import pandas as pd
from utils import load_parse_file, get_frames_by_id, write_results
from ml_engine_utils import download_file_from_storage, save_in_gcs
from multiprocessing import Pool
from nostradamus import run_prophet
from multiprocessing import Pool, cpu_count
from functools import partial
import time
import dill
import json


def run(args):

    start = time.time()
    if args.local_file is not None:
        file_path = download_file_from_storage(args.input_file)
    else:
        file_path = args.input_file

    index = args.index_column
    date_column = args.date_column
    y_column = args.y_column

    data = load_parse_file(file_path=file_path)
    dataframes = get_frames_by_id(dataframe=data, index_col=index)

    #save dataframes on google cloud storage 
    with open("dataframes.dill", "wb") as dill_file:
        dill.dump(dataframes, dill_file)
    dill_file.close()
    if args.local_file is not None:
        pass
    else:
        save_in_gcs("dataframes.dill", args.output_path)

    prophet_config_file_name = args.prophet_options
    if prophet_config_file_name is not None:
        with open('config_example.json', 'r') as f:
            config = json.load(f)
    else:
        config = {'prophet_obj_kwds': {}, 'predict_kwds': {}, 'fit_kwds': {}}

    p = Pool(cpu_count())
    partial_func = partial(run_prophet,
                           date_column=date_column,
                           y_column=y_column,
                           index_column=index,
                           type_=args.type,
                           start_date=args.start_date,
                           end_date=args.end_date,
                           prophet_obj_kwds=config['prophet_obj_kwds'],
                           predict_kwds=config['predict_kwds'],
                           fit_kwds=config['fit_kwds'])

    predictions = p.map(partial_func, dataframes)
    results_path = write_results(predictions, file_name=args.output_name)
    if args.local_file is not None:
        pass
    else:
        save_in_gcs(results_path, args.output_path)
    print("Done in {0} minutes".format((time.time() - start)/60))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, help="Path to the GCS file")
    parser.add_argument('--output_path', type=str, help="Path to the GCS output file", default=None)
    parser.add_argument('--index_column', type=str, help="index column")
    parser.add_argument('--date_column', type=str, help="date column name")
    parser.add_argument('--y_column', type=str, help="y column")
    parser.add_argument('--output_name', type=str, help="output csv file name")
    parser.add_argument('--type', type=str, help="baseline or forecast")
    parser.add_argument('--prophet_options', type=str, help="file name with prophet options", default=None)
    parser.add_argument('--start_date', type=str, help="forecast start date", default=None)
    parser.add_argument('--end_date', type=str, help="baseline or forecast", default=None)
    parser.add_argument('--local_file', type=str, help="Local file: yes or no", default=None)
    myargs = parser.parse_args()
    run(myargs)
