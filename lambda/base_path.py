import json


def handler(event, context):
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Allows access from any origin
            "Access-Control-Allow-Credentials": True  # Needed for cookies, authorization headers with HTTPS
        },
        "body": json.dumps({"message": "Hello from my API"}),
    }
    return response
