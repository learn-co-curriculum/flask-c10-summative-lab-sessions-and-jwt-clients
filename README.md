Recipe Planner API

A RESTful backend service built with Flask and SQLAlchemy that allows users to manage recipes, ingredients, and instructions.

Description

This project was built to practice backend development, specifically setting up relational database models, writing REST API endpoints, handling data validation, and running migrations using Flask-Migrate.

Core Features:

Recipe Management: Create, read, update, and delete recipe entries.

Relational Data: Models relationships between recipes and their corresponding ingredients.

Database Migrations: Configured using Alembic and Flask-Migrate for smooth database schema updates.

Automated Testing: Unit and route testing setup with pytest.

Seeding Script: Included pre-populated test data for quick development and verification.

Tech Stack

Language: Python 3.12+

Framework: Flask

ORM: Flask-SQLAlchemy

Database: SQLite

Migrations: Flask-Migrate / Alembic

Testing: Pytest

Environment & Dependency Management: Pipenv

Installation Instructions

Follow these step-by-step instructions to get your development environment running locally.

1. Prerequisites

Ensure you have Python 3 and Pipenv installed on your system.

2. Clone the Repository

git clone <your-repository-url>
cd recipe-planner-api


3. Install Dependencies

Set up the virtual environment and install required packages using Pipenv:

pipenv install


4. Activate the Virtual Environment

pipenv shell


Run Instructions

Follow these steps to initialize the database and run the server.

1. Set Up the Database

Run database migrations to generate the SQLite database schema:

flask db upgrade


2. Seed the Database (Optional)

To populate your database with sample recipes and ingredients:

python server/seed.py


3. Start the Flask Server

Launch the development server:

python server/app.py


The server will start running locally at:
http://127.0.0.1:5000/

API Reference

Endpoints Overview

Method

Endpoint

Description

GET

/recipes

Retrieve a list of all recipes

GET

/recipes/<id>

Retrieve detailed information for a specific recipe

POST

/recipes

Create a new recipe entry

PATCH

/recipes/<id>

Update fields of an existing recipe

DELETE

/recipes/<id>

Remove a recipe from the database

Running Automated Tests

To run the test suite and verify that all endpoints function correctly:

pytest


Project Directory Overview

recipe-planner-api/
│
├── instance/               # SQLite database storage
├── migrations/             # Alembic migration scripts
├── server/
│   ├── app.py              # Application entry point & route definitions
│   ├── models.py           # SQLAlchemy data models
│   ├── seed.py             # Database seed data script
│   └── tests/              # Test suite
│       └── test_routes.py  
├── conftest.py             # Pytest fixtures and setup
├── Pipfile                 # Dependency tracking
└── Pipfile.lock            # Locked dependencies
