import json

import boto3
import requests

def lambda_handler(event, context):
    # TODO implement

    # s3 = boto3.client("s3")

    print("Event:", event)
    print("Context:", context)
    # url = ...
    # save_as = ...
    # print("Starting file download")
    # response = requests.get(url=url)
    # print("File downloaded")

    # if response.status_code == 200:
    #     print("Saving file to Disk")
    #     with open(save_as, mode="w") as f:
    #         f.write(response.content)
    #         print("File %s downloaded succesfully via URL: %s" % (save_as, url))
    #     print("File saved to disk")

    return {
        'statusCode': response.status_code
    }
