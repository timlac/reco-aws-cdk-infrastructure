# from surveys.filename_sampling.frequency_2_filename import generate_frequency_2_filename
# from surveys.filename_sampling.sample_filenames import balanced_filename_sampling
#
# import math
# from collections import Counter
# import time
# from collections import Counter
# import json
#
# from utils import get_emotion_id
#
# path = "data/project_data.json"
#
# with open(path) as json_data:
#     project_data = json.load(json_data)
#     json_data.close()
#
#
# f2f = generate_frequency_2_filename([], project_data["s3_experiment_objects"])
# eis = [get_emotion_id(filename) for filename in project_data["s3_experiment_objects"]]
#
# eis = list(set(eis))
#
# start = time.time()
# final_filenames = balanced_filename_sampling(f2f, eis, 100)
# end = time.time()
#
# print("elasped time: ", end - start)
#
#
# final_emotion_ids = [get_emotion_id(filename) for filename in final_filenames]
#
# print(final_emotion_ids)
#
# counts = Counter(final_emotion_ids)
#
# for i in counts.items():
#     if i[0] == 22:
#         print()
#     print(i)
#
# print(len(final_emotion_ids))




#
#
# os.environ['AWS_PROFILE'] = 'rackspaceAcc'
#
# survey_repo = SurveyRepository("EmotionDataStack-dev-surveytable310F762D-1SADR68QRMPOO")
#
# response_items = survey_repo.get_surveys("singletest")

# print(response_items)
