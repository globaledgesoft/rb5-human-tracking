import numpy as np
from mqtt_utils import Mqtt_Class

if __name__ == '__main__':
    client1 = Mqtt_Class("cl1")
    client1.subscribe_topic("track")
    client1.client.loop_forever()
    
