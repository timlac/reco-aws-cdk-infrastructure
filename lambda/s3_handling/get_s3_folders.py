import os
from utils import generate_response
from s3_handling.folder_handler import create_folder_dict, add_metadata
from s3_handling.list_bucket_contents import list_all_bucket_contents


def handler(event, context):
    bucket_name = os.environ['S3_BUCKET_NAME']

    try:
        all_objects = list_all_bucket_contents(bucket_name)

        folder_dict = create_folder_dict(all_objects)
        add_metadata(folder_dict)

        return generate_response(200, folder_dict)

    except Exception as e:
        print(f"Error: {str(e)}")
        return generate_response(500, f"Error: {str(e)}")
