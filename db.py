import os
import psycopg2 #type: ignore
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

conn.autocommit = True
cursor = conn.cursor()


# For start Server 17 of PostGreSQL 

"""
& "C:\Program Files\PostgreSQL\17\bin\pg_ctl.exe" `
-D "C:\Postgres17Data" `
-l "C:\Postgres17Data\postgres.log" `
start
"""

# To connect with thor_chatbot Data Base

"""
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" `
-U AB00123 `
-d thor_chatbot `
-p 5433
"""