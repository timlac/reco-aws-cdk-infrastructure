from aws_cdk import (
    aws_cognito as cognito,
    CfnOutput
)

from constructs import Construct


class CognitoConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id)

        # Create a new Cognito User Pool
        self.user_pool = cognito.UserPool(self, "BackOfficeUserPool",
                                          self_sign_up_enabled=False,  # Users cannot sign themselves up
                                          sign_in_aliases=cognito.SignInAliases(username=True, email=True),
                                          auto_verify=cognito.AutoVerifiedAttrs(email=True),
                                          standard_attributes=cognito.StandardAttributes(
                                              email=cognito.StandardAttribute(mutable=True, required=True)
                                          ),
                                          account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
                                          # Additional configurations as necessary
                                          )

        user_pool_client = self.user_pool.add_client("BackOfficeClient",
                                                     generate_secret=False,
                                                     # Creates a client secret for this app client
                                                     auth_flows=cognito.AuthFlow(
                                                         user_password=True,
                                                         # Enables username and password based authentication
                                                         user_srp=True,
                                                         # Enables Secure Remote Password protocol
                                                         # to eliminate need for sending password
                                                     ),
                                                     o_auth=cognito.OAuthSettings(
                                                         flows=cognito.OAuthFlows(
                                                             implicit_code_grant=True,
                                                             # Enables the OAuth implicit code grant flow
                                                         ),
                                                         scopes=[cognito.OAuthScope.EMAIL],
                                                         # Restricts app access to the user's email
                                                     ),
                                                     # Additional settings can be configured as needed
                                                     prevent_user_existence_errors=True,
                                                     # Prevents user enumeration attacks
                                                     )

        self.user_pool.add_domain("CognitoDomain",
                                  cognito_domain=cognito.CognitoDomainOptions(
                                      domain_prefix="reco-backoffice",  # This will be part of your endpoint URL
                                  )
                                  )

        # Outputs
        CfnOutput(self, "UserPoolId", value=self.user_pool.user_pool_id)
        CfnOutput(self, "UserPoolClientId", value=user_pool_client.user_pool_client_id)
