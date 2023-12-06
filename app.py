#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.cognito_stack import CognitoStack
from stacks.emotion_scales_stack import EmotionScalesStack
from stacks.emotion_categories_stack import EmotionCategoriesStack
from stacks.video_metadata_stack import VideoMetadataStack

app = cdk.App()

CognitoStack(app, "CognitoStack")
EmotionScalesStack(app, "EmotionScalesStack")
EmotionCategoriesStack(app, "EmotionCategoriesStack")
VideoMetadataStack(app, "VideoMetadataStack")

app.synth()
