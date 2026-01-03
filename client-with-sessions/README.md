# Productivity App Backend

## Description
Flask API with session and JWT authentication that allows users to manage personal notes.

## Setup
pipenv install  
pipenv shell  
flask db upgrade  
python seed.py  

## Run
flask run -p 5555

## Endpoints
POST /signup  
POST /login  
DELETE /logout  
GET /check_session  
GET /notes  
POST /notes  
PATCH /notes/<id>  
DELETE /notes/<id>  
