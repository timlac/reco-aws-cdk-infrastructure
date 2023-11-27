from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
)
from constructs import Construct


class EmotionScalesStack(Stack):

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 authorizer: apigateway.CognitoUserPoolsAuthorizer,
                 layer: lambda_.LayerVersion,
                 api: apigateway.RestApi,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        response_table_emotion_categories = dynamodb.Table(self, "EmotionCategoriesResponseTable",
                                                           partition_key=dynamodb.Attribute(
                                                               name="id",
                                                               type=dynamodb.AttributeType.STRING
                                                           ),
                                                           billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                                                           # or PROVISIONED
                                                           )

        # This function needs to be adapted for each api
        create_user_lambda = lambda_.Function(
            self, "CreateUser",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="create_user.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": response_table_emotion_categories.table_name
            },
            layers=[layer]
        )

        # This function is the same for both dbs
        get_users_lambda = lambda_.Function(
            self, "GetUsers",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="get_users.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": response_table_emotion_categories.table_name
            },
            memory_size=512,
            layers=[layer]
        )

        response_table_emotion_categories.grant_read_write_data(create_user_lambda)
        response_table_emotion_categories.grant_read_data(get_users_lambda)

        emotion_scales_users = api.root.add_resource("emotion_categories_users")
        emotion_scales_users.add_method("POST", apigateway.LambdaIntegration(create_user_lambda),
                                        authorizer=authorizer,
                                        authorization_type=apigateway.AuthorizationType.COGNITO
                                        )

        emotion_scales_users.add_method("GET", apigateway.LambdaIntegration(get_users_lambda),
                                        authorizer=authorizer,
                                        authorization_type=apigateway.AuthorizationType.COGNITO
                                        )
