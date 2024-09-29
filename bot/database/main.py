from peewee import PostgresqlDatabase
from dotenv import load_dotenv
import os

load_dotenv()

handler = PostgresqlDatabase(
    database=os.getenv("DATABASE_NAME"),
    user=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
)
