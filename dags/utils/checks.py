from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def check_s3_bucket_exists(bucket_name:str) -> None:
    print("TRYing to CONNECT FFS")
    s3_hook = S3Hook("aws_conn")
    # s3_hook.get_bucket()

def check_lambda_exists(function_name:str) -> None:
    pass
