# 🧾 Mintscan to Koinly Converter

This Python script transforms a transaction history CSV file downloaded from [Mintscan](https://www.mintscan.io) into a **Koinly-compatible Advanced CSV format**, ready to be imported directly into [Koinly](https://koinly.io) for tax reporting.

---

## ✅ What the script does

- Filters only the **relevant transaction types**: `Send`, `Receive`, `IBCSend`, `IBCReceive`, and `GetReward`.
- Automatically **normalizes IBC types** (`IBCSend` → `Send`, `IBCReceive` → `Receive`).
- **Groups** transactions by their `txhash` to consolidate related actions.
- **Converts timestamps** to the required Koinly format (`YYYY-MM-DD HH:MM:SS`, UTC).
- **Labels `GetReward` transactions** with the `reward` tag for correct classification in Koinly.
- Outputs a CSV file named like the original but with `_transformed.csv` appended — ready for import into Koinly.

---

## 📥 Getting the input file

1. Visit **[Mintscan](https://www.mintscan.io)** and search for your wallet address (e.g., from the Saga blockchain).
2. Use the **"Export"** function to download your transaction history as a CSV file.
3. Place this file in the **same folder** as the script.

---

## ▶️ How to run

1. Make sure you have Python 3 and `pandas` installed:

   ```bash
   pip install pandas

2. Place both the script and the downloaded CSV in the same directory.
3. Edit the script and paste your downloaded CSV file name.
4. Run the script:

   ```bash
   python mintscan_to_koinly.py

5. After execution, you’ll find the output file.
6. Upload it to Koinly and check transactions.

---

## 🛠️ Notes
- This script is designed for simple wallet transaction histories (not for complex DeFi or NFT operations).