provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "vpc_principal" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "mainVpc"
  }
}

resource "aws_subnet" "subred_publica1" {
  vpc_id     = aws_vpc.vpc_principal.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "subredPublica1"
  }
}

resource "aws_subnet" "subred_publica2" {
  vpc_id     = aws_vpc.vpc_principal.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "subredPublica2"
  }
}

resource "aws_security_group" "instance_security_group" {
    name = "instances_sg"
    description = "security group para practicas cloud"
    vpc_id = aws_vpc.vpc_principal.id

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 8000
        to_port = 8000
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 8080
        to_port = 8080
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 3306
        to_port = 3306
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}