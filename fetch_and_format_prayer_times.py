import requests
import json
from datetime import datetime
import os

MASJID_ID = "keLQn7AM"
YEAR = datetime.now().year
API_URL = f"https://masjidal.com/api/v1/time/range?masjid_id={MASJID_ID}&from_date={YEAR}-01-01&to_date={YEAR}-12-31"

def fetch_prayer_times():
    try:
        print("🔄 Fetching data...")
        response = requests.get(API_URL, headers={'User-Agent': 'iOS-App'}, timeout=10)
        response.raise_for_status()
        return response.json()["data"]
    except Exception as e:
        print(f"❌ Fetch failed: {e}")
        return None

def save_to_repo(data):
    os.makedirs("docs", exist_ok=True)
    with open("docs/prayer_times.json", "w") as f:
        json.dump({
            "last_updated": datetime.now().isoformat(),
            "data": data
        }, f, indent=2)

if __name__ == "__main__":
    if times := fetch_prayer_times():
        save_to_repo(times)
        print("✅ Data saved to docs/prayer_times.json")
    else:
        exit(1)
