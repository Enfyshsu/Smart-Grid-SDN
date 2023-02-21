from .abstract import *
from .packet import PacketType
from . import tcp

class Receiver(IReceiver):
    def __init__(self, packet_type, ip, port):
        self.packet_type = packet_type
        self.handler = None
    
        if self.packet_type == PacketType.TCP:
            self.handler = tcp.Server()
        
        self.set_ip(ip)
        self.set_port(port)
        
    def run(self):
        self.handler.run()
        
    def stop(self):
        self.handler.stop()
        
    def set_ip(self, ip):
        self.handler.set_ip(ip)
        
    def set_port(self, port):
        self.handler.set_port(port)