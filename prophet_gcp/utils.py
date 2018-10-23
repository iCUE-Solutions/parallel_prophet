import pandas as pd
from tqdm import tqdm

def load_parse_file(file_path, date_column="date"):
    """Loads a file into Pandas dataframe, and parse the datetime columns
        Arguments:
            file_path: string path to the input file.
        Returns:
            Dataframe: dask.dataframe from the file
    """
    data = pd.read_csv(file_path)
    data[date_column] =  pd.to_datetime(data[date_column], format='%Y-%m-%d')
    return data


def get_frames_by_id(dataframe, index_col=None):
    """Group by the dataframe by index
        Arguments:
            dataframe: dask.dataframe.
            index_col: string with the index_col to order
        Returns:
            list: list of dask.dataframe with the data filtered
    """
    assert index_col != None, "Must specify and index column"
    indexs_vals = dataframe[index_col].unique()
    dfs = []
    print("INFO: Spliting the dataframes...")
    pbar = tqdm(total=len(indexs_vals))
    for index in indexs_vals:
        pbar.update(1)
        d = dataframe[(dataframe[index_col] == index)]
        dfs.append(d)
    return dfs


def write_results(dataframes=None, file_name=None):
    """Group by the dataframe by index
        Arguments:
            dataframes: pandas.dataframe.
        Returns:
            string: path to the output file
    """
    file_name = "output.csv" if file_name == None else file_name
    dataframe_ = pd.concat(dataframes, axis=0, copy=False, sort=False)
    dataframe_.to_csv(file_name)
    return file_name