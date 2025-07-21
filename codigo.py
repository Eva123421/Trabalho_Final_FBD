# codigo.py
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def conectar():
    return psycopg2.connect(
        host='localhost',
        database='Armazem',
        user='postgres',
        password=os.getenv('BD_PASS'),
        port='5432'
    )


