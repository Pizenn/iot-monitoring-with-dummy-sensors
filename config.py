# config.py

# MQTT Broker
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC = 'sensor/#'

# Batas anomali untuk tiap sensor
ANOMALY_LIMITS = {
    "temperature": (15, 40),
    "distance": (0, 500),       # cm
    "light": (100, 800)         # lux
}

# File log data valid
LOG_FILE = 'data/data_log.csv'

# File log data anomali
ANOMALY_LOG_FILE = 'data/anomaly_log.csv'
