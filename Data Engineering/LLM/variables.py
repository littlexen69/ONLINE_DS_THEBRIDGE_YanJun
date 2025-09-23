import os
from dotenv import load_dotenv

load_dotenv()

os.getenv("KEY_GROQ")

config = {
    "host":os.getenv("DB_HOST"),
    "user":os.getenv("DB_USER"),
    "password":os.getenv("DB_PASSWORD"),
    "port":int(os.getenv("DB_PORT")),
    "dbname": os.getenv("DB_NAME")
}