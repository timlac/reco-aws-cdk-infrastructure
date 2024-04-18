import boto3

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
