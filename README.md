
# SOLUCION RETO

Se tomó este backend previamente desarrollado en FastAPI y se le agregaron pipelines de CI/CD. Se agregaron workflows para la automatización de la integración con las prácticas DevSecOps. Una vez creados estos reportes, se enviarían a la plataforma de gestión de vulnerabilidades. Se escoge DefectDojo por ser open-source. La plataforma se construye en la instancia clonando el repositorio de DefectDojo. En la automatización de CD, se toma la decisión de utilizar rsync para sincronizar los archivos del repositorio con los de la instancia y posteriormente reiniciar los contenedores.

[Ir a Configuración CI/CD](#setup-cicd)

# Backend My Event

This project is a backend designed for event and session management, implemented with FastAPI and GraphQL (Strawberry). It includes key functionalities such as:

CRUD for events and sessions: Allows you to create, list, update and delete events and their associated sessions.

Database: Integration with SQLAlchemy and SQLModel, supporting engines such as PostgreSQ.

GraphQL: Queries using a modular schema with Strawberry.
Scalability and organization: Architecture ready to be extended with advanced searches (e.g., Elasticsearch) and other optional functionalities.

The system is fully dockerized, which makes it easy to deploy and use in different environments. It also includes a test suite with Pytest to ensure code quality.

## Instalation Local Backend

Clone the project
```bash
  git clone https://github.com/Jorgeamayapabon/backend_my_event.git
```
To run this project, you will need to add environment variables in .env.example.

Create .env file with .env.example

Run the following command to create the containers for the postgresql, celery, flower, redis, Elasticsearch services and the FastAPI project.
```bash
 docker compose up
```

## API Documentation

Go to
```bash
 http://127.0.0.1:8000/docs
```

## SETUP CI/CD

Ve al repo https://github.com/Jorgeamayapabon/backend_my_event
Forkealo y clonalo.

Configura tu aws cli con las credenciales.
```bash
    aws configure
```

Entra al directorio de infrastrucure
```bash
    cd infrastrucure
```

Debemos crear un keyPair en AWS. Vamos a la consola de AWS, entramos a EC2 y creamos un keyPair .pem, lo descargamos, le ponemos el nombre de keyPairTest.pem y lo colocamos en el directorio /infrastrucure

Para aprovisionar infraestructura en aws
```bash
    terraform init
    terraform apply
    yes # Cuando lo solicite
```

Vamos a configurar cada instancia el paso es el mismo para ambas solo que con scripts diferentes. Para el backend y defectdojo los scripts son build_back.sh y build_defectdojo.sh respectivamente.

Primero debemos ingresar a la instancia con el siguiente comando.

```bash
    ssh -i /path/key-pair-name.pem instance-user-name@instance-public-ip
```

Una vez dentro de la instancia, crear un file .sh con el contenido del .sh en el repo. Dale permiso de ejecucion a ese archivo y ejecutalo. Ten en cuenta que el contenido dependera de la instancia en la que te encuentres backend o defectdojo.

En el caso del .sh del back debes modificarlo y cambiar los valores de la linea 31 - 39 con los valores del .env

Una vez hayas corrido ambos scripts necesitas credenciales para defectdojo, dentro de la instancia de defectdojo despues de que hayan pasado 3 minutos de haber corrido el script puedes ver la contraseña de la cuenta de prueba. Hay dos formas.

```bash
    docker-compose logs initializer | grep "Admin password:"
    cat /home/ec2-user/user_data.log #logs del script.sh
```

El usuario es admin y la contraseña. Con esto puedes iniciar sesion en defectdojo. Ingresas a la url http://ip-publica-defectdojo:8080. Inicias sesion. Crear un nuevo producto con el nombre Vulns. Ahi mismo sacas para crear el secreto DEFECTDOJO_API_KEY.

Una vez aprovisionada la infraestructura en AWS creamos los secrests para GitHub Actions

```bash
    BACK_IP # ip publica de la instancia del backend
    DEFECTDOJO_IP # ip publica de la instancia de defectdojo
    DEFECTDOJO_API_KEY # cuando inicies sesion en defectdojo la obtienes
    ENV_FILE # con lo que está en tu .env
    KEY_PEM # el contenido de tu llave .pem
    SSH_USER # el usuario de las instancias por defecto es ec2-user
```

Ya está todo listo es hora de probar. Crea una nueva rama genera un cambio en el codigo del backend. Crear un PR a master y se debe ejecutar los pipelines de security y cuando hagas merge se ejecutan los pipelines de CD para actualizar el codigo en la instancia del backend.
