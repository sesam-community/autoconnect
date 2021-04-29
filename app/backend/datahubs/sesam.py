import requests
import logging
import json


def create_system(connection_params, sesam_jwt, sesam_base_url):
    return_msg = None
    header = {
        'Authorization': f'Bearer {sesam_jwt}',
        "content-type": "application/json"
    }

    system = {
        "_id": f"{connection_params['dbName'].replace('_', '-')}",
        "type": f"system:{connection_params['dbase']}",
        "database": f"{connection_params['dbName']}",
        "username": f"{connection_params['dbUser']}",
        "password":
        f"$SECRET({connection_params['dbName'].replace('_', '-')}-password)",
        "host": f"{connection_params['dbHost']}",
        "port": int(connection_params['dbPort'])
    }

    sesam_response = requests.post(f"{sesam_base_url}/systems?force=True",
                                   headers=header,
                                   data=json.dumps([system]),
                                   verify=False)
    if not sesam_response.ok:
        print(sesam_response.content)
        return_msg = "Failed"
    else:
        print(
            f"System '{connection_params['dbName'].replace('_', '-')}' has been created"
        )
        return_msg = "Your system has been created"

    json_secret = {
        f"{connection_params['dbName'].replace('_', '-')}-password":
        f"{connection_params['dbPassword']}"
    }
    sesam_secret_response = requests.post(
        f"{sesam_base_url}/systems/{system['_id']}/secrets?",
        headers=header,
        data=json.dumps(json_secret),
        verify=False)
    if not sesam_secret_response.ok:
        print(sesam_secret_response.content)
    else:
        print(f"System secret has been added")

    return return_msg

def create_pipe_with_fkey_ni(connection_params, list_with_table_relations,
                        sesam_jwt, sesam_base_url):
    return_msg = None
    pipes = {}
    header = {
        'Authorization': f'Bearer {sesam_jwt}',
        "content-type": "application/json"
    }

    tmp_dict = {}
    for table in list_with_table_relations:
        if table[0] in tmp_dict:
            tmp_dict[table[0]].append([
                "make-ni",
                    f"{connection_params['dbase'].replace('_', '-')}-{table[2].replace('_', '-')}",
                    f"{table[1]}"
            ])
        else:
            tmp_dict = {
                table[0]: [[
                "make-ni",
                    f"{connection_params['dbase'].replace('_', '-')}-{table[2].replace('_', '-')}",
                    f"{table[1]}"
            ]]
            }

        pipe = {
            "_id":
            f"{connection_params['dbase']}-{table[0].replace('_', '-')}",
            "type": "pipe",
            "source": {
                "type": "sql",
                "system": f"{connection_params['dbName'].replace('_', '-')}",
                "table": f"{table[0]}"
            },
            "transform": {
                "type": "dtl",
                "rules": {
                    "default": [
                        ["copy", "*"],
                        [
                            "add", "rdf:type",
                            [
                                "ni",
                                f"{connection_params['dbase']}-{table[0].replace('_', '-')}",
                                f"{table[0].replace('_', '-')}"
                            ]
                        ],
                    ] + tmp_dict[table[0]]
                }
            }
        }

        pipes[pipe["_id"]] = pipe

    pipes = list(pipes.values())

    for pipe in pipes:
        sesam_response = requests.post(f"{sesam_base_url}/pipes",
                                       headers=header,
                                       data=json.dumps([pipe]),
                                       verify=False)
        if not sesam_response.ok:
            print(sesam_response.content)
        else:
            print(f"Pipe '{pipe['_id']}' has been created")
            return_msg = "Pipes created"

    return return_msg

def create_pipe_with_idx_ni(connection_params, list_with_table_relations,
                        sesam_jwt, sesam_base_url):
    return_msg = None
    pipes = {}
    header = {
        'Authorization': f'Bearer {sesam_jwt}',
        "content-type": "application/json"
    }

    tmp_dict = {}
    for table in list_with_table_relations:
        pipe_id = list(table[0].keys())[0]
        pipe_id_column = list(table[0].values())[0]
        pipe_idx_table = list(table[1].keys())[0]
        pipe_idx_column = list(table[1].values())[0]
        
        if pipe_id in tmp_dict:
            tmp_dict[pipe_id].append([
                    "make-ni",
                    f"{connection_params['dbase']}-{pipe_idx_table.replace('_', '-')}",
                    f"{pipe_id_column}"
            ])
        else:
            tmp_dict = {
                pipe_id : [[
                    "make-ni",
                    f"{connection_params['dbase']}-{pipe_idx_table.replace('_', '-')}",
                    f"{pipe_id_column}"
                ]]
            }

        pipe = {
            "_id":
            f"{connection_params['dbase']}-{pipe_id.replace('_', '-')}",
            "type": "pipe",
            "source": {
                "type": "sql",
                "system": f"{connection_params['dbName'].replace('_', '-')}",
                "table": f"{pipe_id}"
            },
            "transform": {
                "type": "dtl",
                "rules": {
                    "default": [
                        ["copy", "*"],
                        [
                            "add", "rdf:type",
                            [
                                "ni",
                                f"{connection_params['dbase']}-{pipe_id.replace('_', '-')}",
                                f"{pipe_id.replace('_', '-')}"
                            ]
                        ],
                    ] + tmp_dict[pipe_id]
                }
            }
        }

        pipes[pipe["_id"]] = pipe

    pipes = list(pipes.values())
    
    for pipe in pipes:
        sesam_response = requests.post(f"{sesam_base_url}/pipes",
                                       headers=header,
                                       data=json.dumps([pipe]),
                                       verify=False)
        if not sesam_response.ok:
            print(sesam_response.content)
        else:
            print(f"Pipe '{pipe['_id']}' has been created")
            return_msg = "Pipes created"

    return return_msg

def create_pipe(connection_params, tables, sesam_jwt, sesam_base_url):
    return_msg = None
    pipes = []
    header = {
        'Authorization': f'Bearer {sesam_jwt}',
        "content-type": "application/json"
    }
    for table in tables:
        pipe = {
            "_id": f"{connection_params['dbase']}-{table.replace('_', '-')}",
            "type": "pipe",
            "source": {
                "type": "sql",
                "system": f"{connection_params['dbName'].replace('_', '-')}",
                "table": f"{table}"
            },
            "transform": {
                "type": "dtl",
                "rules": {
                    "default":
                    [["copy", "*"],
                     [
                         "add", "rdf:type",
                         [
                             "ni",
                             f"{connection_params['dbase']}-{table.replace('_', '-')}",
                             f"{table.replace('_', '-')}"
                         ]
                     ]]
                }
            }
        }
        pipes.append(pipe)

    for pipe in pipes:
        sesam_response = requests.post(f"{sesam_base_url}/pipes",
                                       headers=header,
                                       data=json.dumps([pipe]),
                                       verify=False)
        if not sesam_response.ok:
            print(sesam_response.content)
        else:
            print(f"Pipe '{pipe['_id']}' has been created")
            return_msg = "Pipes created"

    return return_msg

def get_all_input_pipes(sesam_jwt, sesam_base_url):
    pipe_names = []
    header = {
        'Authorization': f'Bearer {sesam_jwt}',
        "content-type": "application/json"
    }
    sesam_response = requests.get(f"{sesam_base_url}/pipes",
                                  headers=header,
                                  verify=False)

    if not sesam_response.ok:
        return "Could not fetch pipes from Sesam"

    else:
        for pipe in sesam_response.json():
            if "endpoint" in pipe['_id'] or "output" in pipe[
                    '_id'] or "outgoing" in pipe[
                        '_id'] or "preparation" in pipe[
                            '_id'] or "enrich" in pipe['_id']:
                pass
            else:
                pipe_names.append(pipe['_id'])

    return pipe_names

def create_global(global_name, selected_pipes, sesam_jwt, sesam_base_url):
    return_msg = None
    header = {
        'Authorization': f'Bearer {sesam_jwt}',
        "content-type": "application/json"
    }
    global_pipe = {
        "_id": f"{global_name}",
        "type": "pipe",
        "source": {
            "type": "merge",
            "datasets": selected_pipes,
            "identity": "first",
            "strategy": "default",
            "version": 2
        },
        "metadata": {
            "global": True,
            "tags": [f"{global_name.split('-')[1]}"]
        },
    }

    sesam_response = requests.post(f"{sesam_base_url}/pipes",
                                   headers=header,
                                   data=json.dumps([global_pipe]),
                                   verify=False)
    if not sesam_response.ok:
        response = json.loads(sesam_response.content.decode('utf-8-sig'))
        if response['detail'] == f"The pipe '{global_name}' already exists!":
            print(f'Trying to update config of {global_name}...')
            sesam_second_response = requests.put(f"{sesam_base_url}/pipes/{global_name}/config",
                                   headers=header,
                                   data=json.dumps(global_pipe),
                                   verify=False)
            if not sesam_second_response.ok:
                print(sesam_second_response.content)
            
            else:
                print(f"Pipe '{global_pipe['_id']}' has been updated")
                return_msg = "Global updated"
    
    else:
        print(f"Pipe '{global_pipe['_id']}' has been created")
        return_msg = "Global created"

    return return_msg

def get_all_pipes(sesam_jwt, sesam_base_url):
    pipe_names = []
    header = {
        'Authorization': f'Bearer {sesam_jwt}',
        "content-type": "application/json"
    }
    sesam_response = requests.get(f"{sesam_base_url}/pipes",
                                  headers=header,
                                  verify=False)

    if not sesam_response.ok:
        err_msg = ["Could not fetch pipes from Sesam.", "Make sure your provided URL and JWT are valid and try again by refreshing."]
        return err_msg

    else:
        for pipe in sesam_response.json():
            pipe_names.append(pipe['_id'])

    return pipe_names

def get_global_pipe_config(global_pipe, sesam_jwt, sesam_base_url):
    pipes_in_global = []
    header = {
        'Authorization': f'Bearer {sesam_jwt}',
        "content-type": "application/json"
    }
    sesam_response = requests.get(f"{sesam_base_url}/pipes/{global_pipe}/config",
                                  headers=header,
                                  verify=False)

    if not sesam_response.ok:
        err_msg = ["Could not fetch pipes from Sesam.", "Make sure your provided URL and JWT are valid and try again by refreshing."]
        return err_msg

    else:
        json_config = json.loads(sesam_response.content.decode('utf-8-sig'))
        datasets = json_config['source']['datasets']
        for element in datasets:
            pipes_in_global.append(element.split(' ')[0])

    return pipes_in_global