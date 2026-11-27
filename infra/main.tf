provider "aws" {
  region = "eu-central-1"
}

resource "aws_security_group" "notes" {
  name = "notes-sg"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_key_pair" "notes" {
  key_name   = "notes-key"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_instance" "notes" {
  ami                    = "ami-0a628e1e89aaedf80"
  instance_type          = "t3.micro"
  key_name               = aws_key_pair.notes.key_name
  vpc_security_group_ids = [aws_security_group.notes.id]
  user_data              = "#!/bin/bash\ncurl -fsSL https://get.docker.com | sh"
  tags = { Name = "notes-fastapi" }
}

output "public_ip" {
  value = aws_instance.notes.public_ip
}