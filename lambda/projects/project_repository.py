import boto3
from utils import get_metadata
from pydantic import ValidationError

from projects.project_model import ProjectModel


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
        try:
            # Parse and validate input data using the Project model
            project = ProjectModel(**data)
        except ValidationError as e:
            # Handle validation errors, for example, by logging or raising an error
            print(f"Validation Error: {e}")
            raise

        # Insert validated and parsed data into the DynamoDB table
        self.table.put_item(
            Item=project.dict(),  # Convert Pydantic model to dictionary
            ConditionExpression="attribute_not_exists(project_name)"
        )

        return project.project_name

    def get_projects(self):
        response = self.table.scan()

        items = response['Items']

        while 'LastEvaluatedKey' in response:
            response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])

        return items
