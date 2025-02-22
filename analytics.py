from backend import fetch_interaction_logs

def generate_analytics():
    logs = fetch_interaction_logs()
    total_interactions = len(logs)
    
    return {
        "total_interactions": total_interactions,
        "logs": logs
    }
