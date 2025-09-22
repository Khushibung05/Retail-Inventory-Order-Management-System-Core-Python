# src/config.py
'''import os
from dotenv import load_dotenv
from supabase import create_client, Client
 
load_dotenv()  # loads .env from project root
 
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
 
def get_supabase() -> Client:
    """
    Return a supabase client. Raises RuntimeError if config missing.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment (.env)")
    return create_client(SUPABASE_URL, SUPABASE_KEY)
 '''
# src/config.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()  # loads .env from project root


class SupabaseConfig:
    """Singleton-style access to Supabase client."""

    _client: Client | None = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._client is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            if not url or not key:
                raise RuntimeError(
                    "SUPABASE_URL and SUPABASE_KEY must be set in environment (.env)"
                )
            cls._client = create_client(url, key)
        return cls._client
