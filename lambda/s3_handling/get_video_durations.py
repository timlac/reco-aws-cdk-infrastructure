# from pymediainfo import MediaInfo
# import tempfile
# import os
# import boto3
#
# s3 = boto3.client('s3')
#
#
# def get_video_duration(bucket, key):
#     # Create a temporary file
#     with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#         # Get the object from the S3 bucket
#         obj = s3.get_object(Bucket=bucket, Key=key)
#         tmp_file.write(obj['Body'].read())
#         tmp_file_path = tmp_file.name
#
#     # Using MediaInfo to parse the video data
#     media_info = MediaInfo.parse(tmp_file_path)
#     duration = None
#     for track in media_info.tracks:
#         if track.track_type == 'Video':
#             duration = track.duration  # Duration in milliseconds
#
#     # Clean up the temporary file
#     os.remove(tmp_file_path)
#     return duration
