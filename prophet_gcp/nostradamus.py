from fbprophet import Prophet
import dask.dataframe as dd
import pandas as pd


def run_prophet(timeseries, date_column="ds", y_column="y", index_column=None, type_=None, start_date=None,
                end_date=None, prophet_obj_kwds={}, predict_kwds={}, fit_kwds={}):
    """ Run prophet in a given timeserie 
        Arguments:
            timeseries: pd.Dataframe with the timeserie
            date_column: string with the name of the date column on the dataset
            y: name of the target variable
        Returns:
            Dataframe: pandas.Dataframe with the forecast result
    """
    assert index_column is not None, "Must indicate an index_column"
    assert type_ is not None, "Must specify baseline or forecast"

    timeseries.rename(columns={date_column: 'ds', y_column: 'y'}, inplace=True)
    idx = timeseries[index_column].unique()

    if type_ == "baseline":
        min_date, max_date = timeseries.ds.min(), timeseries.ds.max()
    elif type_ == "forecast":
        min_date, max_date = start_date, end_date
    else:
        raise Exception("--type must be baseline or forecast")
    
    time_index = _create_index_timeserie(min_date, max_date)
    model = Prophet(yearly_seasonality=True, **prophet_obj_kwds)
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    model.fit(timeseries, verbose=False)
    forecast = model.predict(time_index, **predict_kwds)
    forecast['index_column'] = idx[0]

    return forecast


def _create_index_timeserie(min_date, max_date):
    time_index = pd.date_range(min_date, max_date)
    dates = (pd.DataFrame({'ds': pd.to_datetime(time_index.values)},
                          index=range(len(time_index))))
    return dates