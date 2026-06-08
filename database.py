import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Muat variabel dari file .env
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
table_name: str = os.getenv("TABLE", "mahasiswa")

if not url or not key:
    raise ValueError("SUPABASE_URL atau SUPABASE_KEY belum diatur di file .env")

# Inisialisasi client Supabase
supabase: Client = create_client(url, key)