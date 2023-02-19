import socket

class Server():
    def __init__(self, host = '0.0.0.0', port = 7000):
        self.host = host
        self.port = port
        
    def _start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)

        print('wait for connection...')

        while True:
            conn, addr = s.accept()
            print('connected by ' + str(addr))

            while True:
                indata = conn.recv(1024)
                if len(indata) == 0: # connection closed
                    conn.close()
                    print('client closed connection.')
                    break
                print('recv: ' + indata.decode())

                outdata = 'echo ' + indata.decode()
                conn.send(outdata.encode())
        s.close()
        
    def run(self):
    def stop(self):