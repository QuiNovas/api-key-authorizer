# api-key-authorizer
Uses HTTP Bearer Authentication against two dynamodb tables to authorize API Gateway API Key users. Note that this both implements suthorization and serves as an _AUTHORIZER_ for an API Gateway usage plan. 

The first table is the "api-key" table. This table contains the SHA256 hashed _Apikey_, and a _GroupId_.

If the API key is found in the "api-key" table (by hashing the key passed in first), then the group IS is looked up in the "groups" table.

The "groups" table contains the _GroupId_ and a _Policy_ JSON document representing the IAM policy document for that user. It is this document that is returned to API Gateway for further processing.

This function supports the following environment variables:
1. **API_KEYS_TABLE** - The DynamoDB table that contains the api key data, as listed above.
2. **GROUPS_TABLE_NAME** - The DynamoDB table that contains the groups data, as listed above.

Easy implementation of this function via Terraform may be found in the following module: 

https://github.com/QuiNovas/terraform-modules/tree/master/aws/api-key-authenticator