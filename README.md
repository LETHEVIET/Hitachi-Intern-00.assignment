
# 00.Assignment: Develop a FastAPI back-end application
## Run FastAPI server with PostgreSQL Database
To run the server, execute the below command in the terminal
```shell
docker compose up
```

## Application Structure
```
backend/ <== Root folder
|-- alembic/ <== Database migration folder
| |-- versions/
| `-- env.py
|-- apis/ <== Endpoints layer, defines endpoints and related
| |-- __init__.py interfaces with outside
| |-- drivers.py
| |-- sessions.py
| `-- vehicles.py
|-- ctrl/ <== Controllers layer, defines logic and
| |-- __init__.py interactions with database
| |-- drivers.py
| |-- sessions.py
| `-- vehicles.py
|-- db/ <== Database layer
| |-- models/ <== SQLAlchemy model definitions
| | |-- __init__.py
| | |-- driver.py
| | |-- session.py
| | `-- vehicle.py
| |-- schemas/ <== Pydantic schemas for validation
| | |-- __init__.py
| | |-- driver.py
| | |-- session.py
| | `-- vehicle.py
| `-- database.py <== Database initialization and connection handling
|-- alembic.ini
|-- configs.py <== Configuration settings for the application
|-- exceptions.py <== Custom exception classes
`-- main.py <== Entry point for the FastAPI application
```
