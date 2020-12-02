def table_pkey(table):
    query = f"""SELECT KU.table_name as TABLENAME,column_name as PRIMARYKEYCOLUMN FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC 
        INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KU ON TC.CONSTRAINT_TYPE = 'PRIMARY KEY' AND TC.CONSTRAINT_NAME = KU.CONSTRAINT_NAME 
        AND KU.table_name='{table}' ORDER BY KU.TABLE_NAME,KU.ORDINAL_POSITION LIMIT 1;"""
    return query

def get_fkey_relations(db_name, table):
    query = f"""SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = '{db_name}'
            AND REFERENCED_TABLE_NAME = '{table}';"""
    return query
    

def get_index_info(db_name):
    query = f"""SELECT DISTINCT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.STATISTICS WHERE TABLE_SCHEMA = '{db_name}';"""
    return query


def get_table_columns_for_indexing(table):
    query = f"select column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';"
    return query


def get_table_ref_idx(index_table, table, index_column, column):
    sql = f"SELECT * FROM {index_table}, {table} WHERE {index_table}.{index_column} = {table}.{column} LIMIT 500;"
    return sql