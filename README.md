# Saga CSV to Koinly Universal CSV

This Python script converts your **Saga CSV** transactions into **Koinly’s Universal CSV** format. It reads a CSV with transactions (delegates, rewards, sends, etc.), classifies them, and generates an output CSV compatible with Koinly.

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install pandas python-dateutil pytz

2. **Edit the Script (.py file)**:
   
- SAGA_CSV_INPUT → the name of your downloaded Saga CSV.
- KOINLY_CSV_OUTPUT → the name of the output file to be generated.
- MY_SAGA_ADDRESS → your Saga wallet address (optional).
- MICRO_DENOM_FACTOR → conversion factor if amounts are in usaga.
- TIMEZONE_ASSUMED → default timezone if timestamps have none (or leave it as None).
- LABEL_DELEGATE, LABEL_REWARD, CURRENCY_SAGA → Koinly tags/currency symbol as needed.

3. **Run the script**:
   ```bash
   python saga_to_koinly.py

4. Import the resulting CSV (e.g., saga_universal_koinly.csv) into Koinly.