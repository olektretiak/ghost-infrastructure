#### Cleanup all Ghost post python serverless fuction



Serverless fuction to cleanup posts via the Ghost API


---

###### Serverless build stack

Source: [lamda-build-stack.yaml](lamda-build-stack.yaml)

The Build stack creates:
    * CodeBuild - builds seerverless source
    * CRS3Bucket - srores build output artifact
    * Lambda fuction - Trigers CodeBuild
    * Custom CodeBuildTrigger

###### Diagram


<img src="../images/lambda-build.stuck.png"  width="600" height="600">


#### Resources
| Type                         | Logical ID                     |
| :---                         |            ---:                |
| AWS::IAM::Policy             | LambdaPolicy                   |
| AWS::IAM::Role               | LambdaExecutionRole            |
| AWS::IAM::Role               | InstanceRole                   |
| AWS::CodeBuild::Project      | ImageBuildProject              |
| AWS::S3::Bucket              | CRS3Bucket                     |
| AWS::IAM::Policy             | CodeBuildServiceRolePolicy     |
| AWS::Lambda::Function        | CodeBuildInitFunction          |
| Custom::CodeBuildTrigger     | CodeBuildInit                  |



#### Serverless Fuction

Source: [lambda-cleanup-stack.yaml](lambda-cleanup-stack.yaml)

---

###### Diagram


<img src="../images/ghost-cleanaup-fuction.png"  width="470" height="390">


###### Resources

| Type                         | Logical ID                             |
| :---                         |            ---:                        |
| AWS::IAM::Role               | GhostCleanAllPostsLambdaExecutionRole  |
| AWS::IAM::Policy             | GhostCleanAllPostsLambdaExecutionPolicy|
| AWS::Lambda::Function        | GhostCleanAllPostsFunction             |



###### Event JSON exmple

```
{
    "blog_endpoint": "https://blog.otk.ninja",
    "content_api_key": "<Ghost content api token>",
    "admin_api_key": "<GHOST admin API token>"
}
```

###### Event log example:

```
[INFO]	2023-02-06T20:48:58.344Z	324e5b15-9e65-44de-9fd3-cceeb2c003e4	Creating headers...
[INFO]	2023-02-06T20:48:58.344Z	324e5b15-9e65-44de-9fd3-cceeb2c003e4	Creating headers...
[INFO]	2023-02-06T20:48:58.345Z	324e5b15-9e65-44de-9fd3-cceeb2c003e4	Getting all posts...
[INFO]	2023-02-06T20:48:58.652Z	324e5b15-9e65-44de-9fd3-cceeb2c003e4	post id will be deleted: 63e152b0b1507a000152da33
[INFO]	2023-02-06T20:48:59.463Z	324e5b15-9e65-44de-9fd3-cceeb2c003e4	success: post deleted (status_code:204)
[INFO]	2023-02-06T20:48:59.464Z	324e5b15-9e65-44de-9fd3-cceeb2c003e4	post id will be deleted: 63e152a5b1507a000152da2b
[INFO]	2023-02-06T20:48:59.777Z	324e5b15-9e65-44de-9fd3-cceeb2c003e4	success: post deleted (status_code:204)
END RequestId: 324e5b15-9e65-44de-9fd3-cceeb2c003e4
REPORT RequestId: 324e5b15-9e65-44de-9fd3-cceeb2c003e4	Duration: 2102.39 ms	Billed Duration: 2103 ms	Memory Size: 128 MB	Max Memory Used: 50 MB	Init Duration: 213.11 ms	
```

