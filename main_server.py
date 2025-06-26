# main_server.py
import paho.mqtt.client as mqtt
import json
import threading
import queue
import time
from concurrent.futures import ThreadPoolExecutor
from workers import anomaly_worker, logger_worker, notifier_worker
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC

message_queue = queue.Queue()

# Fungsi callback MQTT saat menerima pesan
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"[DATA MASUK] {data}")
        message_queue.put(data)
    except Exception as e:
        print(f"[ERROR] Tidak bisa decode pesan: {e}")

# Worker utama (ambil data dari queue, proses)
def process_queue():
    while True:
        if not message_queue.empty():
            data = message_queue.get()
            is_anomaly, msg = anomaly_worker(data)
            if is_anomaly:
                notifier_worker(msg)
            else:
                logger_worker(data)

def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(MQTT_TOPIC)
    print("[SERVER] Terhubung ke MQTT broker. Menunggu data...")

    # Mulai thread pool untuk proses data
    with ThreadPoolExecutor(max_workers=3) as executor:
        for _ in range(3):
            executor.submit(process_queue)

        client.loop_forever()

if __name__ == '__main__':
    main()
