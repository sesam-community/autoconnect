import pyodbc
from queries.mssql import *

def connect_to_db(connecting_params, option):
    temp_object = []
    return_object = []
    cnxn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        f"Server={connecting_params['dbHost']};"
        f"Port={connecting_params['dbPort']};"
        f"Database={connecting_params['dbName']};"
        f"uid={connecting_params['dbUser']};pwd={connecting_params['dbPassword']}"
    )

    cursor = cnxn.cursor()

    try:
        cursor.execute(
            f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='{connecting_params['dbName']}'"
        )
    except Exception:
        print("SQL Query not working correctly")

    for row in cursor.fetchall():
        temp_object.append(row[0])

    for table in temp_object:
        query = table_pkey(table)
        cursor.execute(query)
        for row in cursor.fetchall():
            return_object.append(row)

    if len(return_object) == 0:
        return_object.append(
            ('Error : Make sure your tabels have a primary key', 'CustomerId'))

    fkey_relations = []
    if option == "Fkey":
        print("finding fKey references")
        query = get_fkey_relations()
        cursor.execute(query)
        for row in cursor.fetchall():
            fkey_relations.append(row)

    index_relations = []
    if option == "Index":
        tmp_relations = []
        print("finding index references")
        query = get_index_info()
        cursor.execute(query)
        for row in cursor.fetchall():
            tmp_relations.append(row)
        
        columns_in_table = []
        list_of_table_and_columns_to_check = []
        for table in return_object:
            query = get_table_columns_for_indexing(table[0])
            cursor.execute(query)
            for row in cursor.fetchall():
                columns_in_table.append(row)

            list_of_table_and_columns_to_check.append({table[0] : columns_in_table})
            columns_in_table = []

        for table in list_of_table_and_columns_to_check:
            for key, values in table.items():
                for idx in tmp_relations:
                    if key !=  idx[0]:
                        for value in values:
                            query = get_table_ref_idx(idx[0], key, idx[1], value[0])
                            try:
                                cursor.execute(query)
                                result = cursor.fetchall()
                                if len(result) != 0:
                                    index_relations.append([{idx[0]: idx[1]}, {key : value[0]}])
                            except Exception as e:
                                pass
                                #print(f"Failing with error : {e}")
    cnxn.close()
    return return_object, fkey_relations, index_relations