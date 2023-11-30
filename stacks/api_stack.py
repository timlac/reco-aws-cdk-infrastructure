from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    CfnOutput
)

from constructs import Construct

from .cognito_construct import CognitoConstruct


class ApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Instantiate the Cognito stack
        cognito_construct = CognitoConstruct(self, "CognitoConstruct")

        # Create an authorizer linked to the Cognito User Pool
        self.authorizer = apigateway.CognitoUserPoolsAuthorizer(self, "CognitoAuthorizer",
                                                                cognito_user_pools=[cognito_construct.user_pool])

        self.api = apigateway.RestApi(self,
                                      "BackOfficeApi",
                                      default_cors_preflight_options=apigateway.CorsOptions(
                                          allow_origins=apigateway.Cors.ALL_ORIGINS,
                                          allow_methods=apigateway.Cors.ALL_METHODS,
                                          allow_headers=["*"]
                                      ))