import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './sgpacket')))
from sgpacket import tcp, udp
import time
import cmd

class SGPacketHelper(cmd.Cmd):
    intro = 'Use the helper to send packets. Type help or ? to list commands.\n'
    prompt = '<Cmd> '
    
    def do_UDP(self, arg):
        '''********************\nOpen UDP receiver\n********************'''
        port = 7001
        r = udp.Server(host = '0.0.0.0', port = port)
        open_receiver(r, 'UDP', port)

    def do_DNP3(self, arg):
        '''********************\nOpen DNP3 receiver\n********************'''
        port = 20000
        r = tcp.Server(host = '0.0.0.0', port = port)
        open_receiver(r, 'DNP3', port)

    def do_XMPP(self, arg):
        '''********************\nOpen XMPP receiver\n********************'''
        port = 5222
        r = tcp.Server(host = '0.0.0.0', port = port)
        open_receiver(r, 'XMPP', port)

    def do_bye(self, arg):
        'Exit the helper:  bye'
        print('Bye.')
        return True

def open_receiver(r, pkt_type, port):
    try:
        r.run()
        r.packet_num = 500
        time.sleep(180)
        r.stop()
        receiver_closed(pkt_type, port)
    except:
        r.stop()
        print('Receiver stopped.')

def receiver_closed(pkt_type, port):
    print('%s receiver on port %s is closed.' %(pkt_type, port))

if __name__ == '__main__':
    SGPacketHelper().cmdloop()