from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "company_db")
DB_USER = os.getenv("DB_USER", "company_admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "test1234!")
DB_PORT = os.getenv("DB_PORT", 5432)
