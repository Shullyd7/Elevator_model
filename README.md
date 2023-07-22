# Elevator System

## Introduction

This README provides a detailed overview of the Elevator System API, which is designed to simulate a simplified elevator model. The API is implemented using Python and Django, with the Django Rest Framework (DRF) to handle Models, ViewSets, Serializers, and other functionalities.

## Table of Contents

1. [Design Decisions](#design-decisions)
2. [Architecture](#architecture)
3. [Repository File Structure](#repository-file-structure)
4. [Database Modeling](#database-modeling)
5. [API Contracts](#api-contracts)
6. [Setup, Deployment, and Testing](#setup-deployment-and-testing)
7. [Postman Collection](#postman-collection)

## Design Decisions

The Elevator System API is designed to manage and control a fleet of elevators. The primary design decisions include:

1. **Simplified Elevator Model**: The elevator system is a simplified model with basic capabilities, including moving up and down, opening and closing doors, starting and stopping, and handling user requests.

2. **Single Button per Floor**: The elevator system is designed with only one button per floor for simplicity.

3. **Immediate API Reflectance**: API calls to make the elevator go up, down, or stop are assumed to reflect immediately.

4. **Optimal Elevator Assignment**: The system is designed to assign the most optimal elevator to users based on their request floor.

5. **Immediate Response**: The API responses are structured to provide easy integration and make sense at a glance.

6. **Database Storage**: The system uses SQLite (for development purposes in Django).

## Architecture

The Elevator System API is built using the Django web framework, following the Model-View-Controller (MVC) architecture. The Django Rest Framework (DRF) is utilized to create a RESTful API with ViewSets and Serializers.

## Repository File Structure

The repository follows a standard Django project structure. Here are the main directories:

```
elevator_system/
  |- elevators/          # Django app containing the Elevator System API
      |- migrations/     # Database migrations
      |- serializers.py  # DRF serializers for model objects
      |- views.py        # ViewSets for API endpoints
      |- models.py       # Database models
  |- elevator_system/     # Django project settings
  |- manage.py            # Django management script
  |- Elevators.postman_collection.json            # Postman Collection
  |- README.md            # Project README
```

## Database Modeling

The Elevator System API has two main models: `Elevator` and `ElevatorRequest`.

1. **Elevator**: Represents an elevator in the system with attributes like `floor`, `direction`, `is_moving`, `is_operational`, and `is_door_open`.

2. **ElevatorRequest**: Represents user requests for an elevator with a `floor` attribute.

The `ElevatorRequest` model is related to the `Elevator` model using a foreign key, representing that each request belongs to an elevator.

## API Contracts

The Elevator System API provides the following endpoints and their functionalities:

1. `POST /elevators/`: Initialize the elevator system with 'n' elevators.
2. `GET /num_elevators/`: Fetch the number of elevators in the system.
3. `POST /clear_elevators/`: Clear all initialized elevators from the system.
4. `GET /elevators/<elevator_id>/requests/`: Fetch all requests for a given elevator.
5. `POST /elevators/<elevator_id>/requests/`: Save a user request to the list of requests for an elevator.
6. `GET /elevators/<elevator_id>/destination/`: Fetch the next destination floor for a given elevator.
7. `GET /elevators/<elevator_id>/is_moving/`: Fetch if the elevator is moving up or down currently.
8. `PUT /elevators/<elevator_id>/maintenance/`: Mark an elevator as not working or in maintenance.
9. `PUT /elevators/<elevator_id>/door/open/`: Open the door of an elevator.
10. `PUT /elevators/<elevator_id>/door/close/`: Close the door of an elevator.
11. `POST /elevators/<elevator_id>/requests/clear/`: Clear user requests for a given elevator.

## Setup, Deployment, and Testing

To set up and run the Elevator System API locally, follow these steps:

1. Clone the repository and navigate to the project directory.

2. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the database migrations:

   ```bash
   python manage.py migrate
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

5. The API is now accessible at `http://localhost:8000/`. You can use tools like Postman to test the API endpoints.

## Postman Collection

A Postman collection is provided to facilitate API testing and integration. The collection contains all the API endpoints and their functionalities.

You can import this collection into Postman and use it to test the Elevator System API easily.