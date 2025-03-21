import pandas as pd
import os

# Input filename defined here
INPUT_FILE = "DOWNLOADED_MINTSCAN_SAGA_TRANSACTION_HISTORY.csv"

def convert_mintscan_to_koinly(input_path):
    df = pd.read_csv(input_path)

    # Only include relevant transaction types
    valid_types = ['Send', 'Receive', 'IBCSend', 'IBCReceive', 'GetReward']
    df = df[df['type'].isin(valid_types)]

    # Normalize transaction types
    df['type'] = df['type'].replace({'IBCSend': 'Send', 'IBCReceive': 'Receive'})

    # Convert timestamp to Koinly-compatible UTC format
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')

    # Group by transaction hash and type
    grouped = df.groupby(['txhash', 'type'])

    koinly_records = []
    for (txhash, tx_type), group in grouped:
        total_amount = group['amount'].sum()
        date = group.iloc[0]['timestamp']
        token = group.iloc[0]['token']

        record = {
            'Date': date,
            'Sent Amount': total_amount if tx_type == 'Send' else '',
            'Sent Currency': token if tx_type == 'Send' else '',
            'Received Amount': total_amount if tx_type in ['Receive', 'GetReward'] else '',
            'Received Currency': token if tx_type in ['Receive', 'GetReward'] else '',
            'Fee Amount': '',
            'Fee Currency': '',
            'Net Worth Amount': '',
            'Net Worth Currency': '',
            'Label': 'reward' if tx_type == 'GetReward' else '',
            'Description': '',
            'TxHash': txhash
        }
        koinly_records.append(record)

    output_df = pd.DataFrame(koinly_records)

    # Output file with '_transformed' suffix
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_transformed.csv"
    output_df.to_csv(output_path, index=False)

    print(f"Converted file saved to: {output_path}")

if __name__ == "__main__":
    convert_mintscan_to_koinly(INPUT_FILE)
