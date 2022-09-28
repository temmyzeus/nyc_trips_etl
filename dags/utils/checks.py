from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def check_s3_bucket_exists(bucket_name:str) -> None:
    s3_hook = S3Hook("aws_conn")
    s3_hook.get_bucket()
