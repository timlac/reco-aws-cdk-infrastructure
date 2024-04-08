import os

from utils import generate_response
from constants import TABLE_NAME_KEY, TEMPLATE_TYPE_KEY
from templates.template_repository import TemplateRepository


def handler(event, context):
    template_type = event['pathParameters'][TEMPLATE_TYPE_KEY]
    template_repo = TemplateRepository(os.environ[TABLE_NAME_KEY])

    try:
        response_items = template_repo.get_templates(
            template_type,
        )

        print("Data queried successfully: {}".format(response_items))
        return generate_response(200, body=response_items)

    except Exception as e:
        print("Error querying data: {}".format(str(e)))
        return generate_response(500, body="Error querying data {}".format(str(e)))
