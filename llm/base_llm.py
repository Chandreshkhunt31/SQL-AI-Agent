from abc import ABC, abstractmethod
from utils.database_utils import validate_sql, execute_query

class BaseLLM(ABC):
    """
    Abstract base class for LLM providers.
    """

    def get_result(self, nl_query: str) -> str:
        """Get result from natural language query."""

        sql_query_response = self.generate_sql(nl_query)
        if not sql_query_response:
            raise ValueError("SQL query generation failed.")
        sql_query = self.extract_sql_from_response(sql_query_response)
        if not sql_query:
            raise ValueError("SQL query not found in the response.")
        sql_query = validate_sql(sql_query)
        final_result = self.retry_and_fix_sql(sql_query)
        return final_result

    @abstractmethod
    def generate_sql(self, nl_query: str) -> str:
        """
        Generate SQL from natural language query.
        """
        pass

    @abstractmethod
    def fix_invalid_sql(self, invalid_query: str, error_message: str) -> str:
        """
        Fix invalid SQL query based on error message.
        """
        pass
    
    def retry_and_fix_sql(self, query: str, attempt: int = 1) -> str:
        """Retry executing SQL and fix if it fails."""

        if attempt > 3:
            raise ValueError("Failed after maximum attempts.")
        
        try:
            result = execute_query(query)
            return {"result": result}
        except Exception as e:
            fixed_sql_response = self.fix_invalid_sql(query, str(e))
            sql_query = self.extract_sql_from_response(fixed_sql_response)

            if not sql_query:
                raise ValueError("Failed to fix SQL query.")
            
            query = validate_sql(sql_query)
            return self.retry_and_fix_sql(query, attempt + 1)

    @abstractmethod
    def extract_sql_from_response(self, res: str) -> str:
        """
        Extract SQL from response.
        """
        pass