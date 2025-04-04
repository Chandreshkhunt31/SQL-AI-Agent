from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from sqlalchemy.engine import Engine
from fastapi import HTTPException

load_dotenv()
# Load environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
# Create a database engine
engine: Engine = create_engine(DATABASE_URL)

def get_database_schema() -> str:
    """
    Fetch table names and columns from the database schema.
    """
    schema_query = """
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """
    with engine.connect() as connection:
        result = connection.execute(text(schema_query))
        tables = {}
        for row in result:
            table = row.table_name
            column = f"{row.column_name} ({row.data_type})"
            if table not in tables:
                tables[table] = []
            tables[table].append(column)
    
    schema_text = "\n".join([f"{table}: {', '.join(columns)}" for table, columns in tables.items()])
    return schema_text

def execute_query(query: str):
    """Execute the SQL query and return the results."""

    with engine.connect() as connection:
        try:
            result = connection.execute(text(query))
            if query.strip().upper().startswith("SELECT"):
                return [dict(row) for row in result.mappings()]
            return {"message": "Query executed successfully."}
        except Exception as e:
            raise Exception(f"SQL Execution Error: {str(e)}")
        
def validate_sql(query):
    """Basic SQL validation to prevent dangerous queries."""
    restricted_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "GRANT", "REVOKE"]
    for keyword in restricted_keywords:
        if keyword in query.upper():
            raise HTTPException(status_code=400, detail="This operation is not allowed.")
    
    return query