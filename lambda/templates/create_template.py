import os
import json

from utils import generate_response
from constants import TABLE_NAME_KEY
from templates.template_repository import TemplateRepository
from templates.template_model import TemplateModel

def handler(event, context):
    # Retrieve data from the event
    data = json.loads(event["body"])

    print("logging data:")
    print(data)

    template_repo = TemplateRepository(os.environ[TABLE_NAME_KEY])

    try:
        template_model = TemplateModel(**data)

        template_model_resp = template_repo.create_template(template_model)

        response_item = template_repo.get_template(template_model_resp.template_type,
                                                   template_model_resp.template_name)

        print("Data inserted successfully: {}".format(response_item))
        return generate_response(200, body=response_item)

    except Exception as e:
        print("Error inserting data: {}".format(str(e)))
        return generate_response(500, body="Error inserting data {}".format(str(e)))
