import boto3
from boto3.dynamodb.conditions import Key


class TemplateRepository:

    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)

    def get_template(self, template_type, template_name):
        response = self.table.get_item(
            Key={
                'template_type': template_type,
                "template_name": template_name
            }
        )
        data = response.get('Item')
        return data

    def get_templates(self, template_type):
        response = self.table.query(
            KeyConditionExpression=Key('template_type').eq(template_type)
        )
        data = response.get('Items', [])
        return data

    def create_template(self, template_model):
        # Insert data into the DynamoDB table
        self.table.put_item(
            Item=template_model.dict(),
            ConditionExpression="attribute_not_exists(template_name)"
        )
        return template_model

    def update_template(self):
        pass
