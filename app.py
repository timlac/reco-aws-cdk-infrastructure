#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.cognito_stack import CognitoStack

from stacks.emotion_data_stack import EmotionDataStack

app = cdk.App()

CognitoStack(app, "CognitoStack")

EmotionDataStack(app, "EmotionDataStack")

app.synth()
