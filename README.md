# Email Leak Checker

Checks a list of emails for data breaches using the HaveIBeenPwned API.

## Setup

1. Install Python 3.8+.
2. Install dependencies: `pip install -r requirements.txt`
3. Get an API key from https://haveibeenpwned.com/API/Key
4. Set the API key as an environment variable:
   - WSL/Ubuntu: `export HIBP_API_KEY=your_api_key`
5. Prepare an `input.csv` with emails in the 4th column.

## Usage

Run: `python src/main.py`

Output: `leaked_emails.csv` with emails and most recent breach titles (if leaks found in the last 6 months).

## Notes

- Compatible with WSL (Windows 11) and Ubuntu 22.04.
- Respects HIBP API rate limits.
- Handles errors gracefully.
