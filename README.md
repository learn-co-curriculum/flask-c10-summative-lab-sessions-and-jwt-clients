Recipe Planner API

The Recipe Planner API is a robust RESTful backend application built as a collaborative group project by a team of five students for our software engineering curriculum. The platform enables users to manage recipes, categorize ingredients, structure meal plans, and track prep details efficiently through a clean set of JSON endpoints.

Technical Overview & Architecture

The application follows standard Model-View-Controller (MVC) principles for backend development. It uses Flask to handle HTTP routing, SQLAlchemy as the Object-Relational Mapper (ORM) for database interactions, and Alembic for managing database migrations.

Core Features

Complete Recipe Lifecycle (CRUD): Endpoints to create, fetch, modify, and delete recipes along with their ingredients and preparation steps.

Relational Database Design: Structured relational models connecting recipes, ingredients, and categories using foreign key relationships and joint tables where appropriate.

Database Migrations: Controlled database schema versioning using Flask-Migrate and Alembic.

Automated Data Seeding: Built-in script (server/seed.py) to initialize the database with pre-populated dummy data for instant local testing.

Test-Driven Reliability: Comprehensive test coverage written with pytest to validate application routes, status codes, and model validations.

Tech Stack & Tooling

Component

Technology

Description

Language

Python 3.12

Primary development language

Framework

Flask

Lightweight WSGI web application framework

ORM

Flask-SQLAlchemy

SQL toolkit and Object-Relational Mapper

Database

SQLite

Lightweight disk-based database engine

Migrations

Flask-Migrate / Alembic

Database schema migration tool

Dependency Manager

Pipenv

Deterministic package management via Pipfile

Testing Framework

Pytest

Framework for unit and integration testing

Repository Structure

recipe-planner-api/
├── instance/                 # Local SQLite database files
│   └── recipe_planner.db
├── migrations/               # Database migration versions managed by Alembic
│   ├── versions/             # Individual migration script files
│   ├── alembic.ini           # Configuration for Alembic runner
│   └── env.py                # Environment setup for migration scripts
├── server/                   # Main application package
│   ├── tests/                # Automated API route and model tests
│   │   └── test_routes.py    # Test cases for HTTP endpoints
│   ├── __init__.py           # Package initialization
│   ├── app.py                # Flask app instance and API route declarations
│   ├── models.py             # SQLAlchemy database models and schema definitions
│   └── seed.py               # Script for populating test data into the database
├── .gitignore                # Git exclusion rules
├── conftest.py               # Pytest configurations and fixtures
├── Pipfile                   # Project dependencies and environment metadata
└── Pipfile.lock              # Explicit lockfile for dependency resolution



Database Schema & Models

The project uses SQLAlchemy to define the core data models (server/models.py):

Recipe: Stores core recipe metadata including title, description, prep time, cook time, and instructions.

Ingredient: Represents individual food items or components used across multiple recipes.

RecipeIngredient (Association Model): Connects recipes to ingredients with additional quantity and unit attributes (e.g., "2 cups").

API Endpoint Reference

All requests and responses use standard JSON formatting (Content-Type: application/json).

Recipes

Method

Endpoint

Description

Status Codes

GET

/recipes

Retrieve a list of all stored recipes

200 OK

GET

/recipes/<int:id>

Retrieve full details for a single recipe by ID

200 OK, 404 Not Found

POST

/recipes

Create a new recipe entry

201 Created, 400 Bad Request

PATCH

/recipes/<int:id>

Update fields on an existing recipe

200 OK, 400 Bad Request, 404 Not Found

DELETE

/recipes/<int:id>

Remove a recipe entry from the database

204 No Content, 404 Not Found

Getting Started

Prerequisites

Python: Version 3.12 or higher

Pipenv: Installed globally via pip install pipenv

Installation & Local Setup

Clone the repository:

git clone <repository-url>
cd recipe-planner-api



Install project dependencies:

pipenv install



Activate the virtual environment:

pipenv shell



Initialize and seed the database:
Execute the seed script to create all necessary database tables and populate sample data:

python server/seed.py



Run database migrations (Optional / Development):
If you modify models in server/models.py, run:

flask db migrate -m "Describe migration"
flask db upgrade



Start the local server:

python server/app.py



The API will be available at http://127.0.0.1:5000/.

Testing

The project includes an automated test suite located in server/tests/. To execute all tests:

pytest



To view verbose test output:

pytest -v



Authors & Team

Developed collaboratively by a group of five students:

Joseph

Douglas

Erick

Roshow

Alex
