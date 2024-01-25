from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_s3 as s3
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

        s3_bucket_name = 'reco-video-files'
        s3_bucket = s3.Bucket.from_bucket_name(
            self, "cdk-reco-video-files",
            s3_bucket_name,
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
                                          name="survey_name",
                                          type=dynamodb.AttributeType.STRING
                                      ),
                                      sort_key=dynamodb.Attribute(
                                          name="survey_id",
                                          type=dynamodb.AttributeType.STRING
                                      ),
                                      billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                                      )

        survey_name_table = dynamodb.Table(self, "survey-name-table",
                                           partition_key=dynamodb.Attribute(
                                               name="survey_name",
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

        get_survey_name = lambda_.Function(self, "GetSurveyName",
                                           runtime=lambda_.Runtime.PYTHON_3_10,
                                           handler="get_survey_name.handler",
                                           code=lambda_.Code.from_asset("lambda"),
                                           environment={"DYNAMODB_TABLE_NAME": survey_table.table_name},
                                           memory_size=512,
                                           layers=[layer]
                                           )

        create_survey_name = lambda_.Function(self, "CreateSurveyName",
                                              runtime=lambda_.Runtime.PYTHON_3_10,
                                              handler="create_survey_name.handler",
                                              code=lambda_.Code.from_asset("lambda"),
                                              environment={"DYNAMODB_TABLE_NAME": survey_table.table_name},
                                              memory_size=512,
                                              layers=[layer]
                                              )

        get_s3_folders = lambda_.Function(self, "GetS3Folders",
                                          runtime=lambda_.Runtime.PYTHON_3_10,
                                          handler="get_s3_folders.handler",
                                          code=lambda_.Code.from_asset("lambda"),
                                          environment={"S3_BUCKET_NAME": s3_bucket_name},
                                          memory_size=2048,
                                          layers=[layer]
                                          )

        s3_bucket.grant_read(get_s3_folders)

        survey_table.grant_read_write_data(create_survey_lambda)
        survey_table.grant_read_data(get_surveys_lambda)
        survey_table.grant_read_data(get_specific_survey_lambda)
        survey_table.grant_read_write_data(put_reply)

        survey_name_table.grant_read_write_data(get_survey_name)
        survey_name_table.grant_read_write_data(create_survey_name)

        # Api routes
        survey_name = api.root.add_resource("{survey_name}")

        survey_name.add_method("GET", apigateway.LambdaIntegration(get_survey_name),
                               authorizer=authorizer,
                               authorization_type=apigateway.AuthorizationType.COGNITO)

        survey_name.add_method("POST", apigateway.LambdaIntegration(create_survey_name),
                               authorizer=authorizer,
                               authorization_type=apigateway.AuthorizationType.COGNITO)

        surveys = survey_name.add_resource("surveys")

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

        s3_folders = api.root.add_resource("s3_folders")

        s3_folders.add_method("GET", apigateway.LambdaIntegration(get_s3_folders))
