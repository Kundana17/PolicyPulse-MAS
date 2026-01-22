import os
import requests
import time
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from data import policies, impacts 
from qdrant_client_local import getClient, setupCollection, getModel, close_client

# 1. LOAD ENVIRONMENT VARIABLES
load_dotenv()
API_KEY = os.getenv("DATA_GOV_API_KEY")

# Configuration (Ensure these 36-character Resource IDs are correct)
RESOURCES = {
    # --- AGRICULTURE ---
    "Agri_Mandi_Prices": "current-daily-price-various-commodities-various-markets-mandi",
    "PM_KISAN_Beneficiaries": "39439683-eb37-49f1-b2e4-0919cf1c7360",
    "Fertilizer_Usage_State": "state-ut-wise-consumption-fertilizers-nitrogen-phosphate-potash",
    "Agri_Infrastructure_Fund": "Starred-Question-Reply-28-03-2025",
    "PM_Fasal_Bima_Claims": "state-ut-wise-details-claims-paid-under-pmfby",

    # --- HEALTHCARE ---
    "Health_Infra_PMABHIM": "e6d8e391-2f91-4d41-8ea9-4a17286a089d",
    "HMIS_Monthly_Indicators": "performance-key-health-management-information-system-hmis-indicators",
    "Health_Staff_Availability": "state-ut-wise-availability-doctors-specialists-community-health-centres",
    "Hospital_Beds_Public": "state-ut-wise-number-government-hospitals-and-beds-rural-and-urban",
    "Maternal_Health_Stats": "state-ut-wise-details-maternal-mortality-ratio-mmr",

    # --- ENERGY ---
    "Renewable_Implementation": "823f4b46-48d4-4cff-b3ba-2656fcf7383b",
    "Solar_Rooftop_Growth": "state-ut-wise-physical-progress-solar-rooftop-programme",
    "Power_Supply_Peak": "state-ut-wise-power-supply-position-energy-and-peak",
    "Village_Electrification": "state-ut-wise-details-villages-electrified-under-deendayal-upadhyaya-gram-jyoti-yojana",

    # --- FINANCE ---
    "State_Revenue_Receipts": "state-wise-total-revenue-receipt-percentage-gsdp",
    "MSME_Daily_Udyam": "social-category-wise-total-micro-small-and-medium-enterprises-msmes",
    "PM_Jan_Dhan_Accounts": "state-ut-wise-number-jan-dhan-accounts-and-deposits",
    "Social_Sector_Spending": "social-allocation-ratio-social-sector-expenditure",
    "Digital_Payments_Volume": "state-ut-wise-digital-transactions-volume-and-value",

    # --- EDUCATION ---
    "Gross_Enrollment_Ratio": "09731bbd-b62d-42f5-8604-bc56625e84e3",
    "Tribal_Edu_Funds_EMRS": "year-wise-details-fund-allocation-under-eklavya-model-residential-school-emrs-scheme",
    "Higher_Edu_AISHE": "state-ut-wise-enrolment-higher-education-aishe",
    "School_Teacher_UDISE": "Teachers-by-Gender-Academic-Qualification-UDISE",

    # --- INFRASTRUCTURE ---
    "Smart_City_Financials": "smart-cities-mission-physical-and-financial-progress",
    "Housing_PMAY_Urban": "aaa29e12-76da-4419-88a1-9641da587cef",
    "Water_Sanitation_JJM": "state-ut-wise-central-fund-allocated-jjm",
    "Road_Accident_Deaths": "state-ut-city-wise-and-place-occurrence-wise-road-accident-deaths"
}

def run_pipeline():
    client = getClient()
    model = getModel()

    print("🚀 Starting PolicyPulse Unified Data Pipeline...")

    # 1. HARD RESET
    # We clear collections to prevent duplicate entries if the script is re-run.
    client.delete_collection("policy_memory")
    client.delete_collection("policy_impact")
    setupCollection("policy_memory")
    setupCollection("policy_impact")

    # 2. LOAD STATIC DATA (200 Policies from data.py)
    print(f"📦 Ingesting {len(policies)} Static Policies...")
    for p in policies:
        # We embed the state/scope directly into the vector for better accuracy.
        text_to_embed = f"Title: {p['title']} | State/Scope: {p['scope']} | Content: {p['text']}"
        vector = model.encode(text_to_embed).tolist()
        
        client.upsert(
            collection_name="policy_memory",
            points=[models.PointStruct(
                id=p["id"], 
                vector=vector, 
                payload={**p, "state": p["scope"]} # Metadata tag for filtering
            )]
        )

    # 3. LOAD LIVE API DATA
    # 3. LOAD LIVE API DATA (OPTIONAL)
        if not API_KEY:
            print("⚠️ DATA_GOV_API_KEY not found. Skipping live data ingestion.")
        else:
            for sector, res_id in RESOURCES.items():
                print(f"📡 Fetching live data for {sector}...")
                url = f"https://api.data.gov.in/resource/{res_id}?api-key={API_KEY}&format=json&limit=50"

        
        success = False
        for attempt in range(3): # Retry up to 3 times
            try:
                # Use a long 60s timeout for heavy road/tribal datasets
                res = requests.get(url, timeout=60)
                
                if res.status_code == 200:
                    records = res.json().get("records", [])
                    print(f"✅ Received {len(records)} records for {sector}.")
                    
                    for i, rec in enumerate(records):
                        # Handle varied state field names across different ministries
                        state = rec.get("state") or rec.get("state_name") or rec.get("state_ut") or "National"
                        text = f"Sector: {sector} | State: {state} | Data: {str(rec)}"
                        
                        vector = model.encode(text).tolist()
                        client.upsert(
                            collection_name="policy_impact",
                            points=[models.PointStruct(
                                id=abs(hash(text + str(i))) % (10**9), 
                                vector=vector,
                                payload={"state": state, "sector": sector, "raw": rec, "type": "live_impact"}
                            )]
                        )
                    success = True
                    break
                else:
                    print(f"⚠️ API returned {res.status_code}. Retrying...")
                    time.sleep(2) # Brief wait before retry
                    
            except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                print(f"⏳ Attempt {attempt + 1} failed (Timeout/Error). Retrying...")
                time.sleep(3)

        if not success:
            print(f"❌ Failed to ingest {sector} after 3 attempts.")

    print("✅ Pipeline Complete: All data sources synchronized.")

if __name__ == "__main__":
    run_pipeline()
    # Explicitly close the connection to prevent "sys.meta_path is None" error
    close_client()