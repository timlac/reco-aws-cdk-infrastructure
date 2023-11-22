import random


def sample(df_):

    categories = df_["emotion_id"].unique()

    # Initialize an empty dictionary to store videos by category combination
    category_videos = {combo: [] for combo in categories}

    # Categorize videos based on all category combinations
    for _, row in df_.iterrows():
        category = row["emotion_id"]
        category_videos[category].append(row['filename'])

    # Initialize an empty list to store the final set of 132 videos for each rater
    ret = []

    # Stratified sampling within each category combination
    for category in categories:
        videos = category_videos[category]

        selected_videos = random.sample(videos, 1)
        ret.extend(selected_videos)

    return ret
