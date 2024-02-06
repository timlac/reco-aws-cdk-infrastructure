import boto3
from utils import get_metadata


class ProjectRepository:
    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)


    def get_project(self, project_name, generate_meta=True):
        response = self.table.get_item(
            Key={
                'project_name': project_name
            }
        )
        item = response.get("Item")

        if generate_meta:
            s3_files_with_meta = {}
            s3_files = item.get('s3_experiment_objects') + item.get('s3_intro_objects')

            for filename in s3_files:
                meta = get_metadata(filename)
                s3_files_with_meta[filename] = meta
            item["s3_objects_with_meta"] = s3_files_with_meta

        return response.get('Item')

    def create_project(self, data):
        project_name = data.get('project_name')

        # Insert data into the DynamoDB table
        self.table.put_item(
            Item={
                "project_name": project_name,
                "s3_experiment_objects": data.get("s3_experiment_objects"),
                "s3_intro_objects": data.get("s3_intro_objects"),
                "s3_folder": data.get('s3_folder'),
                "emotion_sampling_enabled": data.get('emotion_sampling_enabled'),
                "emotions_per_survey": int(data.get('emotions_per_survey', 0)),
                "samples_per_survey": int(data.get('samples_per_survey', 0)),
                "reply_format": data.get('reply_format'),
                "instructions": data.get('instructions')
            },
            ConditionExpression="attribute_not_exists(project_name)"
        )
        return project_name

    def get_projects(self):
        response = self.table.scan()

        items = response['Items']

        while 'LastEvaluatedKey' in response:
            response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])

        return items
