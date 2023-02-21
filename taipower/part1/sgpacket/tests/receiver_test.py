import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sgpacket
import time

r = sgpacket.Receiver(sgpacket.PacketType.TCP, ip = '0.0.0.0', port = 7000)
r.run()
#time.sleep(5)
#r.stop()