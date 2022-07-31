# Examples of deploying and hosting a Machine Learning Model with FastAPI

FastAPI is a modern, high-performance, batteries-included Python web framework that's perfect for building RESTful APIs. It can handle both synchronous and asynchronous requests and has built-in support for data validation, JSON serialization, authentication and authorization, and OpenAPI.
It has a lightweight microframework feel with support for Flask-like route decorators.

* It takes advantage of Python type hints for parameter declaration which enables data validation (via pydantic) and OpenAPI/Swagger documentation.
* It supports the development of asynchronous APIs. It's fast. Since async is much more efficient than the traditional 
  synchronous threading model

### Create the environment

From root of repo, run the following command to create a virtual env, activate it and install the main and dev dependencies.
We also export env vars for connecting to db later.

```
$ python3.8 -m venv venv
$ source activate venv/bin/activate
```


```
(venv) $ pip install -r src/requirements.txt
(venv) $ pip install -r src/requirements-dev.txt
```


```
(venv) $ export DATABASE_USER=<username>
(venv) $ export DATABASE_PASSWORD=<password>
```


### Update Tables in DB


```
(venv) $ python -m src.load_data_into_table
```

### 

```
(venv) $ python -m src.app.crud
```