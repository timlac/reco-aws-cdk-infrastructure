import boto3
from constants import survey_types
from utils import get_metadata

class ProjectRepository:
    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)

    def get_project(self, project_name):
        # Your code to fetch a survey
        response = self.table.get_item(
            Key={
                'project_name': project_name
            }
        )
        item = response.get("Item")

        s3_files_with_meta = {}
        s3_files = item['s3_objects']

        for filename in s3_files:
            meta = get_metadata(filename)
            s3_files_with_meta[filename] = meta
        item["s3_objects_with_meta"] = s3_files_with_meta

        return response.get('Item')

    def create_project(self, data):
        project_name = data.get('project_name')

        survey_type = data.get('survey_type')

        if survey_type not in survey_types:
            raise Exception("Invalid survey type")

        # Insert data into the DynamoDB table
        self.table.put_item(
            Item={
                "project_name": project_name,
                "survey_type": survey_type,
                "s3_objects": data.get("s3_objects"),
                "s3_folder": data.get('s3_folder'),
                "emotions_per_survey": int(data.get('emotions_per_survey')),
                "samples_per_survey": int(data.get('samples_per_survey')),
                "reply_meta": data.get('reply_meta')
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
