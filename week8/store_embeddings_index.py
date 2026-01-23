"""This script generates embeddings for a list of sentences using OpenAI's API"""
import os
import psycopg2
from openai import OpenAI
from constants import Embedding_MODEL
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),  
}


SENTENCES = [
    "PostgreSQL is a powerful open source database.",
    "pgvector enables vector similarity search.",
    "LangChain helps build LLM applications.",
    "Embeddings capture semantic meaning of text."
]

client = OpenAI(api_key=OPENAI_API_KEY)


response = client.embeddings.create(
    model=Embedding_MODEL, 
    input=SENTENCES
)


embeddings = [item.embedding for item in response.data]


conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()


insert_query = """
INSERT INTO sentence_embeddings (sentence, embedding)
VALUES (%s, %s)
"""


for i in range(len(SENTENCES)):
    cur.execute(
        insert_query,
        (SENTENCES[i], embeddings[i])
    )

conn.commit()
cur.close()
conn.close()

print("Embeddings generated and stored successfully in PostgreSQL!")
