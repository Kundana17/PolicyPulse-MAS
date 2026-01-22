import re
from qdrant_client_local import getModel, getClient
from qdrant_client import models
from policy_store import COLLECTION

# Comprehensive list of Indian States/UTs for extraction
INDIAN_STATES = [
    "Andhra Pradesh", "Andhra", "AP", "Andhra Pradseh",
    "Arunachal Pradesh", "Arunachal", "AR",
    "Assam", "AS",
    "Bihar", "BR",
    "Chhattisgarh", "Chhattisgarh", "CG",
    "Goa", "GA",
    "Gujarat", "GJ",
    "Haryana", "HR",
    "Himachal Pradesh", "Himachal", "HP",
    "Jharkhand", "JH",
    "Karnataka", "KA",
    "Kerala", "KL",
    "Madhya Pradesh", "Madhya", "MP",
    "Maharashtra", "MH",
    "Manipur", "MN",
    "Meghalaya", "ML",
    "Mizoram", "MZ",
    "Nagaland", "NL",
    "Odisha", "Orissa", "OD",
    "Punjab", "PB",
    "Rajasthan", "RJ",
    "Sikkim", "SK",
    "Tamil Nadu", "Tamilnadu", "TN",
    "Telangana", "TS",
    "Tripura", "TR",
    "Uttar Pradesh", "UP",
    "Uttarakhand", "UK",
    "West Bengal", "Bengal", "WB",
    "Delhi", "NCT Delhi", "DL",
    "Jammu and Kashmir", "J&K", "JK",
    "Ladakh", "LA",
    "Puducherry", "Pondicherry", "PY"
]


def extract_state(text):
    """Simple regex helper to find state names in the query."""
    for state in INDIAN_STATES:
        if re.search(rf"\b{state}\b", text, re.IGNORECASE):
            return state
    return None

def recommend_policy(query, sector=None):
    model = getModel()
    client = getClient()
    vector = model.encode(query).tolist()
    
    # Identify if the user mentioned a specific state
    requested_state = extract_state(query)

    # 1. ATTEMPT EXACT STATE MATCH
    filt = None
    if requested_state or sector:
        must_conditions = []
        if requested_state:
            must_conditions.append(models.FieldCondition(key="state", match=models.MatchValue(value=requested_state)))
        if sector:
            must_conditions.append(models.FieldCondition(key="sector", match=models.MatchValue(value=sector)))
        filt = models.Filter(must=must_conditions)

    # In recommender.py, replace exact_results = client.search(...) with:

    exact_results = client.query_points(
        collection_name=COLLECTION,
        query=vector,
        query_filter=filt,
        limit=1
    ).points # Note the .points at the end
    
    # High similarity threshold check
    if exact_results and exact_results[0].score > 0.7:
        return {
            "policy": exact_results[0].payload,
            "status": "exact_match",
            "message": f"Found policy for {requested_state or 'National'}."
        }
    
    # Update the fallback section as well:
    fallback_results = client.query_points(
        collection_name=COLLECTION,
        query=vector,
        limit=1
    ).points

    # ADD THIS THRESHOLD CHECK
    if fallback_results and fallback_results[0].score > 0.6: 
        found_state = fallback_results[0].payload.get("state", "National")
        return {
            "policy": fallback_results[0].payload,
            "status": "fallback_match",
            "message": f"That policy in {requested_state or 'your area'} is not available. Here is a similar one from {found_state} region."
        }

    # 3. NO RESULTS AT ALL
    return {
        "policy": None,
        "status": "no_results",
        "message": "no such policy record in the database"
    }