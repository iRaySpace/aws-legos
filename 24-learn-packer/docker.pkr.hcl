packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

variable "iam_instance_profile" {
  type = string
}

variable "security_group_id" {
  type = string
}

variable "subnet_id" {
  type = string
}

source "amazon-ebs" "al2023" {
  region        = "us-east-1"
  instance_type = "t2.micro"
  source_ami    = "ami-02457590d33d576c3"

  ami_name      = "docker-{{timestamp}}"
  ssh_username  = "ec2-user"
  ssh_interface = "session_manager"
  communicator  = "ssh"

  subnet_id            = var.subnet_id
  security_group_id    = var.security_group_id
  iam_instance_profile = var.iam_instance_profile
}

build {
  sources = ["source.amazon-ebs.al2023"]
  provisioner "shell" {
    inline = [
      "sudo dnf update -y",
      "sudo dnf install -y docker",
      "sudo systemctl enable docker",
      "sudo systemctl start docker",
      "sudo usermod -aG docker ec2-user"
    ]
  }
}