import os
import json

from utils import generate_response
from constants import TABLE_NAME_KEY
from templates.template_repository import TemplateRepository


def handler(event, context):
    # Retrieve data from the event
    data = json.loads(event["body"])

    print("logging data:")
    print(data)

    template_repo = TemplateRepository(os.environ[TABLE_NAME_KEY])

    try:
        template_model = template_repo.create_template(data)

        response_item = template_repo.get_template(template_model.template_id,
                                                   template_model.template_type)

        print("Data inserted successfully: {}".format(response_item))
        return generate_response(200, body=response_item)

    except Exception as e:
        print("Error inserting data: {}".format(str(e)))
        return generate_response(500, body="Error inserting data {}".format(str(e)))
