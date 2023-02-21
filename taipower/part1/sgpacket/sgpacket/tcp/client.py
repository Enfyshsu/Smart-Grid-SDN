import socket
import threading
import queue
import enum
from sgpacket.abstract import ITransmitterL3

class TCP_CMD(enum.Enum):
   send = 0
   stop = 1
   
class Client(ITransmitterL3):
    def __init__(self, server_ip = '127.0.0.1', port = 7000):
        self.server_ip = server_ip
        self.port = port
        self.command_q = queue.Queue()
        
            
    def _start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.server_ip, self.port))
        while True:
            if not self.command_q.empty():
                cmd = self.command_q.get()
                if cmd == TCP_CMD.send:
                    msg = self.command_q.get()
                    s.send(msg.encode())
                    print('Send to ' + str(self.server_ip) + ': ' + msg)
                elif cmd == TCP_CMD.stop:
                    s.close()
                    print("Connection closed.")
                    break
            

    def run(self):
        th = threading.Thread(target = self._start)
        th.start()
        
    def stop(self):
        self.command_q.put(TCP_CMD.stop)
        
    def set_server_ip(self, server_ip):
        self.server_ip = server_ip
        
    def set_server_port(self, server_port):
        self.port = server_port
    
    def send_msg(self, msg):
        self.command_q.put(TCP_CMD.send)
        self.command_q.put(msg)
        
    def send_one(self):
        self.send_msg("Taipower Taipower No.1!!")
