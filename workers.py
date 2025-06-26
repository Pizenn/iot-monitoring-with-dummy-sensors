from config import ANOMALY_LIMITS, LOG_FILE, ANOMALY_LOG_FILE
import csv
import os
import json

def anomaly_worker(data):
    # Deteksi anomali berdasarkan jenis data
    for key in ['temperature', 'distance', 'light']:
        if key in data:
            min_val, max_val = ANOMALY_LIMITS[key]
            if not (min_val <= data[key] <= max_val):
                save_anomaly(data)
                return True, f"{key.upper()} ANOMALY: {data[key]}"
    return False, ""

def logger_worker(data):
    # Simpan data valid ke CSV
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    # Simpan data valid ke JSONL
    jsonl_file = LOG_FILE.replace('.csv', '.jsonl')
    with open(jsonl_file, 'a') as f_json:
        json.dump(data, f_json)
        f_json.write('\n')

def save_anomaly(data):
    # Simpan data anomali ke CSV
    file_exists = os.path.isfile(ANOMALY_LOG_FILE)
    with open(ANOMALY_LOG_FILE, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    # Simpan data anomali ke JSONL
    jsonl_file = ANOMALY_LOG_FILE.replace('.csv', '.jsonl')
    with open(jsonl_file, 'a') as f_json:
        json.dump(data, f_json)
        f_json.write('\n')

def notifier_worker(message):
    print(f"\033[91m[NOTIFIKASI ANOMALI]\033[0m {message}")  # Cetak merah di terminal
