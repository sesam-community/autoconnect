from flask import Flask, request, jsonify, Response
import json
import requests
import logging
import os
import sys
from datahubs.sesam import create_pipe, create_system, get_all_input_pipes, create_global, create_pipe_with_fkey_ni, create_pipe_with_idx_ni, get_all_pipes, get_global_pipe_config
from processing.mysql import connect_to_db as mysql_db
from processing.oracle import connect_to_db as oracle_db
from processing.postgres import connect_to_db as postgres_db
from processing.mssql import connect_to_db as mssql_db
from flask_cors import CORS, cross_origin
from sesamutils import VariablesConfig, sesam_logger
import urllib3

urllib3.disable_warnings()
app = Flask(__name__)

## Helpers
logger = sesam_logger("Steve the logger", app=app)
CORS(app,
     resources={r"/*": {
         "origins": "*"
     }},
     headers={
         'Access-Control-Request-Headers', 'Content-Type',
         'Access-Control-Allow-Origin'
     })

connecting_params = None
sesam_response = None
datahub_config_and_tables = None
fkey_relations = None
index_relations = None

## Logic for running program in dev
try:
    with open("helpers.json", "r") as stream:
        env_vars = json.load(stream)
        os.environ['sesam_jwt'] = env_vars['sesam_jwt']
        os.environ['sesam_base_url'] = env_vars['sesam_base_url']
        os.environ['backend_url'] = env_vars['backend_url']
except OSError as e:
    logger.info("Using env vars defined in SESAM")

required_env_vars = ['sesam_jwt', 'sesam_base_url', 'backend_url']
optional_env_vars = ["Denmark_is_here"]
sesam_jwt = os.getenv('sesam_jwt')
base_url = os.getenv('sesam_base_url')
backend_url = os.getenv('backend_url')

@app.route('/')
def index():
    output = {
        'service': 'Autoconnect up and running',
        'remote_addr': request.remote_addr
    }

    return jsonify(output)


## Get connection parameters for db connection and saving them to global variable "connecting_params"
@app.route('/connectors', methods=['POST'])
@cross_origin()
def get_connectors():
    global connecting_params
    connectors = request.json
    connecting_params = connectors
    return jsonify({"parameters": "committed"})


## Create dataflow excluding globals and check for fkey_relations or index_relations.
@app.route('/create_dataflow', methods=['POST'])
@cross_origin()
def create_dataflow():
    ## Validating env vars
    config = VariablesConfig(required_env_vars, optional_env_vars)
    if not config.validate():
        sys.exit(1)

    # Variables
    sesam_system_response = None
    sesam_pipe_response = None
    global datahub_config_and_tables
    global sesam_response
    global fkey_relations
    global index_relations
    connectors = request.json
    pipes = connectors['tables']

    #creating system
    sesam_system_response = create_system(connecting_params, sesam_jwt, base_url)
    if sesam_system_response != "Your system has been created":
        sesam_system_response = "Your system could not be created. Make sure your provided SESAM variables are correct"

    #creating pipes with or without relations
    pipes_to_create = []
    for pipe in pipes:
        pipes_to_create.append(pipe['name'])

    remaining_table_relations = []
    if fkey_relations != []:
        for table in pipes_to_create:
            for fkey_table in fkey_relations:
                if table == fkey_table[0]:
                    remaining_table_relations.append(fkey_table)

        for ni_relation in remaining_table_relations:
            if ni_relation[0] in pipes_to_create:
                pipes_to_create.remove(ni_relation[0])

        create_pipe_with_fkey_ni(connecting_params, remaining_table_relations, sesam_jwt, base_url)
        # remaining tables without ni's
        sesam_pipe_response = create_pipe(
            connecting_params, pipes_to_create,
            sesam_jwt,
            base_url)
        if sesam_pipe_response != "Pipes created":
            sesam_pipe_response = "Your pipes could not be created. Make sure your provided SESAM variables are correct"

    if index_relations != []:
        for table in pipes_to_create:
            for fkey_table in index_relations:
                if table == list(fkey_table[0].keys())[0] and list(fkey_table[0].keys())[0] not in remaining_table_relations:
                    remaining_table_relations.append(fkey_table)

        for ni_relation in remaining_table_relations:
            if list(ni_relation[0].keys())[0] in pipes_to_create:
                pipes_to_create.remove(list(ni_relation[0].keys())[0])

        create_pipe_with_idx_ni(connecting_params, remaining_table_relations, sesam_jwt, base_url)
        # remaining tables without ni's
        sesam_pipe_response = create_pipe(
            connecting_params, pipes_to_create,
            sesam_jwt,
            base_url)
        if sesam_pipe_response != "Pipes created":
            sesam_pipe_response = "Your pipes could not be created. Make sure your provided SESAM variables are correct"

    if index_relations == [] and fkey_relations == []:
        sesam_pipe_response = create_pipe(
            connecting_params, pipes_to_create,
            sesam_jwt,
            base_url)
        if sesam_pipe_response != "Pipes created":
            sesam_pipe_response = "Your pipes could not be created. Make sure your provided SESAM variables are correct"

    sesam_response = {
        "sesam_result": "Your system and pipes have been created! ;)"
    }
    return {
        "system_result": sesam_system_response,
        "pipe_result": sesam_pipe_response
    }


## Get initial scan of db, get relations and write to globals [fkey_relations, index_relations]
@app.route('/scan_db', methods=['GET'])
@cross_origin()
def get_db_data():
    global connecting_params
    global fkey_relations
    global index_relations
    fkey_query_relations = None
    index_query_relations = None
    tables = []
    pkeys = []
    option = connecting_params['option']
    connecting_params["dbase"] = connecting_params["dbase"].lower()

    if option[0] == "Foreign Key references" or option == "Foreign Key references":
        option = "Fkey"
    if option[0] == "Index references" or option == "Index references":
        option = "Index"
    
    if connecting_params["dbase"] == "mysql":
        table_result, fkey_query_relations, index_query_relations = mysql_db(
            connecting_params, option)
    if connecting_params["dbase"] == "postgresql":
        table_result, fkey_query_relations, index_query_relations = postgres_db(
            connecting_params, option)
    if connecting_params["dbase"] == "oracle":
        table_result, fkey_query_relations, index_query_relations = oracle_db(
            connecting_params, option)
    if connecting_params["dbase"] == "mssql":
        table_result, fkey_query_relations, index_query_relations = mssql_db(
            connecting_params, option)

    fkey_relations = fkey_query_relations
    index_relations = index_query_relations

    index_value = 1
    for table, pkey in table_result:
        tables.append({"id": index_value, "name": table, "groupId": 1})
        pkeys.append(pkey)
        index_value = index_value + 1

    return {"result": tables, "base_url": f"{backend_url}"}


## General response...
@app.route('/sesam_response', methods=['GET'])
def sesam_result():
    global sesam_response
    return sesam_response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)