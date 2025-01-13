import pulumi_aws as aws


def create():
    vpc = aws.ec2.Vpc('vpc',
        cidr_block='10.0.0.0/16',
        tags={
            'Name': 'vpc',
        }
    )

    public_subnet = aws.ec2.Subnet('public_subnet',
        vpc_id=vpc.id,
        cidr_block='10.0.1.0/24',
        map_public_ip_on_launch=True,
        tags={
            'Name': 'public_subnet',
        },
    )
