from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    # aws_sqs as sqs,
)
from constructs import Construct

class HelloCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self,
            "hello-vpc",
            max_azs=2,
            nat_gateways=1,
        )

        ec2.Instance(
            self,
            'hello-cdk',
            vpc=vpc,
            instance_type=ec2.InstanceType('t2.micro'),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
        )
