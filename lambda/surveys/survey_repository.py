import boto3
from boto3.dynamodb.conditions import Key
import datetime
from zoneinfo import ZoneInfo

from utils import generate_id
from constants import survey_types

from surveys.survey_item_handler import initialize_survey_item


class SurveyRepository:
    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)

    def create_survey(self, project_name, data):
        # Validate survey type
        survey_type = data.get("survey_type")
        if survey_type not in survey_types:
            raise Exception("Invalid response type")

        survey_id = generate_id()

        # Convert the list of items into the DynamoDB L type
        survey_items_with_attributes = [initialize_survey_item(survey_item) for survey_item in data.get("survey_items")]

        current_date = str(datetime.datetime.now(ZoneInfo("Europe/Berlin")).isoformat())

        # Insert data into the DynamoDB table
        self.table.put_item(
            Item={
                "survey_type": survey_type,
                "project_name": project_name,
                "survey_id": survey_id,
                "survey_items": survey_items_with_attributes,
                "created_at": current_date,
                "user_id": data.get("user_id"),
                "emotion_alternatives": data.get("emotion_alternatives"),
                "valence": data.get("valence"),
                "date_of_birth": str(data.get("date_of_birth")),
                "sex": data.get("sex"),
                "reply_format": data.get("reply_format")
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
