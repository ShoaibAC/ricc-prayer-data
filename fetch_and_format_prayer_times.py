import requests
import json
from datetime import datetime

MASJID_ID = "keLQn7AM"
YEAR = datetime.now().year
API_URL = f"https://masjidal.com/api/v1/time/range?masjid_id={MASJID_ID}&from_date={YEAR}-01-01&to_date={YEAR}-12-31"

def load_and_format_prayer_times():
    try:
        print("🔄 Fetching prayer times from Masjidal API...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if not isinstance(data.get("data"), list):
            raise ValueError("API returned unexpected data format")

        formatted_output = []
        for day in data["data"]:
            formatted_day = {
                "date": day["date"],
                "hijri_date": f"{day['hijri']['day_ar']}, {day['hijri']['year_ar']}",
                "hijri_month": day["hijri"]["month_en"],
                "day": day["day"],
                "fajr": day["prayer_times"]["fajr"],
                "fajr_iqama": day["iqama_times"]["fajr"],
                "sunrise": day["prayer_times"]["sunrise"],
                "dhuhr": day["prayer_times"]["dhuhr"],
                "dhuhr_iqama": day["iqama_times"]["dhuhr"],
                "asr": day["prayer_times"]["asr"],
                "asr_iqama": day["iqama_times"]["asr"],
                "maghrib": day["prayer_times"]["maghrib"],
                "maghrib_iqama": day["iqama_times"]["maghrib"],
                "isha": day["prayer_times"]["isha"],
                "isha_iqama": day["iqama_times"]["isha"]
            }
            formatted_output.append(formatted_day)

        with open("docs/prayer_times.json", "w", encoding="utf-8") as f:
            json.dump(formatted_output, f, indent=2, ensure_ascii=False)

        print("✅ Successfully updated prayer_times.json")
        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    load_and_format_prayer_times()
