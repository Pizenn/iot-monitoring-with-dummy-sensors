# sensor_ldr.py
from utils import publish_loop

if __name__ == '__main__':
    publish_loop(sensor_type='ldr', topic='sensor/ldr', interval=5)
