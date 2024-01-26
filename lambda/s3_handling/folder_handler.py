from nexa_sentimotion_filename_parser.metadata import Metadata
from pathlib import Path


def add_to_folder_dict(obj, folder_dict):
    object_key = obj['Key']
    # Split the key into parts based on '/'
    parts = object_key.split('/')
    if len(parts) > 1:
        folder_name = parts[0] + '/'  # Folder name with trailing '/'
        object_name = parts[-1]  # Object name

        # Check if the folder name is already in the dictionary, if not, initialize it
        if folder_name not in folder_dict:
            folder_dict[folder_name] = {
                    'objects': [],
                    'emotion_ids': set()
                }

        # Append the object name to the folder's list
        folder_dict[folder_name]["objects"].append(object_name)
        folder_dict[folder_name]["emotion_ids"].add(get_emotion_id(object_key))


def get_emotion_id(object_key):
    filename = Path(object_key).stem
    metadata = Metadata(filename)

    return metadata.emotion_1_id


def create_folder_dict(objects):
    folder_dict = {}

    print("creating folder dictionary")

    # Separate objects into folders and non-folders
    for obj in objects:
        object_key = obj['Key']
        # Check if it's a folder (common prefix)
        if object_key.endswith('/'):
            continue
        else:
            add_to_folder_dict(obj, folder_dict)

    return folder_dict
