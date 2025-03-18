import json
import os
from s3_handling.get_s3_folders import handler
from s3_handling.list_bucket_contents import list_all_bucket_contents
from time import time

start = time()


os.environ['AWS_PROFILE'] = 'rackspaceAcc'

os.environ['S3_BUCKET_NAME'] = 'reco-video-files'


# resp = list_all_bucket_contents("reco-video-files")
#
#
# print(resp)

resp = handler(None, None)

print(resp)

