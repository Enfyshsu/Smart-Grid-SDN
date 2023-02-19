import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sgpacket


# test transmitter
my_transmitter = sgpacket.Transmitter(sgpacket.PacketType.MMS)

# test enumerator
print(sgpacket.PacketType.TCP)
sgpacket.dnp3.a()