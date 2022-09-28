import os
from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.lambda_function import LambdaHook
from airflow.providers.amazon.aws.operators.lambda_function import \
    AwsLambdaInvokeFunctionOperator

from utils.checks import check_s3_bucket_exists

LAMBDA_FUNCTION_NAME:str = os.getenv("NYC_LAMBDA")
BUCKET_NAME:str = os.getenv("NYC_BUCKET_NAME")

@dag(
    dag_id="NYC-Trips",
    description="Ingesting trips data from NYC City Website",
    start_date=datetime(2022, 1, 1),
    schedule_interval="@monthly",
    catchup=False
)
def dag():

    # @task
    # def check_lambda_functions_exists(function_name:str = "nyc_lambda_function") -> None:
    #     lambda_hook = LambdaHook()
    #     lambda_conn = lambda_hook.get_conn()

    check_s3_bucket_exists = PythonOperator(
        python_callable=check_s3_bucket_exists,
        op_kwargs={
            "bucket_name": BUCKET_NAME
        }
    )

    # download_to_s3 = AwsLambdaInvokeFunctionOperator(
    #     function_name=,
    # )

    # check_lambda_exists    \
    #                           Downloaad data to S3
    # check_s3_buclet_exists /
    # check_lambda_functions_exists

    check_s3_bucket_exists

dag()
