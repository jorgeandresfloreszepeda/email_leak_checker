import os
from .leak_checker import LeakChecker

def main():
    api_key = os.getenv("HIBP_API_KEY")  # Set this in your environment
    if not api_key:
        print("Error: HIBP_API_KEY environment variable not set.")
        return
    
    input_csv = "../Private/itsecuritylist.csv"
    output_csv = "leaked_emails.csv"
    
    checker = LeakChecker(api_key)
    checker.check_emails(input_csv, output_csv)

if __name__ == "__main__":
    main()