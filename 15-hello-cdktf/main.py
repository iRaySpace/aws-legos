#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.instance import Instance


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        AwsProvider(
            self,
            'Aws',
            region='us-east-1',
        )

        instance = Instance(
            self,
            'compute',
            ami='ami-05576a079321f21f8',
            instance_type='t2.micro',
        )

        TerraformOutput(
            self,
            'public_ip',
            value=instance.public_ip,
        )


app = App()
MyStack(app, "hello-cdktf")

app.synth()
