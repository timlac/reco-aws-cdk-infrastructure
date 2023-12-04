from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    Fn
)
from constructs import Construct

from stacks.cognito_construct import CognitoConstruct


class VideoMetadataStack(Stack):

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        layer = lambda_.LayerVersion(
            self, 'DependencyLayer',
            code=lambda_.Code.from_asset('lambda/my-layer.zip'),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_10],
            description='A layer containing my Python dependencies'
        )

        # Instantiate the Cognito stack
        cognito_construct = CognitoConstruct(self, "CognitoConstruct")

        # Create an authorizer linked to the Cognito User Pool
        authorizer = apigateway.CognitoUserPoolsAuthorizer(self, "CognitoAuthorizer",
                                                           cognito_user_pools=[cognito_construct.user_pool])

        api = apigateway.RestApi(self,
                                 "VideoMetaDataApi",
                                 default_cors_preflight_options=apigateway.CorsOptions(
                                     allow_origins=apigateway.Cors.ALL_ORIGINS,
                                     allow_methods=apigateway.Cors.ALL_METHODS,
                                     allow_headers=["*"]
                                 ))

        video_metadata_table = dynamodb.Table(self, "VideoMetadataTable",
                                              partition_key=dynamodb.Attribute(
                                                  name="filename",
                                                  type=dynamodb.AttributeType.STRING
                                              ),
                                              billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,  # or PROVISIONED
                                              )

        get_videos_lambda = lambda_.Function(
            self, "GetVideoMetadata",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="get_all.handler",
            code=lambda_.Code.from_asset("lambda/video_metadata"),
            environment={
                "DYNAMODB_TABLE_NAME": video_metadata_table.table_name
            },
            memory_size=512,
            layers=[layer]
        )

        video_metadata_table.grant_read_data(get_videos_lambda)

        video_metadata = api.root.add_resource("videos")

        video_metadata.add_method("GET", apigateway.LambdaIntegration(get_videos_lambda),
                                  authorizer=authorizer,
                                  authorization_type=apigateway.AuthorizationType.COGNITO,
                                  )
