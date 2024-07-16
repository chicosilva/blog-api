
# API documentation - ** Blog **

This document presents the basic information of the **API - Blog  **. For more information, contact the developers at [Cards](#4-Cards).

# Version control

| Date       | Version | Description          | Author                    |
|------------|---------|----------------------|---------------------------|
| 02/04/2023 | 0.1.0   | Project creation     | **Francisco de Assis** |

# Summary

1. [Post Overview](#1-Product-Overview)

2. [Endpoint List](#2-Endpoint-List)

3. [Environment Preparation](#3-Environment-Preparation)

4. [Cards](#4-Cards)


# 2. Endpoints List

    URL: http://127.0.0.1:8000/api/schema/swagger-ui/



# 3. Environment Preparation
### Via Local 
1. Clone the api repository:
    ```shell
    git clone git@github.com:chicosilva/blog.git
    ```

2. Create Virtual Env:
    > **_NOTE:_** Install Pip (tool for dependency management and packaging)
    ```shell
    python3 -m venv .venv
    ```

3. install the dependencies:
   > **_NOTE:_** active the virtualenv: source .venv/bin/activate  
    ```shell
    pip install -r requirements.txt
    ```


4. Configure environment variables:
    > **_NOTE:_** A local PostgreSQL database will be required, see the **.env-sample** file.
    ```shell
      create create a file .env and set the variables.
    ``

5. Run the application:
   - create postgres database (using Docker): 
     ```shell
     make localdb
     ```
   - python manage migrate:
     ``` make migrations ```

   - run the application
     ```shell
     make run
     ```

6. For running unit tests locally:
   > **_NOTE:_** run make localdb and use the variable "TESTING=True" and "DATABASE_HOST=localhost" to run unit and integration tests.
   - Console coverage report:
     ```shell
     make test
     ```

### Via docker-compose

1. Requirements
   
   ### Minimum requirements   
   | requirement                                                   | release  |
   |---------------------------------------------------------------|----------|
   | [docker](https://docs.docker.com/get-docker/)                 | 19.03.0+ |
   | [docker-compose](https://github.com/docker/compose/releases/) | 1.26.0+  |

2. Copy the file [.env-sample](.env-sample) to a new file `.env` and set the required values in the environment variables. Then run the containers build:
   ```shell
   docker-compose up --build
   ```

   ### Exposed ports on the host system:
   
   | container             | port |
   |-----------------------|------|
   | blog-app | 8000 |

# 4 Contacts

> Developer:
1. Francisco Silva - chicosilva1@gmail.com
