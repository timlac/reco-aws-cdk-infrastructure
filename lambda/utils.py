from decimal import Decimal
import json
import hashlib
import uuid
from pathlib import Path
import datetime
from zoneinfo import ZoneInfo
from dateutil import parser
from datetime import datetime, timedelta, timezone
import dateutil
import gzip
import base64

from nexa_sentimotion_filename_parser.metadata import Metadata
from nexa_py_sentimotion_mapper.sentimotion_mapper import Mapper

from surveys.database.survey_model import SurveyModel


def within_time_delta(survey: SurveyModel, days_threshold):
    if survey.last_modified:
        start_date = parser.isoparse(survey.last_modified)
    else:
        start_date = parser.isoparse(survey.created_at)

    current_date = datetime.now(ZoneInfo("Europe/Berlin"))

    # Calculating the difference
    difference = abs(current_date - start_date)  # Use abs to ensure the difference is non-negative

    # Checking if the difference is more or less than 7 days
    if difference <= timedelta(days=days_threshold):
        return True
    else:
        return False


def to_serializable(val):
    if isinstance(val, Decimal):
        return str(val)
    return val


# def generate_response(status_code, body):
#     return {
#         'statusCode': status_code,
#         'headers': {
#             'Access-Control-Allow-Origin': '*',
#             'Access-Control-Allow-Credentials': True
#         },
#         'body': json.dumps(body, default=to_serializable)
#     }


def generate_response(status_code, body, compressed=False):
    """
    Generate API Gateway response.
    If `compressed=True`, the body is gzipped and base64-encoded.
    """
    if compressed:
        # Compress and Base64-encode the JSON body
        json_data = json.dumps(body, default=to_serializable)
        compressed_data = gzip.compress(json_data.encode("utf-8"))
        encoded_data = base64.b64encode(compressed_data).decode("utf-8")

        return {
            'statusCode': status_code,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
                'Content-Encoding': 'gzip',
                'Content-Type': 'application/json'
            },
            'body': encoded_data,
            'isBase64Encoded': True  # Important for API Gateway to decode correctly
        }

    else:
        # Normal JSON response
        return {
            'statusCode': status_code,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            },
            'body': json.dumps(body, default=to_serializable)
        }


def generate_id():
    # Generate a random UUID
    unique_uuid = uuid.uuid4()
    # Convert the UUID to a string
    uuid_str = str(unique_uuid)
    # Create a hash object using the hashlib library (you can choose a different algorithm)
    hash_object = hashlib.sha256()
    # Update the hash object with the UUID string
    hash_object.update(uuid_str.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    unique_hash = hash_object.hexdigest()
    return unique_hash


def get_emotion_id(filename):
    filename = Path(filename).stem
    metadata = Metadata(filename)

    return metadata.emotion_1_id


def get_valence(filename):
    filename = Path(filename).stem
    metadata = Metadata(filename)
    emotion_id = metadata.emotion_1_id
    emotion = Mapper.get_emotion_from_id(emotion_id)

    return Mapper.get_valence_from_emotion(emotion)


def get_metadata(filename):
    """
    Return a dictionary containing only the selected attributes from the object.

    Parameters:
    - obj: The object from which to select attributes.
    - selected_attributes (list): A list of attribute names that should be included in the returned dictionary.

    Returns:
    dict: A new dictionary containing only the selected attributes and their corresponding values.
    """
    selected_attributes = ["video_id", "mix", "emotion_1_id", "emotion_2_id", "intensity_level"]

    filename = Path(filename).stem
    metadata = Metadata(filename)

    return {attr: getattr(metadata, attr) for attr in selected_attributes if hasattr(metadata, attr)}

