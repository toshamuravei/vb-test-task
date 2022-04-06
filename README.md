# vb-test-task
Simple aiohttp-based web api with db for so-called Vehicle Builder service

Current back-end uses aiohttp as web-framework and PostgreSQL as database. 

Backend structure could be displayed like this: 

```bash
├── api
│   ├── exceptions.py      - Errors & exceptions
│   ├── handlers.py        - Request handlers also called "views"
│   ├── __init__.py
│   ├── responses.py       - Custom Response-based classes 
│   ├── routes.py          - URLs & their bindings with handlers
│   └── services           - Service-logic module
│       ├── __init__.py
│       ├── raw_queries.py - Raw SQL queries and related query column names
│       └── vehicle.py     - Service class which handles vehicle-related requests
├── app.py
├── config
│   ├── __init__.py
│   └── main.py
├── db
│   ├── alembic_imports.py - Import proxy file to avoid import path conflicts
│   ├── base.py            - Declarative base class
│   ├── __init__.py
│   ├── models.py
│   └── session.py
├── __init__.py
└── middlewares
    ├── db_session.py      - Middleware inserting db session into requests
    └── __init__.py
```

#### Project could be started with simply:
```bash
cd project-path
docker-compose -f docker/docker-compose.local.yaml up
```

Service implements single RESTful http request, that could be performed from any http-client, e.g. from a web-browser:
```http://localhost:8080/api/vehicles/1```

#### Database scheme generated with pgAdmin4:
![alt text](https://github.com/toshamuravei/vb-test-task/blob/main/db_scheme.png)
