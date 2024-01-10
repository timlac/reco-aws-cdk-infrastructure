#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.cognito_stack import CognitoStack

from stacks.emotion_data_stack import EmotionDataStack

app = cdk.App()

env = app.node.try_get_context("env")
env = env if env else 'dev'

CognitoStack(app, f"CognitoStack-{env}", env=env)

EmotionDataStack(app, f"EmotionDataStack-{env}", env=env)

app.synth()
