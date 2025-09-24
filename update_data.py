# update_data.py

import json
import requests
import random
from datetime import datetime

# URL for the trigger endpoint on your running API server
# When testing locally, this is correct.
# IMPORTANT: For deployment, change this to your live Render/server URL.
# In update_data.py
TRIGGER_URL = "https://med-test1-backend.onrender.com/api/trigger-update"
DATA_FILE = "data.json"

def run_update_task():
    """
    Generates new data, saves it to a file, and then notifies the live server.
    """
    print("⚙️  Running scheduled update task...")
    
    # 1. Generate or fetch your new data
    # (Here we use the simulated data from your original request)
    new_data = {
        "active_global_outbreaks": random.randint(240, 290),
        "amr_cases_this_month": random.randint(1800, 2200),
        "critical_health_alerts": [
            {"alert": f"High transmission of new Influenza strain reported at {datetime.now().strftime('%H:%M')} IST."},
            {"alert": "Multi-drug resistant Salmonella reports increasing in central regions."}
        ],
        "reporting_facilities_count": random.randint(15500, 16000),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    }

    # 2. Save the new data to the JSON file
    with open(DATA_FILE, "w") as f:
        json.dump(new_data, f, indent=4)
    print(f"💾  Data saved to '{DATA_FILE}'.")

    # 3. Notify the live server by making a POST request
    try:
        print(f"📡  Notifying live server at {TRIGGER_URL}...")
        response = requests.post(TRIGGER_URL)
        response.raise_for_status() # This will raise an error if the request fails
        print("✅  Server notified successfully. Update pushed to clients.")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not notify server. Is it running? Error: {e}")

if __name__ == "__main__":
    run_update_task()
