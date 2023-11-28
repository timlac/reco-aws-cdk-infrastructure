from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_iam as iam,
    Duration
)
from constructs import Construct

from .cognito_construct import CognitoConstruct


from .emotion_scales_stack import EmotionScalesStack
from .emotion_categories_stack import EmotionCategoriesStack
from .shared_resources_stack import SharedResourcesStack
from .video_metadata_stack import VideoMetadataStack


class MainStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "video-files-720p")

        shared_resources = SharedResourcesStack(self, "SharedResources")

        base_path_lambda = lambda_.Function(
            self, "BasePathLambda",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="base_path.handler",
            code=lambda_.Code.from_asset("lambda"),
        )

        # Define the API Gateway
        api = apigateway.RestApi(self,
                                 "BackOfficeApi",
                                 default_cors_preflight_options=apigateway.CorsOptions(
                                     allow_origins=apigateway.Cors.ALL_ORIGINS,
                                     allow_methods=apigateway.Cors.ALL_METHODS,
                                     allow_headers=["*"]
                                 ))

        api.root.add_method("GET", apigateway.LambdaIntegration(base_path_lambda),
                            authorizer=authorizer,
                            authorization_type=apigateway.AuthorizationType.COGNITO,
                            )

        emotion_scales_stack = EmotionScalesStack(self,
                                                  "EmotionScalesStack",
                                                  authorizer=authorizer,
                                                  layer_arn=shared_resources.lambda_layer_arn,
                                                  api=api)

        emotion_categories_stack = EmotionCategoriesStack(self,
                                                          "EmotionCategoriesStack",
                                                          authorizer=authorizer,
                                                          layer_arn=shared_resources.lambda_layer_arn,
                                                          api=api)

        video_metadata_stack = VideoMetadataStack(self,
                                                  "VideoMetadataStack",
                                                  authorizer=authorizer,
                                                  layer_arn=shared_resources.lambda_layer_arn,
                                                  api=api)

