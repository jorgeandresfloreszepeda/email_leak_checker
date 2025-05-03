import requests
import time
from datetime import datetime, timedelta
from dateutil import parser

class HaveIBeenPwnedClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://haveibeenpwned.com/api/v3"
        self.headers = {
            "hibp-api-key": api_key,
            "user-agent": "EmailLeakChecker",
            "Accept": "application/json"
        }

    def check_breaches(self, email):
        """Check if an email has been involved in breaches."""
        url = f"{self.base_url}/breachedaccount/{email}?truncateResponse=false"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return []  # No breaches found
            elif response.status_code == 429:
                print("Rate limit exceeded. Waiting 10 seconds...")
                time.sleep(10)
                return self.check_breaches(email)
            else:
                print(f"API error for {email}: {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Error checking {email}: {e}")
            return []

    def get_most_recent_breach(self, breaches, months=6):
        """Find the most recent breach within the last specified months."""
        if not breaches:
            return None
        cutoff_date = datetime.now() - timedelta(days=months * 30)
        recent_breaches = [
            breach for breach in breaches
            if parser.parse(breach['BreachDate']) >= cutoff_date
        ]
        if not recent_breaches:
            return None
        # Sort by BreachDate descending
        most_recent = max(recent_breaches, key=lambda x: parser.parse(x['BreachDate']))
        return most_recent['Title']