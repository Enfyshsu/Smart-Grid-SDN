from .abstract import *
from .packet import PacketType
from . import tcp

class Transmitter(ITransmitter):
    def __init__(self, packet_type, server_ip = None, server_port = None, dst_mac = None, ifce = None):
        self.packet_type = packet_type
        self.handler = None
        
        if self.packet_type == PacketType.TCP:
            self.handler = tcp.Client()
        else:
            raise NotImplementedError
        
        if isinstance(self.handler, ITransmitterL2):
            assert ifce is not None and dst_mac is not None
            self.handler.set_ifce(ifce)
            self.handler.set_dst_mac(dst_mac)
        elif isinstance(self.handler, ITransmitterL3):
            assert server_ip is not None and server_port is not None
            self.handler.set_server_ip(server_ip)
            self.handler.set_server_port(server_port)
            
        
    def run(self):
        self.handler.run()
        
    def stop(self):
        self.handler.stop()
        
    def send_one(self):
        self.handler.send_one()