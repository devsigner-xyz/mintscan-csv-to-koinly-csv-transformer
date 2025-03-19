import pandas as pd
from dateutil import parser as dateparser
import pytz

# =====================================
# CONFIGURATION
# =====================================

# 1) Input CSV file with your Saga transactions
SAGA_CSV_INPUT = "DOWNLOADED_CSV_NAME.csv"

# 2) Output CSV file (Koinly universal format)
KOINLY_CSV_OUTPUT = "saga_universal_koinly.csv"

# 3) (Optional) Your Saga address, if you want to handle "from" or "to" checks
MY_SAGA_ADDRESS = "YOUR_SAGA_ADDRESS"

# 4) Conversion factor (for "usaga" to "SAGA"). 1 SAGA = 1e6 usaga.
MICRO_DENOM_FACTOR = 1e-6

# 5) If the CSV timestamps have no timezone, assume UTC (or another TZ like "Europe/Madrid").
TIMEZONE_ASSUMED = None

# 6) Labels (Koinly tags)
LABEL_DELEGATE = "stake"   # For delegate transactions
LABEL_REWARD = "reward"    # For staking rewards

# 7) The Koinly currency symbol to use for Saga
CURRENCY_SAGA = "SAGA"


# =====================================
# HELPER FUNCTIONS
# =====================================

def parse_saga_amount(amount_str: str) -> float:
    """
    Parses a string that may contain dot separators for thousands,
    converts it to an integer in 'usaga', then applies MICRO_DENOM_FACTOR to get SAGA.

    Example:
      "22.000.000" -> remove dots -> "22000000" -> int(22000000) -> 22000000 usaga -> 22 SAGA
    """
    clean_str = amount_str.replace(".", "")
    as_int = int(clean_str)
    return as_int * MICRO_DENOM_FACTOR

def parse_timestamp_to_utc(ts_str: str) -> str:
    """
    Parses a timestamp string such as "2024-12-26 19:36:19" and returns a
    string in Koinly's preferred format "YYYY-MM-DD HH:mm:ss" in UTC.
    
    If the original timestamp has no timezone and TIMEZONE_ASSUMED is set,
    it will localize to that timezone and then convert to UTC.
    Otherwise, it is assumed to be UTC already.
    """
    dt = dateparser.parse(ts_str)
    if dt is None:
        return ""
    if dt.tzinfo is None:
        if TIMEZONE_ASSUMED:
            dt_local = pytz.timezone(TIMEZONE_ASSUMED).localize(dt)
            dt_utc = dt_local.astimezone(pytz.UTC)
        else:
            dt_utc = dt
    else:
        dt_utc = dt.astimezone(pytz.UTC)
    return dt_utc.strftime("%Y-%m-%d %H:%M:%S")


# =====================================
# MAIN SCRIPT
# =====================================

def main():
    # Read the original Saga CSV
    df = pd.read_csv(SAGA_CSV_INPUT, dtype=str)  # Everything as strings to avoid float parsing issues

    # Koinly's universal CSV columns
    columns_koinly = [
        "Date",
        "Sent Amount",
        "Sent Currency",
        "Received Amount",
        "Received Currency",
        "Fee Amount",
        "Fee Currency",
        "Net Worth Amount",
        "Net Worth Currency",
        "Label",
        "Description",
        "TxHash",
    ]

    # We'll accumulate rows in this list, then build a DataFrame at the end
    koinly_rows = []

    for _, row in df.iterrows():
        # Build a blank dictionary for each row
        krow = {col: "" for col in columns_koinly}

        # Extract fields from the Saga CSV
        tx_type = (row.get("type", "") or "").strip()
        tx_from = (row.get("from", "") or "").strip()
        tx_to   = (row.get("to", "") or "").strip()
        tx_hash = (row.get("txhash", "") or "").strip()
        amt_str = (row.get("amount", "0") or "").strip()
        ts_str  = (row.get("timestamp", "") or "").strip()

        # Parse the date/time
        krow["Date"] = parse_timestamp_to_utc(ts_str)
        # Store the transaction hash
        krow["TxHash"] = tx_hash

        # Skip rows with empty or zero amount
        if amt_str == "" or amt_str == "0":
            continue

        # Convert usaga to SAGA
        try:
            amount_saga = parse_saga_amount(amt_str)
        except:
            amount_saga = 0

        # Classify the transaction based on 'type'
        if tx_type in ["Delegate", "Send", "IBCSend"]:
            # Outgoing transaction
            krow["Sent Amount"] = amount_saga
            krow["Sent Currency"] = CURRENCY_SAGA
            if tx_type == "Delegate":
                krow["Label"] = LABEL_DELEGATE
        elif tx_type in ["Receive"]:
            # Incoming transaction
            krow["Received Amount"] = amount_saga
            krow["Received Currency"] = CURRENCY_SAGA
        elif tx_type in ["GetReward"]:
            # Staking reward
            krow["Received Amount"] = amount_saga
            krow["Received Currency"] = CURRENCY_SAGA
            krow["Label"] = LABEL_REWARD
        else:
            # Unhandled transaction type (you can skip or handle differently)
            pass

        # Optional description
        krow["Description"] = f"{tx_type} from {tx_from} to {tx_to}"

        koinly_rows.append(krow)

    # Build the final DataFrame
    df_koinly = pd.DataFrame(koinly_rows, columns=columns_koinly)

    # Filter out rows that have neither Sent nor Received
    mask_nonempty = ~(
        (df_koinly["Sent Amount"] == "") &
        (df_koinly["Received Amount"] == "")
    )
    df_koinly = df_koinly[mask_nonempty]

    # Write the final CSV
    df_koinly.to_csv(KOINLY_CSV_OUTPUT, index=False)
    print(f"Created '{KOINLY_CSV_OUTPUT}' with {len(df_koinly)} transactions.")


if __name__ == "__main__":
    main()
