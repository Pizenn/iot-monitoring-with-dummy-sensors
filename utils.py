# utils.py
import random
import time
import json
import paho.mqtt.client as mqtt

def generate_dummy_data(sensor_type):
    timestamp = int(time.time())
    if sensor_type == 'distance':
        return {
            "device_id": "sensor_distance01",
            "distance": round(random.uniform(10.0, 600.0), 2),
            "timestamp": timestamp #time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        }
    elif sensor_type == 'ldr':
        return {
            "device_id": "sensor_ldr01",
            "light": random.randint(0, 1023),
            "timestamp": timestamp #time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        }
    elif sensor_type == 'temperature':
        return {
            "device_id": "sensor_temp01",
            "temperature": round(random.uniform(10.0, 50.0), 2),
            "timestamp": timestamp #time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        }

def publish_loop(sensor_type, topic, broker='localhost', port=1883, interval=3):
    client = mqtt.Client()
    client.connect(broker, port, 60)
    print(f"[{sensor_type.upper()}] Publisher terhubung ke broker MQTT...")

    while True:
        data = generate_dummy_data(sensor_type)
        payload = json.dumps(data)
        client.publish(topic, payload)
        print(f"[{sensor_type.upper()}] Dikirim: {payload}")
        time.sleep(interval)
