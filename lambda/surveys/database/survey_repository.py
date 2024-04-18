import boto3
from boto3.dynamodb.conditions import Key

from surveys.database.survey_model import SurveyModel
from utils import get_metadata


def generate_meta_for_survey(survey: SurveyModel):
    for survey_item in survey.survey_items:
        metadata = get_metadata(survey_item.filename)
        survey_item.metadata = metadata


class SurveyRepository:

    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)

    def create_survey(self, survey_model):

        # Insert data into the DynamoDB table
        self.table.put_item(
            Item=survey_model.dict(),
            ConditionExpression="attribute_not_exists(survey_id)",  # Assert that 'survey_id' does not already exist
            # TODO: write a test to make sure this works properly
        )
        return survey_model

    def get_survey(self, project_name, survey_id, generate_meta=True):
        response = self.table.get_item(
            Key={
                "project_name": project_name,
                'survey_id': survey_id
            }
        )
        data = response.get('Item')
        if data is not None:
            survey_model = SurveyModel(**data)
            if generate_meta:
                generate_meta_for_survey(survey_model)
            return survey_model.dict()
        else:
            return None

    def get_surveys(self, project_name, generate_meta=True):
        response = self.table.query(
            KeyConditionExpression=Key('project_name').eq(project_name)
        )
        data = response.get('Items', [])
        if data:
            surveys = []
            for d in data:
                survey_model = SurveyModel(**d)
                if generate_meta:
                    generate_meta_for_survey(survey_model)
                surveys.append(survey_model.dict())
            return surveys
        else:
            return data

    def update_survey(self, project_name, survey_id,
                      update_idx, reply, time_spent_on_item):
        """
        :param project_name: partition key to locate survey
        :param survey_id: sort key to locate survey
        :param update_idx: the survey_items index to update
        :param reply: reply value, e.g. emotion id or scale values
        :param time_spent_on_item: time spent on survey item
        :return:
        """
        self.table.update_item(
            Key={
                'project_name': project_name,
                'survey_id': survey_id
            },
            UpdateExpression=f'SET survey_items[{update_idx}].reply = :val, '
                             f'survey_items[{update_idx}].has_reply = :hasReplyVal, '
                             f'survey_items[{update_idx}].time_spent_on_item = :timeSpent',
            ExpressionAttributeValues={
                ':val': reply,
                ':hasReplyVal': 1,
                ':timeSpent': time_spent_on_item
            }
        )
