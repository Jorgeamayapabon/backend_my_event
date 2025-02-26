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
# Clonar backend como ec2-user
sudo -u ec2-user bash << 'EOT'
    cd /home/ec2-user
    git clone https://github.com/Jorgeamayapabon/backend_my_event.git
    cd backend_my_event
    # Crear archivo .env con variables de entorno
    cat > .env <<EOF
        # DB Config
        PSQL_USERNAME=XXXX
        PSQL_PASSWORD=XXXX
        PSQL_HOST=XXXX
        PSQL_PORT=XXXX
        PSQL_DB=XXXX

        # JWT Config
        SECRET_KEY=XXXX
        ALGORITHM=XXXX
    EOF
    docker-compose up --build -d
EOT

# Confirmar finalización
echo "User Data script finalizado correctamente" >> /home/ec2-user/user_data.log
