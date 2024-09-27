from peewee import PostgresqlDatabase
from dotenv import load_dotenv
import os

load_dotenv()

# print(os.getenv("DATABASE_NAME"))
# print(os.getenv("USERNAME"))
# print(os.getenv("PASSWORD"))
# print(os.getenv("HOST"))

handler = PostgresqlDatabase(
    database="IntelligentAssistant",
    user="postgres", 
    password="hjQ45dm9",
    host="localhost",
)