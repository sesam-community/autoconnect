import psycopg2
from queries.postgres import *

def connect_to_db(connecting_params, option):
    return_object = []
    temp_object = []
    conn = psycopg2.connect(database=f"{connecting_params['dbName']}",
                            user=f"{connecting_params['dbUser']}",
                            host=f"{connecting_params['dbHost']}",
                            port=f"{connecting_params['dbPort']}",
                            password=f"{connecting_params['dbPassword']}")
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='{connecting_params['dbName']}'"
    )

    rows = cursor.fetchall()
    for row in rows:
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
        for table in temp_object:
            query = get_fkey_relations(table)
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
                            cursor.execute("SAVEPOINT DK_fix")
                            query = get_table_ref_idx(idx[0], key, idx[2], value[0])
                            try:
                                cursor.execute(query)
                                result = cursor.fetchall()
                                if len(result) != 0:
                                    index_relations.append([{idx[0]: idx[2]}, {key : value[0]}])
                            except Exception as e:
                                ##print(f"Failing with error : {e}")
                                cursor.execute("ROLLBACK TO SAVEPOINT DK_fix")

    conn.close()
    return return_object, fkey_relations, index_relations