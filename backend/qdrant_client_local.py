# qdrant_client_local.py
import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "qdrant_data")

_client = None
_model = None 

def getClient():
    global _client
    if _client is None:
        _client = QdrantClient(path=DB_PATH)
    return _client


def setupCollection(name, size=384):
    client = getClient()
    if not client.collection_exists(name):
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE)
        )

def getModel():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def close_client():
    global _client
    if _client:
        _client.close()
        _client = None

__all__ = ["getClient", "getModel", "close_client", "setupCollection", "DB_PATH"]