# Boilerplate to initiate Django project


[Django](https://www.djangoproject.com/) project template that we will use at [Emumba](https://www.emumba.com/).

Best suited for medium-sized and bigger apps.

 

## Features

- Django-based backend

    - [Django](https://www.djangoproject.com/)
    - Control settings through environment variables
    - Python 3.6 or later
    - Django 3.1.3
    - Django Rest Framework 3.12.1
    - Redis 3.5.3 
    - Sentry SDK 0.19.2
    


- Batteries

    - Docker / Docker Compose integration
    - Linting of Python code with [pylint](https://github.com/pycqa/pylint) and [flake8](https://pypi.org/project/flake8/)
    - Static type checker for Python using [mypy](https://mypy.readthedocs.io/en/stable/getting_started.html) 
    - [py.test](http://pytest.org/) and [coverage](https://coverage.readthedocs.io/) integration
 

## Project Setup

To use this template, first ensure that you have
[virtualenv](https://naysan.ca/2019/08/05/install-python-3-virtualenv-on-ubuntu/)  available.

After that, you should:
1. Create and activate a virtual environment
    ```
    virtualenv -p python3 my_env
    source my_env/bin/activate 
    ```
2. Navigate to the directory where you cloned the project:
    ```
    cd /home/my-projects/
    ```

3. Install the requirements by running
    ```
    sh tools/install_requirements.sh
    ```
4. Set the environment variable
    ```
   create a .env file
   clone the env.example into .env file
   set the value of the environment variable
    ```
   Note: **you should set environment variables for your development environment**



 
## Docker images
- documents will update soon

**Project CI Image**

- documents will update soon


**Template CI Image:**
- documents will update soon
