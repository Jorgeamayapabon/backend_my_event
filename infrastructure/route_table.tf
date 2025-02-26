resource "aws_route_table" "ruta_publica" {
  vpc_id = aws_vpc.vpc_principal.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gateway.id
  }

  tags = {
    Name = "publicRouteTable"
  }
}

resource "aws_route_table_association" "subred_publica1_asociacion" {
  subnet_id      = aws_subnet.subred_publica1.id
  route_table_id = aws_route_table.ruta_publica.id
}

resource "aws_route_table_association" "subred_publica2_asociacion" {
  subnet_id      = aws_subnet.subred_publica2.id
  route_table_id = aws_route_table.ruta_publica.id
}