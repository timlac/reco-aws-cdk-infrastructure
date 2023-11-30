#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.api_stack import ApiStack
from stacks.main_stack import MainStack
from stacks.lambda_layer_stack import LambdaLayerStack
from stacks.emotion_scales_stack import EmotionScalesStack
from stacks.emotion_categories_stack import EmotionCategoriesStack
from stacks.video_metadata_stack import VideoMetadataStack

app = cdk.App()

lambda_layer_stack = LambdaLayerStack(app, "LambdaLayerStack")

api_stack = ApiStack(app, "ApiStack")

MainStack(app, "MainStack", api_stack)

EmotionScalesStack(app, "EmotionScalesStack", api_stack, lambda_layer_stack)
EmotionCategoriesStack(app, "EmotionCategoriesStack", api_stack, lambda_layer_stack)
VideoMetadataStack(app, "VideoMetadataStack", api_stack, lambda_layer_stack)

app.synth()
