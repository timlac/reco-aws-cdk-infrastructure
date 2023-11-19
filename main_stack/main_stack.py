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


class MainStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        response_table = dynamodb.Table(self, "EmotionScalesResponseTable",
                                        partition_key=dynamodb.Attribute(
                                            name="id",
                                            type=dynamodb.AttributeType.STRING
                                        ),
                                        sort_key=dynamodb.Attribute(
                                            name="createdAt",
                                            type=dynamodb.AttributeType.NUMBER
                                        ),
                                        billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,  # or PROVISIONED
                                        )

        video_table = dynamodb.Table(self, "VideoMetadataTable",
                                     partition_key=dynamodb.Attribute(
                                         name="filename",
                                         type=dynamodb.AttributeType.STRING
                                     ),
                                     sort_key=dynamodb.Attribute(
                                         name="video_id",
                                         type=dynamodb.AttributeType.NUMBER
                                     ),
                                     billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,  # or PROVISIONED
                                     )

        # Instantiate the Cognito stack
        cognito_construct = CognitoConstruct(self, "CognitoConstruct")

        # Create an authorizer linked to the Cognito User Pool
        authorizer = apigateway.CognitoUserPoolsAuthorizer(self, "CognitoAuthorizer",
                                                           cognito_user_pools=[cognito_construct.user_pool]
                                                           )

        bucket = s3.Bucket(self, "video-files-720p")

        layer = lambda_.LayerVersion(
            self, 'MyLayer',
            code=lambda_.Code.from_asset('lambda/my-layer.zip'),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_10],
            description='A layer containing my Python dependencies'
        )

        base_path_lambda = lambda_.Function(
            self, "BasePathLambda",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="base_path.handler",
            code=lambda_.Code.from_asset("lambda"),
        )

        create_user_lambda = lambda_.Function(
            self, "CreateUser",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="create_user.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": response_table.table_name
            },
            layers=[layer]
        )

        list_videos_lambda = lambda_.Function(
            self, "ListVideos",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="list_videos.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "BUCKET_NAME": bucket.bucket_name
            },
            timeout=Duration.seconds(10),
            memory_size=512,
            layers=[layer]
        )

        get_users_lambda = lambda_.Function(
            self, "GetUsers",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="get_users.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": response_table.table_name
            }
        )

        # Grant permissions for the Lambda function to write to the S3 bucket and DynamoDB table
        bucket.grant_read(list_videos_lambda)
        response_table.grant_read_write_data(create_user_lambda)
        response_table.grant_read_data(get_users_lambda)

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

        users = api.root.add_resource("users")

        users.add_method("POST", apigateway.LambdaIntegration(create_user_lambda),
                         authorizer=authorizer,
                         authorization_type=apigateway.AuthorizationType.COGNITO
                         )

        users.add_method("GET", apigateway.LambdaIntegration(get_users_lambda),
                         authorizer=authorizer,
                         authorization_type=apigateway.AuthorizationType.COGNITO
                         )

        videos = api.root.add_resource("videos")

        videos.add_method("GET", apigateway.LambdaIntegration(list_videos_lambda),
                          authorizer=authorizer,
                          authorization_type=apigateway.AuthorizationType.COGNITO,
                          )
