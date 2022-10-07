import json
import os
from datetime import datetime, date
from typing import Union

from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.lambda_function import LambdaHook
from airflow.providers.amazon.aws.operators.lambda_function import \
    AwsLambdaInvokeFunctionOperator

from utils import checks

LAMBDA_FUNCTION_NAME:str = os.getenv("NYC_LAMBDA")
BUCKET_NAME:str = os.getenv("S3_BUCKET_NAME")

date_month_type = Union[int, str]

def create_download_url(ti, year: date_month_type, month: date_month_type) -> None:
    """
    Create data download link based on date and availability of the data and save as xcoms.

    Yellow Trips records: Jan 2009 - till
    Green Trips records: August 2013 - till
    For-Hire Vehicle Trip Records: January 2015 - till
    High Volume For-Hire Vehicle Trip Records: February 2019 - till
    """

    if isinstance(year, str):
        year = int(year)

    if isinstance(month, str):
        month = int(month)

    run_interval_date:date = date(year, month, 1)

    ti.xcom_push(
        key="yellow_trips_url", 
        value="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{}-{:02d}.parquet".format(year, month)
        )

    if run_interval_date > date(2013, 8, 1):
        ti.xcom_push(
            key="green_trips_url",
            value="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{}-{:02d}.parquet".format(year, month)
        )
        print("Green Trips now Available")

    if run_interval_date > date(2015, 1, 1):
        ti.xcom_push(
            key="fhv_trips_url",
            value="https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_{}-{:02d}.parquet".format(year, month)
        )
        print("For-Hire Vehicle now available")

    if run_interval_date > date(2019, 2, 1):
        ti.xcom_push(
            key="high_volume_fhv_url",
            value="https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_{}-{:02d}.parquet".format(year, month)
        )
        print("High Volume For-Hire Vehicle Trip available")

@dag(
    dag_id="NYC-Trips",
    description="Ingesting trips data from NYC City Website",
    start_date=datetime(2009, 1, 1),
    schedule_interval="@monthly",
    catchup=False
)
def dag():

    # @task
    # def check_lambda_functions_exists(function_name:str = "nyc_lambda_function") -> None:
    #     lambda_hook = LambdaHook()
    #     lambda_conn = lambda_hook.get_conn()

    check_s3_bucket_exists = PythonOperator(
        task_id="check_s3_bucket_exists",
        python_callable=checks.check_s3_bucket_exists,
        op_kwargs={
            "bucket_name": BUCKET_NAME
        }
    )

    check_lambda_exists = PythonOperator(
        task_id="check_lambda_exists",
        python_callable=checks.check_lambda_exists,
        op_kwargs={"function_name": LAMBDA_FUNCTION_NAME}
    )

    create_download_links = PythonOperator(
        task_id="create_download_links",
        python_callable=create_download_url,
        op_kwargs={
            "year": "{{ dag_run.logical_date.year }}",
            "month": "{{ dag_run.logical_date.month }}",
        }
    )

    fetch_data_to_s3_with_lambda = AwsLambdaInvokeFunctionOperator(
        task_id="fetch_data_to_s3_with_lambda",
        function_name=LAMBDA_FUNCTION_NAME,
        aws_conn_id="aws_conn",
        payload=json.dumps({
            "msg": "hello world"
        })
    )

    [check_s3_bucket_exists, check_lambda_exists] >> create_download_links >> fetch_data_to_s3_with_lambda

dag()
