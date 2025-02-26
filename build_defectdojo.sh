#!/bin/bash
set -ex  # Habilita logs detallados y detiene el script si hay errores

# Redirigir salida a un log para depuración
exec > /home/ec2-user/user_data.log 2>&1


# Actualizar paquetes
sudo dnf update -y

# Instalar Docker y Git
sudo dnf install -y docker git
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# Instalar Docker Compose manualmente
DOCKER_COMPOSE_VERSION="v2.27.1"
sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Verificar instalación
docker-compose version

# Clonar DefectDojo como ec2-user
sudo -u ec2-user bash << 'EOT'
cd /home/ec2-user
git clone https://github.com/DefectDojo/django-DefectDojo.git
cd django-DefectDojo
docker-compose build
docker-compose up -d
sleep 200
docker-compose logs initializer | grep "Admin password:"
EOT

# Confirmar finalización
echo "User Data script finalizado correctamente" >> /home/ec2-user/user_data.log
