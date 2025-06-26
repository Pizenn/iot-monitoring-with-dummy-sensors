# sensor_temperature.py
from utils import publish_loop

if __name__ == '__main__':
    publish_loop(sensor_type='temperature', topic='sensor/temperature', interval=4)
