from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
)
from constructs import Construct


class VideoMetadataStack(Stack):

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 authorizer: apigateway.CognitoUserPoolsAuthorizer,
                 layer_arn: lambda_.LayerVersion,
                 api: apigateway.RestApi,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        video_metadata_table = dynamodb.Table(self, "VideoMetadataTable",
                                              partition_key=dynamodb.Attribute(
                                                  name="filename",
                                                  type=dynamodb.AttributeType.STRING
                                              ),
                                              billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,  # or PROVISIONED
                                              )

        layer = lambda_.LayerVersion.from_layer_version_arn(self, "ImportedLayer", layer_arn)

        get_videos_lambda = lambda_.Function(
            self, "GetVideoMetadata",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="get_video_metadata.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": video_metadata_table.table_name
            },
            memory_size=512,
            layers=[layer]
        )

        video_metadata_table.grant_read_data(get_videos_lambda)

        video_metadata = api.root.add_resource("video_metadata")

        video_metadata.add_method("GET", apigateway.LambdaIntegration(get_videos_lambda),
                                  authorizer=authorizer,
                                  authorization_type=apigateway.AuthorizationType.COGNITO,
                                  )
