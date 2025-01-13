import aws_cdk as core
import aws_cdk.assertions as assertions

from hello_cdk.hello_cdk_stack import HelloCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in 13_hello_cdk/13_hello_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = HelloCdkStack(app, "13-hello-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
