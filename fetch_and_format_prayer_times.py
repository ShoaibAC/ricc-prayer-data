import requests
import json
from datetime import datetime
import os  # Added for directory handling

MASJID_ID = "keLQn7AM"
YEAR = datetime.now().year
API_URL = f"https://masjidal.com/api/v1/time/range?masjid_id={MASJID_ID}&from_date={YEAR}-01-01&to_date={YEAR}-12-31"

def load_and_format_prayer_times():
    try:
        print("🔄 Fetching prayer times from Masjidal API...")
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'  # Explicitly request JSON
        }
        response = requests.get(API_URL, headers=headers, timeout=15)  # Increased timeout
        response.raise_for_status()
        
        # Debug: Print API status
        print(f"API Response Status: {response.status_code}")
        
        data = response.json()
        if not isinstance(data.get("data"), list):
            raise ValueError("API returned unexpected data format")

        formatted_output = []
        for day in data["data"]:
            try:
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
            except Exception as day_error:
                print(f"⚠️ Error processing day data: {day_error}")
                continue

        # Create docs directory if it doesn't exist
        os.makedirs("docs", exist_ok=True)
        
        # Write to file with error handling
        try:
            with open("docs/prayer_times.json", "w", encoding="utf-8") as f:
                json.dump(formatted_output, f, indent=2, ensure_ascii=False)
            print("✅ Successfully updated docs/prayer_times.json")
        except IOError as file_error:
            raise Exception(f"Failed to write JSON file: {file_error}")

        return True

    except requests.exceptions.RequestException as req_err:
        print(f"❌ Network error: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"❌ Invalid JSON response: {json_err}")
        print(f"Response content: {response.text[:200]}...")  # Show partial response
    except Exception as err:
        print(f"❌ Unexpected error: {err}")
    
    return False

if __name__ == "__main__":
    success = load_and_format_prayer_times()
    if not success:
        exit(1)  # Exit with error code if failed
