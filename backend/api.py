import os
import time
import json
from groq import Groq
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommender import recommend_policy
from drift_detector import detect_policy_drift
from pydantic import BaseModel
from qdrant_client_local import DB_PATH

class FeedbackRequest(BaseModel):
    policy_name: str
    state: str
    user_opinion: str


load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",    # React's current port
        "http://127.0.0.1:5174",    # IP equivalent
        "http://localhost:5173",    # Default Vite port (backup)
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    text: str
    sector: str = None

def archivistAgent(query, sector=None):
    return recommend_policy(query, sector)

def auditorAgent(policyId):
    return detect_policy_drift(policyId)

def strategistAgent(intent, impact, drift, sector):
    drift_score = drift.get('DriftScore')
    
    prompt = f"""
    SYSTEM: You are the 'Civic Strategist Agent'.
    CONTEXT:
    - Sector: {sector}
    - Intent: {intent}
    - Impact: {impact}
    - Drift Score: {drift_score} (Scale: 0.0 = No Drift/In Sync, 1.0 = Full Drift/Failure)
    
    TASK:
    1. If Drift Score is near 0.0, explain why the policy is successfully 'In Sync'.
    2. If Drift Score is high, explain the specific gaps causing the drift.
    3. Provide a 'Cross-Jurisdiction' lesson.
    """
    # ... (Keep existing Groq call)
    # Upgraded to Gemini 2.5 Flash
    try:
        # Using Llama 3.3 70B for high-level reasoning
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a policy analyst specializing in Indian governance."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Strategist Error: {str(e)}"

# Updated snippet for api.py
@app.post("/analyze")
async def analyze(req: QueryRequest):
    # This now returns a dictionary: {"policy": ..., "status": ..., "message": ...}
    result_data = archivistAgent(req.text, req.sector)
    
    # 1. Handle "No Results" (Intent Gate)
    if result_data["status"] == "no_results":
        return {
            "policy": None,
            "status": "no_results",
            "message": result_data["message"]
        }
    
    # 2. Extract policy directly (No longer recs[0])
    policy = result_data["policy"]
    
    # 3. Continue Agentic Handoff
    drift = auditorAgent(policy["id"])
    strategy = strategistAgent(
        policy["text"], 
        drift.get("ActualImpact", "N/A"), 
        drift, 
        policy["sector"]
    )
    
    return {
        "policy": policy["title"],
        "status": result_data["status"],
        "message": result_data["message"],
        "analysis": drift,
        "strategy": strategy
    }


@app.post("/feedback")
async def save_feedback(req: FeedbackRequest):
    new_entry = {
        "timestamp": time.time(),
        "policy": req.policy_name,
        "state": req.state,
        "opinion": req.user_opinion
    }
    
    # Read existing data, append, and rewrite as a proper list
    try:
        if os.path.exists("feedback_logs.json"):
            with open("feedback_logs.json", "r") as f:
                data = json.load(f)
        else:
            data = []
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    data.append(new_entry)

    with open("feedback_logs.json", "w") as f:
        json.dump(data, f, indent=4)
        
    return {"status": "success", "message": "Feedback saved."}

@app.get("/system-status")
async def system_status():
    from qdrant_client_local import getClient
    client = getClient()
    
    policies = client.count(collection_name="policy_memory").count
    impacts = client.count(collection_name="policy_impact").count
    
    return {
        "policies_indexed": policies,
        "impacts_indexed": impacts,
        "storage_path": DB_PATH
    }