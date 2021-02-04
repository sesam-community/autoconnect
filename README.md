# Autoconnect
A microservice for making connecting [DATABASE,API,REST,GRAPH] generic

## Currently autoconnect supports:
Databases [MySQL, PostgreSQL, MsSQL]

## Prerequisites
python3, Vue

## API Capabalities
Supports GET, POST

## How to:

*Run program using Docker-compose*

1. Open the docker-compose.yaml file. Fill out the environment section in the backend service defined there. You need to fill in **sesam_jwt** and **sesam_base_url**

2. Navigate to /app in your terminal. Then run the following:
    ```
    docker-compose build
    ```

    ```
    docker-compose up
    ```

    To gracefully stopping the containers running run *ctrl+c*
    
3. Open your browser and navigate to http://localhost/ and start autoconnecting to your database! 

*Run program in development*

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

