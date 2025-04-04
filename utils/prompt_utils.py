def get_generate_sql_prompt(schema_info: str, nl_query: str) -> str:
    """Generate structured SQL with explanation (Retries up to 3 times)"""

    prompt = f"""
    You are an AI SQL assistant. Given a database schema and a user request, generate a SQL query.
    
    - Use `LIKE` for partial matches.
    - Use `>` and `<` for range conditions.
    - If filtering dates, use `BETWEEN`.
    - If multiple conditions, use `AND` or `OR` correctly.
    - SQL is case-sensitive but query condition should be case-insensitive.
    
    Database schema: 
    {schema_info}

    User request: 
    {nl_query}

    Return only JSON with:
    - `sql_query`: The Generated SQL query.
    """

    return prompt

def get_fix_sql_prompt(schema_info: str, invalid_query: str, error_message: str) -> str:
    """Send invalid SQL to OpenAI for correction."""

    prompt = f"""
    You are an AI SQL assistant. A user-provided SQL query failed due to an error.
    Your job is to fix the SQL query while keeping the user's original intent.

    - Do not remove necessary conditions.
    - Do not change table or column names unless needed.
    - Use `LIKE` for better matches when neccessary.
    - SQL is case-sensitive but query condition should be case-insensitive.

    Database schema:
    {schema_info}

    Invalid SQL query:
    {invalid_query}

    Error message:
    {error_message}

    Return only JSON with:
    - `sql_query`: The corrected SQL query.

    """

    return prompt
