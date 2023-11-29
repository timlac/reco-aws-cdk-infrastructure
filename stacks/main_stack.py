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


class MainStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, shared_resources, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "video-files-720p")

        base_path_lambda = lambda_.Function(
            self, "BasePathLambda",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="base_path.handler",
            code=lambda_.Code.from_asset("lambda"),
        )

        shared_resources.api.root.add_method("GET", apigateway.LambdaIntegration(base_path_lambda),
                                             authorizer=shared_resources.authorizer,
                                             authorization_type=apigateway.AuthorizationType.COGNITO,
                                             )
