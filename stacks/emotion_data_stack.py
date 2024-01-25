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
                 env: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        layer = lambda_.LayerVersion(
            self, 'DependencyLayer',
            code=lambda_.Code.from_asset('lambda/my-layer.zip'),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_10],
            description='A layer containing my Python dependencies'
        )

        # Cognito
        user_pool_id = self.node.try_get_context(f"userPoolId-{env}")
        # Import the existing User Pool
        user_pool = UserPool.from_user_pool_id(self, "ImportedUserPool", user_pool_id)
        # Create an authorizer linked to the Cognito User Pool
        authorizer = apigateway.CognitoUserPoolsAuthorizer(self, "CognitoAuthorizer",
                                                           cognito_user_pools=[user_pool])
        # Api Definition
        api = apigateway.RestApi(self,
                                 f"survey_api-{env}",
                                 default_cors_preflight_options=apigateway.CorsOptions(
                                     allow_origins=apigateway.Cors.ALL_ORIGINS,
                                     allow_methods=apigateway.Cors.ALL_METHODS,
                                     allow_headers=["*"]),
                                 deploy=False
                                 )

        # DynamoDB
        survey_table = dynamodb.Table(self, "survey_table",
                                      partition_key=dynamodb.Attribute(
                                          name="survey_type",
                                          type=dynamodb.AttributeType.STRING
                                      ),
                                      sort_key=dynamodb.Attribute(
                                          name="survey_id",
                                          type=dynamodb.AttributeType.STRING
                                      ),
                                      billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                                      )

        survey_type_table = dynamodb.Table(self, "survey-type-table",
                                           partition_key=dynamodb.Attribute(
                                               name="survey_type",
                                               type=dynamodb.AttributeType.STRING
                                           ),
                                           billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                                           )

        # Lambdas
        create_survey_lambda = lambda_.Function(
            self, "CreateSurvey",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="create_survey.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": survey_table.table_name
            },
            layers=[layer]
        )

        get_surveys_lambda = lambda_.Function(
            self, "GetSurveys",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="get_surveys.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": survey_table.table_name
            },
            memory_size=2048,
            layers=[layer]
        )

        get_specific_survey_lambda = lambda_.Function(
            self, "GetSpecificSurvey",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="get_specific_survey.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": survey_table.table_name
            },
            layers=[layer]
        )

        put_reply = lambda_.Function(
            self, "PutReply",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="update_survey.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE_NAME": survey_table.table_name
            },
            memory_size=512,
            layers=[layer]
        )

        get_survey_type = lambda_.Function(self, "GetSurveyType",
                                           runtime=lambda_.Runtime.PYTHON_3_10,
                                           handler="get_survey_type.handler",
                                           code=lambda_.Code.from_asset("lambda"),
                                           environment={"DYNAMODB_TABLE_NAME": survey_table.table_name},
                                           memory_size=512,
                                           layers=[layer]
                                           )

        create_survey_type = lambda_.Function(self, "CreateSurveyType",
                                              runtime=lambda_.Runtime.PYTHON_3_10,
                                              handler="create_survey_type.handler",
                                              code=lambda_.Code.from_asset("lambda"),
                                              environment={"DYNAMODB_TABLE_NAME": survey_table.table_name},
                                              memory_size=512,
                                              layers=[layer]
                                              )

        survey_table.grant_read_write_data(create_survey_lambda)
        survey_table.grant_read_data(get_surveys_lambda)
        survey_table.grant_read_data(get_specific_survey_lambda)
        survey_table.grant_read_write_data(put_reply)

        survey_type_table.grant_read_write_data(get_survey_type)
        survey_type_table.grant_read_write_data(create_survey_type)

        # Api routes
        response_type = api.root.add_resource("{survey_type}")

        response_type.add_method("GET", apigateway.LambdaIntegration(get_survey_type),
                                 authorizer=authorizer,
                                 authorization_type=apigateway.AuthorizationType.COGNITO)

        surveys = response_type.add_resource("surveys")

        # backoffice endpoints
        surveys.add_method("POST", apigateway.LambdaIntegration(create_survey_lambda),
                           authorizer=authorizer,
                           authorization_type=apigateway.AuthorizationType.COGNITO
                           )
        surveys.add_method("GET", apigateway.LambdaIntegration(get_surveys_lambda),
                           authorizer=authorizer,
                           authorization_type=apigateway.AuthorizationType.COGNITO
                           )

        specific_user = surveys.add_resource("{survey_id}")

        # survey front-end endpoints
        specific_user.add_method("GET", apigateway.LambdaIntegration(get_specific_survey_lambda))
        specific_user.add_method("PUT", apigateway.LambdaIntegration(put_reply))

        # Api Deployment
        api_deployment = apigateway.Deployment(self, "APIDeployment", api=api)
        api_stage = apigateway.Stage(self, f"{env}", deployment=api_deployment, stage_name=env)
