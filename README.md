# Autoconnect
A docker-compose microservice that automates the scanning of databases and its table relations.

## Currently autoconnect supports:
Databases [MySQL, PostgreSQL, MsSQL]

## Prerequisites
docker

## API Capabalities
Supports GET, POST

## How to:

*Run program using Docker-compose*

1. Open the docker-compose.yaml file. Fill out the environment section in the backend service defined there. You need to fill in **sesam_jwt** and **sesam_base_url**
    
    - To get your **sesam_base_url**, go into your sesam node via: https://portal.sesam.io/dashboard. When in your node, navigate to the Subscription tab -> Network tab. In the network tab you'll see the "Default URL". That is the URL that should be pasted in **sesam_base_url**.

    - To generate a SESAM JWT navigate to the Subscription tab -> JWT tab. In the JWT tab do as instructed to generate a JWT. Paste the JWT in **sesam_jwt**.

2. Navigate to /app in your terminal. Then run the following:
    ```
    docker-compose build
    ```

    ```
    docker-compose up
    ```

    To gracefully stopping the containers running run *ctrl+c*
    
3. Open your browser and navigate to http://localhost/ and start autoconnecting to your database! 

*Run program for development purposes*

This repo uses the file ```package.json``` and [yarn](https://yarnpkg.com/lang/en/) to run the required commands.

1. Modify the base_url in app/frontend/src/api/index.js and app/frontend/src/components/NewIndex.vue to use http://localhost:5000/.
- Comments will also be present in the respective files.

2. Make sure you have installed yarn.

3. Run backend - from root:
    ```
        yarn install
    ```

4. Run backend - execute to run the script:
    ```
        yarn swagger
    ```

5. Run frontend - from /frontend:
    ```
        yarn dev
    ```

