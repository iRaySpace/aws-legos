provider "aws" {
    region = "us-east-1"
}

# EC2 instance
resource "aws_instance" "auth" {
    instance_type = "t2.micro"
    ami = "ami-0953476d60561c955"
    subnet_id = var.subnet_id
    iam_instance_profile = var.iam_instance_profile
    tags = {
        Name = "auth"
    }
}

# Route53
resource "aws_route53_zone" "internal" {
    name = "internal.irayspace"
    vpc {
        vpc_id = var.vpc_id
    }
}

resource "aws_route53_record" "auth" {
    zone_id = aws_route53_zone.internal.zone_id
    name = "auth"
    type = "CNAME"
    ttl = 5
    records = [aws_instance.auth.private_dns]
}