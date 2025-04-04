from .base_llm import BaseLLM
from utils.prompt_utils import get_generate_sql_prompt, get_fix_sql_prompt
from utils.database_utils import get_database_schema, validate_sql, execute_query
import anthropic
import os 
import json
import re
from tenacity import retry, stop_after_attempt, wait_fixed
from dotenv import load_dotenv
load_dotenv()

# Load environment variables
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=anthropic_api_key)

class Anthropic_LLM(BaseLLM):
    """Implementation of LLM using Anthropic."""

    api_key = anthropic_api_key
    model: str = "claude-3-7-sonnet-20250219"
    client = anthropic.Anthropic(api_key=anthropic_api_key)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2)) 
    def generate_sql(self, nl_query: str) -> str:
        """Generate SQL from natural language query."""
        schema_info = get_database_schema()
        prompt = get_generate_sql_prompt(schema_info, nl_query)
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system="You are an AI assistant that generates SQL queries.",
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        
        sql_query_response = response.content[0]
        return sql_query_response
    
    def fix_invalid_sql(self, invalid_query: str, error_message: str) -> str:
        """Fix invalid SQL query based on error message."""
        schema_info = get_database_schema()
        prompt = get_fix_sql_prompt(schema_info, invalid_query, error_message)
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system="You are an AI assistant that generates SQL queries.",
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        
        fixed_sql_response = response.content[0]
        return fixed_sql_response
    
    def extract_sql_from_response(self, response: str) -> str:
        """Extract SQL query from the response."""
        try:
            clean_text = re.sub(r"```json\n|\n```", "", response.text)
            parsed_query_json = json.loads(clean_text)
            query = parsed_query_json.get("sql_query")
            return query
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response.")