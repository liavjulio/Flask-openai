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
   git clone https://github.com/liavjulio/flask-openai-postgres.git
   cd flask-openai-postgres

2. Build and run the containers:
   #### docker-compose up --build

3. edit the api env file to held your secret openai key.

### Test
To run the tests, use the following command:
#### docker-compose run web pytest

### Run
To run the app , use the following command:
#### curl -X POST http://localhost:8080/ask -H "Content-Type: application/json" -d '{"question": "Enter your question here?"}'
