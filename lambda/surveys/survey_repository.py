import boto3
from boto3.dynamodb.conditions import Key
import datetime
from zoneinfo import ZoneInfo

from utils import generate_id

from surveys.survey_item_handler import initialize_survey_item
from surveys.filename_sampling.sample_filenames import sample_filenames


class SurveyRepository:
    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)

    def create_survey(self, project_name, data):

        survey_id = generate_id()

        # Convert the list of items into the DynamoDB L type
        survey_items_with_attributes = [initialize_survey_item(survey_item) for survey_item in data.get("survey_items")]

        print("creating current date")
        current_date = str(datetime.datetime.now(ZoneInfo("Europe/Berlin")).isoformat())

        print("current date: " + current_date)

        # Insert data into the DynamoDB table
        self.table.put_item(
            Item={
                "project_name": project_name,
                "survey_id": survey_id,
                "created_at": current_date,

                "survey_items": survey_items_with_attributes,
                "user_id": data.get("user_id"),
                "emotion_alternatives": data.get("emotion_alternatives"),
                "valence": data.get("valence"),
                "date_of_birth": str(data.get("date_of_birth")),
                "sex": data.get("sex"),
            },
            ConditionExpression="attribute_not_exists(id)",  # Check if 'id' does not already exist
        )
        return survey_id

    def get_survey(self, project_name, survey_id):
        response = self.table.get_item(
            Key={
                "project_name": project_name,
                'survey_id': survey_id
            }
        )
        return response.get('Item')

    def get_surveys(self, project_name):
        response = self.table.query(
            KeyConditionExpression=Key('project_name').eq(project_name)
        )
        return response.get('Items', [])

    def update_survey(self, project_name, survey_id,
                      update_idx, reply):
        """
        :param project_name: partition key to locate survey
        :param survey_id: sort key to locate survey
        :param update_idx: the survey_items index to update
        :param reply: reply value, e.g. emotion id or scale values
        :return:
        """
        self.table.update_item(
            Key={
                'project_name': project_name,
                'survey_id': survey_id
            },
            UpdateExpression=f'SET survey_items[{update_idx}].reply = :val, '
                             f'survey_items[{update_idx}].has_reply = :hasReplyVal',
            ExpressionAttributeValues={
                ':val': reply,
                ':hasReplyVal': 1
            }
        )
