import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './sgpacket')))
from sgpacket import tcp, udp, xmpp
import time
import cmd

class SGPacketHelper(cmd.Cmd):
    intro = 'Use the helper to send packets. Type help or ? to list commands.\n'
    prompt = '<Cmd> '
    
    def do_UDP(self, addr):
        '''****************************\nSend UDP packets: UDP [IP]\nE.g., UDP 10.0.2.201\n****************************'''
        port = 7001
        t = udp.Client(server_ip = addr, port = port)
        send_packets(t, 'UDP', addr, port)

    def do_DNP3(self, addr):
        '''****************************\nSend DNP3 packets: DNP3 [IP]\nE.g., DNP3 10.0.2.201\n****************************'''
        port = 20000
        t = tcp.Client(server_ip = addr, port = port)
        send_packets(t, 'DNP3', addr, port)

    def do_XMPP(self, addr):
        '''****************************\nSend XMPP packets: XMPP [IP]\nE.g., XMPP 10.0.2.201\n****************************'''
        port = 5222
        t = xmpp.Client(server_ip = addr, port = port)
        send_packets(t, 'XMPP', addr, port)
    
    def do_bye(self, arg):
        'Exit the helper:  bye'
        print('Bye.')
        return True


def send_packets(t, pkt_type, addr, port):
    try:
        t.run()
        if pkt_type == 'XMPP':
            for i in range(1000):
                t.send_msg("Edward", "<time>")
                time.sleep(0.05)
        else:
            for i in range(1000):
                t.send_msg("<time> " + str(time.time()))
                time.sleep(0.05)
        t.stop()
        t.join()
        sent_success(pkt_type, addr, port)
    except:
        # t.stop()
        print('Error occurred.')

def sent_success(pkt_type, addr, port=None):
    print('Sent %s packets to %s:%d.' %(pkt_type, addr, port))

if __name__ == '__main__':
    SGPacketHelper().cmdloop()