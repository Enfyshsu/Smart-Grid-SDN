import socket
import threading 

class Server():
    def __init__(self, host = '0.0.0.0', port = 7000):
        self.host = host
        self.port = port
        self.conn = None
        self.s = None
        
    def _start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.host, self.port))

        print('Wait for data...')
        while True:
            indata, addr = self.s.recvfrom(1024)
            print('Receive data from ' + str(addr) + ': ' + indata.decode())
        self.s.close()
        
        
    def run(self):
        th = threading.Thread(target = self._start)
        th.start()
        
    def stop(self):
        self.s.close()
        #self.conn.close()
        