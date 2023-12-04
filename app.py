#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.emotion_scales_stack import EmotionScalesStack
from stacks.emotion_categories_stack import EmotionCategoriesStack
from stacks.video_metadata_stack import VideoMetadataStack

app = cdk.App()

EmotionScalesStack(app, "EmotionScalesStack")
EmotionCategoriesStack(app, "EmotionCategoriesStack")
VideoMetadataStack(app, "VideoMetadataStack")

app.synth()
