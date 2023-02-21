import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sgpacket
import time

# test transmitter
t = sgpacket.Transmitter(sgpacket.PacketType.TCP, server_ip = '127.0.0.1', server_port = 7000)

t.run()
time.sleep(3)
t.send_one()
time.sleep(3)
t.stop()