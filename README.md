# Flask OpenAI PostgreSQL Project

## Overview

This project is a simple Flask server application that integrates with the OpenAI API to answer questions. The application also stores questions and answers in a PostgreSQL database. Both the server and the database are dockerized and managed with Docker Compose.

## Features

- Flask server with an endpoint to ask questions
- Integration with the OpenAI API for generating answers
- PostgreSQL database for storing questions and answers
- Dockerized application with Docker Compose
- Database migrations using Alembic
- Basic testing with pytest

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository:
   git clone https://github.com/yourusername/flask-openai-postgres.git
   cd flask-openai-postgres
   
2. Create a .env file in the root of the project directory and update it with your OpenAI API key and PostgreSQL database credentials. Use the provided template below:
   #### OpenAI API Key
   OPENAI_API_KEY=your_openai_api_key_here

   #### PostgreSQL Database URL
   DATABASE_URL=postgresql+psycopg2://your_username:your_password@database:5432/your_database_name

   #### PostgreSQL Database Credentials
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database_name

   #### Python Path
   PYTHONPATH=/app:$PYTHONPATH

3. Build and run the containers:
   #### docker-compose up --build
4. Apply Database Migrations
   #### docker-compose run web alembic upgrade head

### Test
To run the tests, use the following command:
docker-compose run web pytest

### Run
To run the app , use the following command:
curl -X POST http://localhost:8080/ask -H "Content-Type: application/json" -d '{"question": "Enter your question here?"}

