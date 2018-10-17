### Running multiple timeseries forcasting with Facebook Prophet

This package allows to run multiple timeseries forecasting using [Facebook Prophet](https://research.fb.com/prophet-forecasting-at-scale/) in Google Machine Learning Engine or your local computer.

##### Usage
You must provide the input csv file like this:

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

Your input could have other column names, but you must specify them when launching the command.

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

The output file are the results of Facebook Prophet Forecasting, they are stored in Google Cloud Storage, the aggregated time series are stored in GCS too with  `dill`. 