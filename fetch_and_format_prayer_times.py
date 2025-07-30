import requests
import json
from datetime import datetime

MASJID_ID = "keLQn7AM"
YEAR = datetime.now().year
API_URL = f"https://masjidal.com/api/v1/time/range?masjid_id={MASJID_ID}&from_date={YEAR}-01-01&to_date={YEAR}-12-31"

def load_and_format_prayer_times():
    try:
        print("🔄 Fetching data from Masjidal API...")
        response = requests.get(API_URL)
        response.raise_for_status()
        # Debug what kind of data we get
        print("Raw API response snippet:", response.text[:300])
        try:
            data = response.json()
        except Exception as e:
            print("❌ Response was not valid JSON:", response.text)
            raise

        days = data.get("data", [])
        formatted_output = []

        for day in days:
            formatted_day = {
                "date": day.get("date", ""),
                "hijri_date": f"{day.get('hijri', {}).get('day_ar', '')}, {day.get('hijri', {}).get('year_ar', '')}",
                "hijri_month": day.get("hijri", {}).get("month_en", ""),
                "day": day.get("day", ""),
                "fajr": day.get("prayer_times", {}).get("fajr", ""),
                "fajr_iqama": day.get("iqama_times", {}).get("fajr", ""),
                "sunrise": day.get("prayer_times", {}).get("sunrise", ""),
                "dhuhr": day.get("prayer_times", {}).get("dhuhr", ""),
                "dhuhr_iqama": day.get("iqama_times", {}).get("dhuhr", ""),
                "asr": day.get("prayer_times", {}).get("asr", ""),
                "asr_iqama": day.get("iqama_times", {}).get("asr", ""),
                "maghrib": day.get("prayer_times", {}).get("maghrib", ""),
                "maghrib_iqama": day.get("iqama_times", {}).get("maghrib", ""),
                "isha": day.get("prayer_times", {}).get("isha", ""),
                "isha_iqama": day.get("iqama_times", {}).get("isha", "")
            }
            formatted_output.append(formatted_day)

        # Write to file
        with open("prayer_times.json", "w", encoding="utf-8") as f:
            json.dump(formatted_output, f, indent=2, ensure_ascii=False)

        print("✅ Successfully updated prayer_times.json.")

    except requests.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}; API response: {response.text}")
    except Exception as err:
        print(f"❌ Unexpected error: {err}")

if __name__ == "__main__":
    load_and_format_prayer_times()

