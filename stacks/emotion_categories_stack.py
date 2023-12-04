from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    Fn
)
from constructs import Construct


class EmotionCategoriesStack(Stack):

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 api_stack,
                 lambda_layer_stack,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        layer = lambda_layer_stack.lambda_layer

        api = api_stack.api
        authorizer = api_stack.authorizer

        table = dynamodb.Table(self, "EmotionCategoriesResponseTable",
                               partition_key=dynamodb.Attribute(
                                   name="id",
                                   type=dynamodb.AttributeType.STRING
                               ),
                               billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                               )

        # This function needs to be adapted for each api
        create_user_lambda = lambda_.Function(
            self, "CreateUserEmotionCategories",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="create_emotion_categories_user.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": table.table_name
            },
            layers=[layer]
        )

        # This function is the same for both dbs
        get_users_lambda = lambda_.Function(
            self, "GetUsersEmotionCategories",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="get_user.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": table.table_name
            },
            memory_size=512,
            layers=[layer]
        )

        # This function is the same for both dbs
        get_specific_user_lambda = lambda_.Function(
            self, "GetSpecificUserEmotionCategories",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="get_specific_user.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": table.table_name
            },
            memory_size=512,
            layers=[layer]
        )

        table.grant_read_write_data(create_user_lambda)
        table.grant_read_data(get_users_lambda)
        table.grant_read_data(get_specific_user_lambda)

        emotion_scales_users = api.root.add_resource("emotion_categories_users")

        # backoffice endpoints
        emotion_scales_users.add_method("POST", apigateway.LambdaIntegration(create_user_lambda),
                                        authorizer=authorizer,
                                        authorization_type=apigateway.AuthorizationType.COGNITO
                                        )
        emotion_scales_users.add_method("GET", apigateway.LambdaIntegration(get_users_lambda),
                                        authorizer=authorizer,
                                        authorization_type=apigateway.AuthorizationType.COGNITO
                                        )

        specific_user = emotion_scales_users.add_resource("{userId}")

        # front-end endpoints
        specific_user.add_method("GET", apigateway.LambdaIntegration(get_specific_user_lambda))
