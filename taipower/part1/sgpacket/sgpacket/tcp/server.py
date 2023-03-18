import socket
import threading
import time
import statistics
from sgpacket.abstract import IReceiver

class Server(IReceiver):
    def __init__(self, host = '0.0.0.0', port = 7000):
        self.host = host
        self.port = port
        self.conn = None
        self.s = None
        self.packet_num = None
        self.time_log = []
        
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
                break
            if indata.find('<time>'.encode('utf-8')) >= 0:
                self.time_log.append(time.time() - float(indata.split()[1]))
            print('recv: ' + indata.decode())
        print('Client closed connection.')
        if len(self.time_log) == self.packet_num:
            self.delay_analysis(self.time_log)

    def set_ip(self, ip):
        self.host = ip
        
    def set_port(self, port):
        self.port = port
        
    def run(self):
        th = threading.Thread(target = self._start)
        th.start()
        
    def stop(self):
        self.s.close()
        
    def delay_analysis(self, data):
        mean = statistics.mean(data)
        stdev = statistics.stdev(data)
        print("Mean: %.6f" %mean) 
        print("Standard Deviation: %.6f" % stdev)