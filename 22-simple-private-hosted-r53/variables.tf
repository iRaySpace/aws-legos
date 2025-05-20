variable "vpc_id" {
    description = "The VPC ID to associate with"
    type        = string
}

variable "subnet_id" {
    description = "The Subnet ID to associate with"
    type        = string
}

variable "iam_instance_profile" {
    description = "The IAM Instance Profile to associate with"
    type        = string
}
