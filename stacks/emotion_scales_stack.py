from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    Fn
)
from constructs import Construct

from stacks.cognito_construct import CognitoConstruct


class EmotionScalesStack(Stack):

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
                                 "EmotionScalesApi",
                                 default_cors_preflight_options=apigateway.CorsOptions(
                                     allow_origins=apigateway.Cors.ALL_ORIGINS,
                                     allow_methods=apigateway.Cors.ALL_METHODS,
                                     allow_headers=["*"]
                                 ))

        response_table = dynamodb.Table(self, "EmotionScalesResponseTable",
                                        partition_key=dynamodb.Attribute(
                                            name="id",
                                            type=dynamodb.AttributeType.STRING
                                        ),
                                        billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                                        )

        create_user_lambda = lambda_.Function(
            self, "CreateUserEmotionScales",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="create_emotion_scale_user.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": response_table.table_name
            },
            layers=[layer]
        )

        get_users_lambda = lambda_.Function(
            self, "GetUsersEmotionScales",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="get_users.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": response_table.table_name
            },
            memory_size=512,
            layers=[layer]
        )

        response_table.grant_read_write_data(create_user_lambda)
        response_table.grant_read_data(get_users_lambda)

        emotion_scales_users = api.root.add_resource("emotion_scales_users")
        emotion_scales_users.add_method("POST", apigateway.LambdaIntegration(create_user_lambda),
                                        authorizer=authorizer,
                                        authorization_type=apigateway.AuthorizationType.COGNITO
                                        )

        emotion_scales_users.add_method("GET", apigateway.LambdaIntegration(get_users_lambda),
                                        authorizer=authorizer,
                                        authorization_type=apigateway.AuthorizationType.COGNITO
                                        )
