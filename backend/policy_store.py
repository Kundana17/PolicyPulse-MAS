# policy_store.py
from qdrant_client_local import getModel, setupCollection, getClient
from qdrant_client.models import PointStruct

COLLECTION = "policy_memory"

def setupPolicyCollection():
    setupCollection(COLLECTION)

def storePolicy(policy):
    model = getModel()
    client = getClient() # Get the singleton instance
    vector = model.encode(policy["text"]).tolist()
    point = PointStruct(
        id=int(policy["id"]),
        vector=vector,
        payload=policy
    )
    client.upsert(collection_name=COLLECTION, points=[point])