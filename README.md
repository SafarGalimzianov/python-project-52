### Hexlet tests and linter status:
[![Actions Status](https://github.com/SafarGalimzianov/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/SafarGalimzianov/python-project-52/actions)

### Test Coverage and Mainatinability
[![Test Coverage](https://api.codeclimate.com/v1/badges/1974c5bee55064ade7ef/test_coverage)](https://codeclimate.com/github/SafarGalimzianov/python-project-52/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/1974c5bee55064ade7ef/maintainability)](https://codeclimate.com/github/SafarGalimzianov/python-project-52/maintainability)
___

### Problem

Users of Hexlet (students) struggle to keep up with their studying schedules
For example, according to the inner research,  numerous students forget about their tasks.
In order to help the students achieve their goals, I decided to create the task-management web-service (service) to create and follow tasks.
___

### Requirements

#### Availability
- Everyone on the Internet should be able to visit the service at any time
- Registered users should have the same access to the service as everyone else

#### Functionality
- Everyone on the Internet should be able to view tasks and users associated with them and register via name and password
- Registered users should be able to do as everyone else and also create tasks, categorise them (tag them)

#### Design
- The service HTML templates should not include scripts and CSS, but only HTML5 and Bootstrap5
- The language of the service should be English
- The footer of each page of the service should include link to the Hexlet: https://hexlet.io
- The service design should follow modern soft corporate style

#### Other
- The service deployment deadline is 16 February 2025
- The service should be deployed on PaaS
- The service should load each page in at least 3 seconds
- The service's interface should be user-friendly
- The project is based on Python (3.10+), Django (5.0+) PostgreSQL (16+) (remote DB) and SQLite (3.4+) (local DB for development)
___

### Architecture

#### Structure
This is a project that solves a problem not related with high loads, important data and the problem will not get more complex in the future.
That's why the structure is concise and mostly based on basic Django functionality.
The Django project includes no static files and only one application Tasks to create, edit and delete tasks.
Other views related functionality is handled by functions in views.py in the project's root directory.

#### Data
The project's communication with database is handled by DBRepository (SQL queries) and DBPool (connection pool) classes.
DB contains tables USERS (data from registation form) and TASKS (everything else).

#### Security
The security of users' data is handled by default Django functionality.
The connection to DB is secured by storing required credentials on a local machine.

#### Errors
The errors related with users actions are forgived and simply shown to the user, except for data provided in the registration form.

#### Performance and stability
There are no special methods to boost performance and stability is ensured by the simplicity of the project.
___