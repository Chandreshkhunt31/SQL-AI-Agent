import openai
from .base_llm import BaseLLM
from utils.prompt_utils import get_generate_sql_prompt, get_fix_sql_prompt
from utils.database_utils import get_database_schema, validate_sql, execute_query
import os
import json
import re
from tenacity import retry, stop_after_attempt, wait_fixed
from dotenv import load_dotenv
load_dotenv()
# Load environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

class OpenAI_LLM(BaseLLM):
    """Implementation of LLM using OpenAI."""

    model: str = "gpt-4"
    client = openai.OpenAI(api_key=openai_api_key)
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2)) 
    def generate_sql(self, nl_query: str) -> str:
        """Generate SQL from natural language query."""
        schema_info = get_database_schema()
        prompt = get_generate_sql_prompt(schema_info, nl_query)
        
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system", 
                    "content": [
                        {
                            "type": "text",
                            "text": "You are an AI assistant that can generate SQL queries very efficiently using given table schemas."
                        }
                    ]
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        
        sql_query_response = response.choices[0].message.content
        return sql_query_response
    
    def fix_invalid_sql(self, invalid_query: str, error_message: str) -> str:
        """Fix invalid SQL query based on error message."""
        schema_info = get_database_schema()
        prompt = get_fix_sql_prompt(schema_info, invalid_query, error_message)
        
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system", 
                    "content": [
                        {
                            "type": "text",
                            "text": "You are an AI assistant that can fix SQL queries based on error messages."
                        }
                    ]
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        
        fixed_sql_response = response.choices[0].message.content
        return fixed_sql_response
    
    def extract_sql_from_response(self, response: json) -> str:
        """Extract SQL query from the response."""
        try:
            parsed_query_json = json.loads(response)
            query = parsed_query_json.get("sql_query")
            return query
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response.")