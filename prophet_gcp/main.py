import argparse
import pandas as pd
from utils import load_parse_file, get_frames_by_id, write_results
from ml_engine_utils import download_file_from_storage, save_in_gcs
from multiprocessing import Pool
from nostradamus import run_prophet
from multiprocessing import Pool, cpu_count
from functools import partial
import time

def run(args):

    start = time.time()
    file_path = download_file_from_storage(args.input_file)
    index = args.index_column
    date_column = args.date_column
    y_column=args.y_column

    data = load_parse_file(file_path=file_path)
    dataframes = get_frames_by_id(dataframe=data, index_col=index)
    p = Pool(cpu_count())
    partial_func = partial(run_prophet,
                            date_column=date_column, 
                            y_column=y_column,
                            index_column=index,
                            type_=args.type,
                            start_date=args.start_date,
                            end_date=args.end_date)

    predictions = p.map(partial_func, dataframes)
    results_path = write_results(predictions,file_name=args.output_name)
    save_in_gcs(results_path, args.output_path)
    print("Done in {0} minutes".format(   (time.time() - start)/60 ))
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, help="Path to the GCS file")
    parser.add_argument('--output_path', type=str, help="Path to the GCS output file")
    parser.add_argument('--index_column', type=str, help="index column")
    parser.add_argument('--date_column', type=str, help="date column name")
    parser.add_argument('--y_column', type=str, help="y column")
    parser.add_argument('--output_name', type=str, help="output csv file name")
    parser.add_argument('--type', type=str, help="baseline or forecast")
    parser.add_argument('--start_date', type=str, help="forecast start date", default=None)
    parser.add_argument('--end_date', type=str, help="baseline or forecast", default=None)
    args = parser.parse_args()
    run(args)