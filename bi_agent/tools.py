"""
Tools for the Business Intelligence agents.
Modified for high-stability JSON output and SQL Server compatibility.
"""

import os
import json
import pandas as pd
from typing import Dict, Any
from dotenv import load_dotenv
from .db_config import create_db_engine, get_schema_info
from .sql_executor import execute_query, validate_sql

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def execute_sql_and_format(sql_query: str) -> str:
    """
    Executes T-SQL and returns a COMPACT, SAFE JSON string.
    Fixes 'Expecting value: line 1 column 1' by ensuring valid JSON is always returned.
    """
    try:
        # 1. Get Credentials
        server = os.getenv("MSSQL_SERVER")
        database = os.getenv("MSSQL_DATABASE")
        username = os.getenv("MSSQL_USERNAME")
        password = os.getenv("MSSQL_PASSWORD")

        if not all([server, database, username, password]):
            return json.dumps({"success": False, "error": "Database credentials missing in .env"})

        # 2. Execute Query
        engine = create_db_engine(server, database, username, password)
        result = execute_query(engine, sql_query)

        if result['success']:
            df = result['data']
            
            # --- CRITICAL FIX FOR JSON ERROR ---
            # Replace NaN/NaT/Null with empty strings because raw NaN breaks JSON parsers
            if df is not None and not df.empty:
                df = df.fillna('')
                # Convert timestamps to strings to prevent serialization errors
                for col in df.select_dtypes(include=['datetime64']).columns:
                    df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
                data_list = df.to_dict(orient='records')
            else:
                data_list = []

            response = {
                'success': True,
                'data': data_list,
                'columns': list(result['columns']) if result['columns'] is not None else [],
                'row_count': int(result['row_count']),
                'error': None
            }
        else:
            # Clean error message to avoid broken quotes in JSON
            clean_error = str(result['error']).replace('"', "'").replace('\n', ' ')
            response = {
                'success': False,
                'data': [],
                'columns': [],
                'row_count': 0,
                'error': clean_error
            }

        engine.dispose()
        
        # Return COMPACT JSON (no indents) to prevent Agent from getting confused
        return json.dumps(response, separators=(',', ':'))

    except Exception as e:
        return json.dumps({
            'success': False, 
            'error': f"Tool internal error: {str(e).replace('"', "'")}"
        }, separators=(',', ':'))


def get_database_schema() -> str:
    """
    Retrieve database schema. Returns a clean string for the Agent to read.
    """
    try:
        server = os.getenv("MSSQL_SERVER")
        database = os.getenv("MSSQL_DATABASE")
        username = os.getenv("MSSQL_USERNAME")
        password = os.getenv("MSSQL_PASSWORD")

        if not all([server, database, username, password]):
            return "Error: Database credentials not configured."

        engine = create_db_engine(server, database, username, password)
        
        # Limit tables to 15 to prevent context window overflow (causes Char 0 error)
        schema_info = get_schema_info(engine, max_tables=15)

        engine.dispose()
        return schema_info

    except Exception as e:
        return f"Error retrieving schema: {str(e)}"