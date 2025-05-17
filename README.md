[![Testing workflow](https://github.com/alisher-nil/task_tracker_test_assignment/actions/workflows/main.yml/badge.svg)](https://github.com/alisher-nil/task_tracker_test_assignment/actions/workflows/main.yml)
![Last Commit](https://img.shields.io/github/last-commit/alisher-nil/task_tracker_test_assignment)

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-FF8C00?style=flat&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-DAA520?style=flat&logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![uv](https://img.shields.io/badge/uv-000000?style=flat&logo=uv&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-000000?style=flat&logo=ruff&logoColor=white)

# Task Tracker API

A simple task tracking API built with Django 5 and Django Rest Framework. This project was developed as a test assignment for a Python developer position.

## Features

- User authentication and authorization using JWT
- CRUD operations for tasks
- Filtering and sorting tasks
- Pagination for task lists
- Comprehensive unit tests for API endpoints

## Tech Stack

- Python 3.13
- Django 5+
- Django Rest Framework
- PostgreSQL
- Docker & Docker Compose
- Pytest for testing

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git
- Python 3.13 (for local development)
- uv package manager (optional, for local development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/alisher-nil/task_tracker_test_assignment.git
   cd task_tracker_test_assignment
   ```

2. Create a `.env` file in the root directory. Example file is provided as `.env.example`. Update the values as needed.
   ```bash
   cp .env.example .env
   ```

3. Run with Docker Compose:
   ```bash
   docker-compose up --build -d
   ```

4. Access the API at `http://localhost:8000/api/`

## API Documentation
All the API endpoints are relative to `/api/`.
### Authentication

- `POST /auth/register/` - Register a new user
- `POST /auth/login/` - Login and get JWT tokens

### Tasks
All endpoints in the tasks section require authentication. Use the JWT token obtained from the login endpoint in the `Authorization` header as `Bearer <token>`.

- `POST /tasks/` - Create a new task
- `GET /tasks/` - List all tasks (supports pagination, filtering, and sorting)
- `GET /tasks/{id}/` - Retrieve a specific task
- `PUT /tasks/{id}/` - Update a task
- `PATCH /tasks/{id}/` - Partially update a task
- `DELETE /tasks/{id}/` - Delete a task

### Filtering and Sorting

- Filter by completion: `GET /tasks/?completed=true` or `false`
- Search by partial match in title: `GET /tasks/?search=keyword`

## Development
### Setup
Create a virtual environment and install dependencies:
```
python -m venv .venv
source .venv/bin/activate # On Windows use `.venv\Scripts\activate`
pip install -r app/requirements.txt
```
or using `uv`:
```bash
uv sync
```
### Running the Development Server
To run the development server, use:
```bash
python app/manage.py runserver
```

### Running Tests
For local testing PostgreSQL server is required. You can run one with provided Docker Compose file in `infra` directory:
```bash
docker-compose -f infra/docker-compose.local.yml up -d
```
With the container running, you can run the tests:
```bash
pytest
```

## CI/CD

The project uses GitHub Actions to automate testing. Check the `.github/workflows` directory for the configuration.
