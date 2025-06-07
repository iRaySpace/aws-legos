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

  ami_name      = "hello-{{timestamp}}"
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
      "sudo usermod -aG docker ec2-user",

      # Docker might not be ready
      "sleep 5",

      # Docker Image
      "sudo docker pull irayspace/hello-server",

      # Add to systemd
      "echo '[Unit]' | sudo tee /etc/systemd/system/hello-server.service",
      "echo 'Description=Hello Server Docker Container' | sudo tee -a /etc/systemd/system/hello-server.service",
      "echo 'After=docker.service' | sudo tee -a /etc/systemd/system/hello-server.service",
      "echo '' | sudo tee -a /etc/systemd/system/hello-server.service",
      "echo '[Service]' | sudo tee -a /etc/systemd/system/hello-server.service",
      "echo 'ExecStart=/usr/bin/docker run --rm -p 80:8080 irayspace/hello-server' | sudo tee -a /etc/systemd/system/hello-server.service",
      "echo 'Restart=always' | sudo tee -a /etc/systemd/system/hello-server.service",
      "echo '' | sudo tee -a /etc/systemd/system/hello-server.service",
      "echo '[Install]' | sudo tee -a /etc/systemd/system/hello-server.service",
      "echo 'WantedBy=multi-user.target' | sudo tee -a /etc/systemd/system/hello-server.service",

      # Enable and start service on boot
      "sudo systemctl daemon-reexec",
      "sudo systemctl daemon-reload",
      "sudo systemctl enable hello-server.service"
    ]
  }
}