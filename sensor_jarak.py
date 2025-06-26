# sensor_distance.py
from utils import publish_loop

if __name__ == '__main__':
    publish_loop(sensor_type='distance', topic='sensor/distance', interval=3)
