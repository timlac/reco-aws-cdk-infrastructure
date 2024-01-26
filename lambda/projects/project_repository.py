import boto3
from constants import survey_types


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
                "s3_data_folder": data.get('s3_data_folder'),
                "reply_meta": data.get('reply_meta')
            },
            ConditionExpression="attribute_not_exists(project_name)"
        )
        return project_name
