### Running multiple timeseries forcasting with Facebook Prophet

This package allows you to run timeseries forecasting in parallel using [Facebook Prophet](https://research.fb.com/prophet-forecasting-at-scale/) in Google Machine Learning Engine or your local computer.

##### Usage

The input csv file must look like this:

y | date | id
--- | --- | ---
25| 2018-04-24 | A
11|2018-04-18|A
7|2017-02-02|A
27|2017-03-19|B
7|2017-04-18|B
10|2017-04-01|B

Where:

+ `y` is the target value
+ `date` date
+ `id` identifier of the timeserie

If you want to use other column names, you must specify them when launching the command.


##### Running local

```
python main.py --local_file yes --input_file "../../sample.csv" \
               --index_column "product_uid" \
               --date_column "date" --y_column "q_total" \
               --output_name "../../output.csv" --type "baseline" 
```


The output file contains the results of Facebook Prophet Forecasting




##### Running on Google Machine Learning Engine

```
gcloud ml-engine jobs submit training JOB_NAME \
        --module-name=prophet_gcp.main \
        --package-path prophet_gcp/ \
        --region=us-east1 \
        --staging-bucket=gs://your-stagin-bucket/ \
        --scale-tier=BASIC \
        --runtime-version=1.9 \
        -- \
        --input_file gs://path/to/input_file.csv \
        --output_file gs://path/to/output_file/ \
        --index_column id \
        --date_column date \
        --y_column y \
        --type baseline \
        --y_column y \
        --output_name prediction_results.csv \
        --start_date "yyy-MM-dd" \ #only if type is forecast
        --end_date "yyy-MM-dd" \ #only if type is forecast
```

The output file contains the results of Facebook Prophet Forecasting, they are stored in Google Cloud Storage, the aggregated time series are stored in GCS too with  `dill`. 

##### Using a config file por Prophet

You can optionally pass a configuration file, for both the local and google machine learning version.
We provide an example config file called `config_example.json`.


```
python main.py --local_file yes --input_file "../../sample.csv" \
               --index_column "product_uid" \
               --date_column "date" --y_column "q_total" \
               --output_name "../../output.csv" --type "baseline \
               --prophet_options config_example.json" 
```

The config file needs to have three keys, though they can be left blank:

+ `prophet_obj_kwds`: passed as `Prophet(yearly_seasonality=True, **prophet_obj_kwds)`
+ `predict_kwds`: passed as `model.fit(timeseries, **fit_kwds)`
+ `fit_kwds`: passed as `model.predict(time_index, **predict_kwds)`

##### List of arguments for main.py

Argument name | description | optional
--- | --- | ---
input_file | Path to the GCS or local file | No
output_path | Path to the GCS output file | Yes, only needed if using GCS version
index_column |index column | No
date_column | date column name| No
y_column | y column | No
output_name | output csv file name | No
type | baseline or forecast | No
prophet_options | file name with prophet options | Yes
output_name | output csv file name | No
start_date |forecast start date| Only needed if type forecast is specified
end_date|forecast end date| Only needed if type forecast is specified
local_file | Local file: yes or no | Yes




