from utils import get_metadata


def add_to_folder_dict(object_key, folder_dict):
    parts = object_key.split("/")

    source_folder = parts[0]
    partition_folder = parts[1]
    object_name = parts[2]

    if source_folder not in folder_dict:
        folder_dict[source_folder] = {}

    if partition_folder not in folder_dict[source_folder]:
        folder_dict[source_folder][partition_folder] = []

    folder_dict[source_folder][partition_folder].append(object_name)


def add_metadata(folder_dict):
    for source_folder in folder_dict.keys():
        mix = 0
        emotion_ids = set()
        for partition_folder, files in folder_dict[source_folder].items():
            if partition_folder == "experiment":
                for file_name in files:
                    meta = get_metadata(file_name)
                    if meta.get("mix") == 1:
                        mix = 1
                    emotion_ids.add(meta.get("emotion_1_id"))
                    if mix == 1:
                        emotion_ids.add(meta.get("emotion_2_id"))
        folder_dict[source_folder]["experiment_metadata"] = {
            "emotion_ids": list(emotion_ids),
            "mix": mix
        }


def create_folder_dict(objects):
    folder_dict = {}

    # Separate objects into folders and non-folders
    for obj in objects:
        object_key = obj['Key']
        # Check if it's a folder (common prefix)
        if object_key.endswith('/'):
            continue
        else:
            add_to_folder_dict(object_key, folder_dict)

    return folder_dict