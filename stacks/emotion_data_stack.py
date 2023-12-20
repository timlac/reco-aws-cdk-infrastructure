from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    Fn
)
from constructs import Construct
from aws_cdk.aws_cognito import UserPool


class EmotionDataStack(Stack):

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 table_name: str,
                 api_name: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        layer = lambda_.LayerVersion(
            self, 'DependencyLayer',
            code=lambda_.Code.from_asset('lambda/my-layer.zip'),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_10],
            description='A layer containing my Python dependencies'
        )

        user_pool_id = self.node.try_get_context("userPoolId")

        # Import the existing User Pool
        user_pool = UserPool.from_user_pool_id(self, "ImportedUserPool", user_pool_id)

        # Create an authorizer linked to the Cognito User Pool
        authorizer = apigateway.CognitoUserPoolsAuthorizer(self, "CognitoAuthorizer",
                                                           cognito_user_pools=[user_pool])

        api = apigateway.RestApi(self,
                                 api_name,
                                 default_cors_preflight_options=apigateway.CorsOptions(
                                     allow_origins=apigateway.Cors.ALL_ORIGINS,
                                     allow_methods=apigateway.Cors.ALL_METHODS,
                                     allow_headers=["*"]
                                 ))

        table = dynamodb.Table(self, table_name,
                               partition_key=dynamodb.Attribute(
                                   name="id",
                                   type=dynamodb.AttributeType.STRING
                               ),
                               billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                               )

        # This function needs to be adapted for each api
        create_survey_lambda = lambda_.Function(
            self, "CreateSurvey",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="emotion_categories.create_survey.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": table.table_name
            },
            layers=[layer]
        )

        # This function is the same for both dbs
        get_surveys_lambda = lambda_.Function(
            self, "GetSurveys",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="get_surveys.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": table.table_name
            },
            memory_size=2048,
            layers=[layer]
        )

        # This function is the same for both dbs
        get_specific_survey_lambda = lambda_.Function(
            self, "GetSpecificSurvey",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="get_specific_survey.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": table.table_name
            },
            layers=[layer]
        )

        put_reply = lambda_.Function(
            self, "PutReply",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="emotion_categories.update_survey.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": table.table_name
            },
            memory_size=512,
            layers=[layer]
        )

        table.grant_read_write_data(create_survey_lambda)
        table.grant_read_data(get_surveys_lambda)
        table.grant_read_data(get_specific_survey_lambda)
        table.grant_read_write_data(put_reply)

        users = api.root.add_resource("users")

        # backoffice endpoints
        users.add_method("POST", apigateway.LambdaIntegration(create_survey_lambda),
                         authorizer=authorizer,
                         authorization_type=apigateway.AuthorizationType.COGNITO
                         )
        users.add_method("GET", apigateway.LambdaIntegration(get_surveys_lambda),
                         authorizer=authorizer,
                         authorization_type=apigateway.AuthorizationType.COGNITO
                         )

        specific_user = users.add_resource("{userId}")

        # front-end endpoints
        specific_user.add_method("GET", apigateway.LambdaIntegration(get_specific_survey_lambda))
        specific_user.add_method("PUT", apigateway.LambdaIntegration(put_reply))
