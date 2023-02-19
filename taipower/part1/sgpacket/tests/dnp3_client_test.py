import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sgpacket.dnp3

client = sgpacket.dnp3.Client()
client.run()
client.send_o1()
#client.stop()
