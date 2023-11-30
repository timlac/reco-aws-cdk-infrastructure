from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    CfnOutput
)

from constructs import Construct


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
        #
        # # Export the Layer ARN
        # CfnOutput(
        #     self, "DependencyLayerArnOutput",
        #     value=lambda_layer.layer_version_arn,
        #     export_name="DependencyLayerArn"
        # )