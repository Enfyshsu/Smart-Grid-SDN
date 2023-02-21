import socket
import threading 
from sgpacket.abstract import IReceiver

class Server(IReceiver):
    def __init__(self, host = '0.0.0.0', port = 7000):
        self.host = host
        self.port = port
        self.conn = None
        self.s = None
        
    def _start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(5)

        print('wait for connection...')
        
        self.conn, addr = self.s.accept()
        print('connected by ' + str(addr))

        while True:
            indata = self.conn.recv(1024)
            if len(indata) == 0: # connection closed
                self.conn.close()
                print('client closed connection.')
                break
            print('recv: ' + indata.decode())

            #outdata = 'echo ' + indata.decode()
            #self.conn.send(outdata.encode())
        
    def set_ip(self, ip):
        self.host = ip
        
    def set_port(self, port):
        self.port = port
        
    def run(self):
        th = threading.Thread(target = self._start)
        th.start()
        
    def stop(self):
        self.s.close()
        #self.conn.close()
        