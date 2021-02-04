#import cx_Oracle
from queries.oracle import *


def connect_to_db(connecting_params, option):
    return_object = []
    cursor = None
    cx_Oracle.init_oracle_client(
        lib_dir="/oracle-instantclient/instantclient_12_1")
    try:
        dsn_tns = cx_Oracle.makedsn(
            connecting_params['dbHost'],
            connecting_params['dbPort'],
            service_name=connecting_params['dbName']
        )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
        conn = cx_Oracle.connect(
            user=connecting_params['dbUser'],
            password=connecting_params['dbPassword'],
            dsn=dsn_tns
        )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
        cursor = conn.cursor()

    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)

    cursor.execute(
        tables_and_columns(connecting_params['dbName'])
    )  # use triple quotes if you want to spread your query across multiple lines
    for row in cursor:
        return_object.append(row)
        print(
            row[0], '-', row[1]
        )  # this only shows the first two columns. To add an additional column you'll need to add , '-', row[2], etc.

    conn.close()
    cursor.close()

    return return_object