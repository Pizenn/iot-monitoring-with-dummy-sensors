# client/multi_client.py
import paho.mqtt.client as mqtt
import time
import random
import json
import threading

BROKER = 'localhost'
PORT = 1883
INTERVAL = 3  # detik

# Fungsi untuk menghasilkan data dummy
def generate_data(sensor_type, device_id):
    timestamp = int(time.time())
    if sensor_type == 'temperature':
        return {
            "device_id": device_id,
            "temperature": round(random.uniform(10, 50), 2),
            "timestamp": timestamp
        }
    elif sensor_type == 'distance':
        return {
            "device_id": device_id,
            "distance": round(random.uniform(10, 600), 2),
            "timestamp": timestamp
        }
    elif sensor_type == 'light':
        return {
            "device_id": device_id,
            "light": random.randint(0, 1023),
            "timestamp": timestamp
        }

# Fungsi untuk satu client sensor
def run_sensor(sensor_type, device_id, topic, interval):
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    print(f"[{device_id}] Terhubung ke broker MQTT")

    while True:
        data = generate_data(sensor_type, device_id)
        payload = json.dumps(data)
        client.publish(topic, payload)
        print(f"[{device_id}] Dikirim: {payload}")
        time.sleep(interval)

# Jalankan banyak client
def start_clients():
    configs = []

    # Atur jumlah client tiap jenis sensor
    num_temp = 1
    num_distance = 1
    num_light = 1

    # Sensor suhu
    for i in range(num_temp):
        configs.append(('temperature', f'Sensor Suhu : {i+1}', 'sensor/temperature'))

    # Sensor jarak
    for i in range(num_distance):
        configs.append(('distance', f'Sensor Jarak : {i+1}', 'sensor/distance'))

    # Sensor cahaya
    for i in range(num_light):
        configs.append(('light', f'Sensor Cahaya : {i+1}', 'sensor/ldr'))

    # Jalankan semua client di thread terpisah
    for sensor_type, device_id, topic in configs:
        t = threading.Thread(target=run_sensor, args=(sensor_type, device_id, topic, INTERVAL))
        t.daemon = True
        t.start()

    while True:
        time.sleep(1)  # biar main thread tetap jalan

if __name__ == '__main__':
    start_clients()
