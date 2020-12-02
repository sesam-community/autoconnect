def table_pkey(table):
    query = f"""SELECT KU.table_name as TABLENAME,column_name as PRIMARYKEYCOLUMN FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC 
        INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KU ON TC.CONSTRAINT_TYPE = 'PRIMARY KEY' AND TC.CONSTRAINT_NAME = KU.CONSTRAINT_NAME 
        AND KU.table_name='{table}' ORDER BY KU.TABLE_NAME,KU.ORDINAL_POSITION;"""
    return query


def get_fkey_relations(table):
    query = f"""SELECT
                    tc.table_name, 
                    kcu.column_name, 
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name 
                FROM 
                    information_schema.table_constraints AS tc 
                    JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                    AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='{table}';"""
    return query
    

def get_index_info():
    query = """SELECT 
            idx.indrelid::regclass as tables,
            idx.indkey,(
            SELECT pg_get_indexdef(idx.indexrelid, k + 1, true)
            FROM generate_subscripts(idx.indkey, 1) as k
            ORDER BY k
            ) as indkey_names
        FROM   pg_index as idx
        JOIN   pg_class as i
        ON     i.oid = idx.indexrelid
        JOIN   pg_am as am
        ON     i.relam = am.oid
        JOIN   pg_namespace as ns
        ON     ns.oid = i.relnamespace
        AND    ns.nspname = ANY(current_schemas(false));"""
    return query


def get_table_columns_for_indexing(table):
    query = f"select column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';"
    return query


def get_table_ref_idx(index_table, table, index_column, column):
    sql = f"SELECT * FROM {index_table}, {table} WHERE {index_table}.{index_column} = {table}.{column} LIMIT 500;"
    return sql