from .api_client import HaveIBeenPwnedClient
from .csv_handler import read_emails_from_csv, write_leaked_emails
import time

class LeakChecker:
    def __init__(self, api_key):
        self.client = HaveIBeenPwnedClient(api_key)

    def check_emails(self, input_csv, output_csv):
        """Check emails for leaks and write results to a CSV."""
        emails = read_emails_from_csv(input_csv)
        leaked_emails = []
        
        for i, email in enumerate(emails, 1):
            print(f"Checking email {i}/{len(emails)}: {email}")
            breaches = self.client.check_breaches(email)
            breach_title = self.client.get_most_recent_breach(breaches, months=6)
            if breach_title:
                leaked_emails.append((email, breach_title))
            time.sleep(1.6)  # Respect HIBP rate limit (1.5s + buffer)
        
        if leaked_emails:
            write_leaked_emails(output_csv, leaked_emails)
        else:
            print("No leaks found in the last 6 months.")