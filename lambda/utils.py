from decimal import Decimal
import json
import hashlib
import uuid
from pathlib import Path

from nexa_sentimotion_filename_parser.metadata import Metadata


def to_serializable(val):
    if isinstance(val, Decimal):
        return str(val)
    return val


def generate_response(status_code, body):
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

