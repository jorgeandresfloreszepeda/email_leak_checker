import pandas as pd
import csv

def read_emails_from_csv(file_path):
    """Read emails from the 4th column of a CSV file."""
    try:
        # Try reading with 'latin1' encoding, which handles more byte sequences
        df = pd.read_csv(file_path, header=None, encoding='latin1')
        if df.shape[1] < 4:
            raise ValueError("CSV must have at least 4 columns")
        emails = df[3].dropna().str.strip().tolist()
        return [email for email in emails if isinstance(email, str) and '@' in email]
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

def write_leaked_emails(file_path, leaked_emails):
    """Write emails with leaks to a new CSV with the most recent breach title."""
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Email', 'Most Recent Breach Title'])
            for email, breach_title in leaked_emails:
                writer.writerow([email, breach_title])
        print(f"Results written to {file_path}")
    except Exception as e:
        print(f"Error writing CSV: {e}")