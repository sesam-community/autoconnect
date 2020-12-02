def tables_and_columns(database_name):
    sql = f"SELECT * FROM information_schema.role_column_grants where table_catalog='{database_name}'"
    return sql