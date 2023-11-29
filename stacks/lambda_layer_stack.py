from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    CfnOutput
)

from constructs import Construct

from .cognito_construct import CognitoConstruct


class LambdaLayerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.lambda_layer = lambda_.LayerVersion(
            self, 'DependencyLayer',
            code=lambda_.Code.from_asset('lambda/my-layer.zip'),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_10],
            description='A layer containing my Python dependencies'
        )

        # self.lambda_layer_arn = lambda_layer.layer_version_arn

        # # Export the Layer ARN
        # CfnOutput(
        #     self, "DependencyLayerArnOutput",
        #     value=lambda_layer.layer_version_arn,
        #     export_name="DependencyLayerArn"
        # )

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
