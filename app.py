#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.main_stack import MainStack
from stacks.shared_resources_stack import SharedResourcesStack
from stacks.emotion_scales_stack import EmotionScalesStack
from stacks.emotion_categories_stack import EmotionCategoriesStack
from stacks.video_metadata_stack import VideoMetadataStack

app = cdk.App()

shared_resources = SharedResourcesStack(app, "SharedResourcesStack")

MainStack(app, "MainStack", shared_resources)

EmotionScalesStack(app, "EmotionScalesStack", shared_resources)
EmotionCategoriesStack(app, "EmotionCategoriesStack", shared_resources)
VideoMetadataStack(app, "VideoMetadataStack", shared_resources)

app.synth()
