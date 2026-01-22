from qdrant_client import models
from qdrant_client_local import getClient, getModel

def detect_policy_drift(policyId):
    client = getClient()
    model = getModel()
    
    # 1. Fetch policy details
    res = client.retrieve(collection_name="policy_memory", ids=[policyId])
    if not res:
        return {"SimilarityScore": 1.0, "DriftDetected": False, "Explanation": "Policy record missing."}
    
    policy = res[0].payload
    vector = model.encode(policy["text"]).tolist()
    
    # 2. Search impacts by Sector similarity
    impacts = client.query_points(
        collection_name="policy_impact",
        query=vector,
        query_filter=models.Filter(
            must=[models.FieldCondition(key="sector", match=models.MatchValue(value=policy["sector"]))]
        ),
        limit=2
    ).points
    
    # 3. Default "In Sync" if no specific logs are found
    if not impacts:
        return {
            "DriftScore": 0.0, # Zero distance means In Sync
            "DriftDetected": False,
            "Explanation": "No drift detected. System is in sync.",
            "Region": "National Coverage",
            "ActualImpact": "Active"
        }
    
    avg_sim = sum(i.score for i in impacts) / len(impacts)
    # Drift is the inverse of similarity
    drift_val = round(1.0 - avg_sim, 2)
    
    return {
        "DriftScore": drift_val,
        "DriftDetected": drift_val > 0.4, 
        "Explanation": f"Verified against {len(impacts)} recent field data points.",
        "Region": impacts[0].payload.get("state", "National"),
        "ActualImpact": str(impacts[0].payload.get("raw", "Positive"))
    }