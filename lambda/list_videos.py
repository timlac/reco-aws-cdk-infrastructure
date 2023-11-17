import os
import boto3
import json
from aws_lambda_powertools import Logger

logger = Logger()


def lambda_handler(event, context):
    logger.info("initiating client")

    s3_client = boto3.client('s3')
    bucket_name = os.environ['BUCKET_NAME']

    logger.info("done, now starting data collection")

    def list_objects(bucket, continuation_token=None):
        if continuation_token:
            resp = s3_client.list_objects_v2(Bucket=bucket, ContinuationToken=continuation_token)
        else:
            resp = s3_client.list_objects_v2(Bucket=bucket)
        return resp

    keys = []
    token = None
    while True:
        response = list_objects(bucket_name, token)
        keys.extend([obj['Key'] for obj in response.get('Contents', [])])

        logger.info("collected batch of data")

        # Check if more objects are available
        if response.get('IsTruncated'):
            token = response.get('NextContinuationToken')
        else:
            break

    logger.info("returning")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Allows access from any origin
            'Access-Control-Allow-Credentials': True  # Needed for cookies, authorization headers with HTTPS
        },
        'body': json.dumps(keys)
    }
