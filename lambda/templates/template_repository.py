import boto3


class TemplateRepository:

    def __init__(self, table_name):
        self.table = boto3.resource('dynamodb').Table(table_name)

    def get_template(self, template_id, template_type):
        response = self.table.get_item(
            Key={
                "template_id": template_id,
                'template_type': template_type
            }
        )
        data = response.get('Item')
        return data.dict()

    def get_templates(self):
        pass

    def create_template(self, template_model):
        # Insert data into the DynamoDB table
        self.table.put_item(
            Item=template_model.dict(),
            ConditionExpression="attribute_not_exists(id)",  # Check if 'id' does not already exist
        )
        return template_model

    def update_template(self):
        pass
