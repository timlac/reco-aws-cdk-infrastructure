from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as lambda_
)
from constructs import Construct

from .cognito_construct import CognitoConstruct


class MainStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        dynamodb.Table(self, "UsersEmotionScales",
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

        # Instantiate the Cognito stack
        cognito_construct = CognitoConstruct(self, "CognitoConstruct")

        # Create an authorizer linked to the Cognito User Pool
        authorizer = apigateway.CognitoUserPoolsAuthorizer(self, "CognitoAuthorizer",
                                                           cognito_user_pools=[cognito_construct.user_pool]
                                                           )

        base_path_lambda = lambda_.Function(
            self, "BasePathLambda",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="base_path.handler",  # Make sure you have a 'welcome' function in a file named 'welcome.py'
            code=lambda_.Code.from_asset("lambda"),  # Point to the directory containing your Lambda code
        )

        # Define the API Gateway
        api = apigateway.RestApi(self, "BackOfficeApi")

        api.root.add_method("GET", apigateway.LambdaIntegration(base_path_lambda),
                            authorizer=authorizer,
                            authorization_type=apigateway.AuthorizationType.COGNITO,
                            )