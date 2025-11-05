"""Database connection module for Supabase."""

import os
from supabase import create_client, Client
from typing import Optional


class DatabaseConnection:
    """Manages database connection to Supabase."""
    
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        """
        Initialize database connection.
        
        Args:
            url: Supabase project URL (defaults to SUPABASE_URL env var)
            key: Supabase anon key (defaults to SUPABASE_KEY env var)
        """
        self.url = url or os.getenv('SUPABASE_URL')
        self.key = key or os.getenv('SUPABASE_KEY')
        
        if not self.url or not self.key:
            raise ValueError("Supabase URL and key must be provided either as parameters or environment variables")
        
        self.client: Client = create_client(self.url, self.key)
    
    def get_client(self) -> Client:
        """Get Supabase client."""
        return self.client
    
    def execute_sql(self, sql: str) -> dict:
        """
        Execute raw SQL query.
        
        Note: Supabase client doesn't directly support raw SQL execution.
        This method is a placeholder for SQL execution via PostgREST or direct PostgreSQL connection.
        For actual SQL execution, you may need to use psycopg2 or similar.
        """
        # For Supabase, you typically use the client methods instead of raw SQL
        # This is a placeholder that would need to be implemented based on your Supabase setup
        # If you need raw SQL, consider using psycopg2 with the Supabase connection string
        raise NotImplementedError(
            "Raw SQL execution not directly supported by Supabase client. "
            "Use Supabase client methods or connect via psycopg2 for raw SQL."
        )

