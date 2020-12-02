def table_pkey(table):
    query = f"""SELECT KU.table_name as TABLENAME,column_name as PRIMARYKEYCOLUMN FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC 
        INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KU ON TC.CONSTRAINT_TYPE = 'PRIMARY KEY' AND TC.CONSTRAINT_NAME = KU.CONSTRAINT_NAME 
        AND KU.table_name='{table}' ORDER BY KU.TABLE_NAME,KU.ORDINAL_POSITION;"""
    return query


def get_fkey_relations():
    query = """SELECT 
            ccu.table_name AS SourceTable
            ,ccu.column_name AS SourceColumn
            ,kcu.table_name AS TargetTable
            ,kcu.column_name AS TargetColumn
        FROM INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE ccu
            INNER JOIN INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc
                ON ccu.CONSTRAINT_NAME = rc.CONSTRAINT_NAME 
            INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu 
                ON kcu.CONSTRAINT_NAME = rc.UNIQUE_CONSTRAINT_NAME  
        ORDER BY ccu.table_name;"""
    return query


def get_index_info():
    query = """SELECT 
            TableName = t.name,
            ColumnName = col.name
        FROM 
            sys.indexes ind 
        INNER JOIN 
            sys.index_columns ic ON  ind.object_id = ic.object_id and ind.index_id = ic.index_id 
        INNER JOIN 
            sys.columns col ON ic.object_id = col.object_id and ic.column_id = col.column_id 
        INNER JOIN 
            sys.tables t ON ind.object_id = t.object_id 
        WHERE 
            ind.is_primary_key = 1 
            AND ind.is_unique = 1
            AND ind.is_unique_constraint = 0 
            AND t.is_ms_shipped = 0 
        ORDER BY 
            t.name, ind.name, ind.index_id, ic.is_included_column, ic.key_ordinal;"""
    return query


def get_table_columns_for_indexing(table):
    query = f"select column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';"
    return query


def get_table_ref_idx(index_table, table, index_column, column):
    sql = f"SELECT * FROM {index_table}, {table} WHERE {index_table}.{index_column} = {table}.{column};"
    return sql