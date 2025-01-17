
# Backend My Event

This project is a backend designed for event and session management, implemented with FastAPI and GraphQL (Strawberry). It includes key functionalities such as:

CRUD for events and sessions: Allows you to create, list, update and delete events and their associated sessions.

Database: Integration with SQLAlchemy and SQLModel, supporting engines such as PostgreSQ.

GraphQL: Queries using a modular schema with Strawberry.
Scalability and organization: Architecture ready to be extended with advanced searches (e.g., Elasticsearch) and other optional functionalities.

The system is fully dockerized, which makes it easy to deploy and use in different environments. It also includes a test suite with Pytest to ensure code quality.

## Instalation

Clone the project
```bash
  git clone https://github.com/Jorgeamayapabon/backend_my_event.git
```
To run this project, you will need to add environment variables in .env.example.

Run the following command to create the containers for the postgresql, celery, flower, redis, Elasticsearch services and the FastAPI project.
```bash
 docker compose up
```

## API Documentation

Go to
```bash
 http://127.0.0.1:8000/docs
```