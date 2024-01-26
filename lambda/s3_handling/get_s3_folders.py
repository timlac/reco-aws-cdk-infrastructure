import boto3
import os
from utils import generate_response
from s3_handling.folder_handler import create_folder_dict

s3 = boto3.client('s3')


def list_all_bucket_contents(bucket_name):
    continuation_token = None

    all_objects = []

    while True:
        params = {
            'Bucket': bucket_name
        }
        if continuation_token:
            params['ContinuationToken'] = continuation_token

        response = s3.list_objects_v2(**params)
        continuation_token = response.get('NextContinuationToken')

        all_objects.extend(response.get('Contents', []))

        # If there are no more results, break the loop
        if not continuation_token:
            break

    return all_objects


def handler(event, context):
    bucket_name = os.environ['S3_BUCKET_NAME']

    try:
        all_objects = list_all_bucket_contents(bucket_name)

        folder_dict = create_folder_dict(all_objects)

        for folder_name in folder_dict.keys():
            folder_dict[folder_name]['emotion_ids'] = list(folder_dict[folder_name]['emotion_ids'])

        return generate_response(200, folder_dict)

    except Exception as e:
        print(f"Error: {str(e)}")
        return generate_response(500, f"Error: {str(e)}")
