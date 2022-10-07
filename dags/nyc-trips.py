import os
from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.lambda_function import LambdaHook
from airflow.providers.amazon.aws.operators.lambda_function import \
    AwsLambdaInvokeFunctionOperator

from utils import checks

LAMBDA_FUNCTION_NAME:str = os.getenv("NYC_LAMBDA")
BUCKET_NAME:str = os.getenv("S3_BUCKET_NAME")

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

    fetch_data_to_s3_with_lambda = DummyOperator(
        task_id="fetch_data_to_s3_with_lambda"
    )

    # download_to_s3 = AwsLambdaInvokeFunctionOperator(
    #     function_name=,
    # )

    # check_lambda_exists    \
    #                           Downloaad data to S3
    # check_s3_buclet_exists /
    # check_lambda_functions_exists

    [check_s3_bucket_exists, check_lambda_exists] >> fetch_data_to_s3_with_lambda

dag()
