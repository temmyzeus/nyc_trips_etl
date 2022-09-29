from airflow.providers.amazon.aws.hooks.s3 import S3Hook

class BucketNotFoundError(Exception):
    """Exeption class for Bucket not found"""
    pass

def check_s3_bucket_exists(bucket_name:str) -> None:
    """Check if an S3 Bucket of specified name, exists in the account provided"""
    print("Trying to CONNECT FFS")
    s3_hook = S3Hook("aws_conn")
    print(s3_hook.extra_args)
    does_bucket_exist = s3_hook.check_for_bucket(bucket_name)
    if not does_bucket_exist:
        raise BucketNotFoundError("Bucket name: %s not found" % bucket_name)

def check_lambda_exists(function_name:str) -> None:
    pass
