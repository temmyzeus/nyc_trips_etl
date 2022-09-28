import os
from datetime import datetime

from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.lambda_function import LambdaHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.lambda_function import \
    AwsLambdaInvokeFunctionOperator

LAMBDA_FUNCTION_NAME:str = os.getenv("nyc_lambda")

@dag(
    dag_id="NYC-Trips",
    description="Ingesting trips data from NYC City Website",
    start_date=datetime(2022, 1, 1),
    schedule_interval="@monthly",
    catchup=False
)
def dag():
    @task
    def check_lambda_functions_exists(function_name:str) -> None:
        lambda_hook = LambdaHook()
        lambda_conn = lambda_hook.get_conn()

    # download_to_s3 = AwsLambdaInvokeFunctionOperator(
    #     function_name=,
    # )

    # check_lambda_exists    \
    #                           Downloaad data to S3
    # check_s3_buclet_exists /
    check_lambda_functions_exists()

dag()
