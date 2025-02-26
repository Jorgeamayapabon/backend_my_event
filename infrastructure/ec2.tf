resource "aws_instance" "instancia1" {
  ami                         = "ami-01b799c439fd5516a"
  instance_type               = "t3.medium"
  associate_public_ip_address = true
  key_name                    = "keyPairTest"
  subnet_id                   = aws_subnet.subred_publica1.id
  vpc_security_group_ids = [
    aws_security_group.instance_security_group.id
  ]

  tags = {
    Name = "defectdojo"
  }
}

resource "aws_instance" "instancia2" {
  ami                         = "ami-01b799c439fd5516a"
  instance_type               = "t2.micro"
  associate_public_ip_address = true
  key_name                    = "keyPairTest"
  subnet_id                   = aws_subnet.subred_publica2.id
  vpc_security_group_ids = [
    aws_security_group.instance_security_group.id
  ]

  tags = {
    Name = "backend_my_event"
  }
}
