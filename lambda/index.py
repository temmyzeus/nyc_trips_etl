import json

def lambda_handler(event, context):
    # TODO implement

    print("Event:", event, end="\n\n")
    print("Context:", context)
    
    return {
        'statusCode': 200,
        'body': "Great"
    }
