from os import getenv
import os
import sys
import boto3 
from pymongo import MongoClient
from openai import OpenAI
import logging

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

logger = logging.getLogger(__name__)

ENV = getenv("ENV", "local")

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://pranjaljain:6jBbFHiuKtu7n6ve@indiansolarpanel77.nrnnt7p.mongodb.net/")
db_client = MongoClient(MONGO_URI)
db_name = os.getenv("DB_NAME", "solar-dev")
db = db_client[db_name]

# server_url = os.getenv("CALLBACK_URL", "http://localhost:80")

collection = db["users"]
