from qdrant_client_local import getClient, setupCollection, getModel

def verify_ingestion():
    client = getClient()
    
    # Check counts
    policy_info = client.get_collection("policy_memory")
    impact_info = client.get_collection("policy_impact")
    
    print("\n--- INGESTION REPORT ---")
    print(f"Policies in Memory: {policy_info.points_count}")
    print(f"Impact Logs in Store: {impact_info.points_count}")

    # Peek at one record to ensure 'state' metadata exists
    sample = client.scroll(collection_name="policy_impact", limit=1)[0]
    if sample:
        print(f"Sample State Tag: {sample[0].payload.get('state')}")
        print(f"Sample Sector Tag: {sample[0].payload.get('sector')}")
    print("------------------------\n")

# verify_ingestion()
if __name__ == "__main__":
    verify_ingestion()