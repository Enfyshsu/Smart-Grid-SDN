import sys
import time
import threading
import traceback
import signal
import sys
sys.path.insert(0, "/libiec61850/pyiec61850")
import iec61850
from datetime import datetime
import queue
import enum

class MMS_CLIENT_CMD(enum.Enum):
   send_req = 0
   stop = 1

class Client():
    def __init__(self, server_ip = "127.0.0.1", port = 102):
        self.server_ip = server_ip
        self.port = port
        self.command_q = queue.Queue()
        
    def _start(self):
        con = iec61850.IedConnection_create()
        error = iec61850.IedConnection_connect(con, self.server_ip, self.port)
        if error == iec61850.IED_ERROR_OK:
            while True:
                if not self.command_q.empty():
                    cmd = self.command_q.get()
                    if cmd == MMS_CLIENT_CMD.send_req:
                        the_val = "testmodelLD1/LN1.DO1.data1"
                        the_val_type = iec61850.IEC61850_FC_MX
                        value = iec61850.IedConnection_readFloatValue(con, the_val, the_val_type)
                        print("Received data:", value)
                    elif cmd == MMS_CLIENT_CMD.stop:
                        break
        else:
            print("Connection error")
            
        iec61850.IedConnection_close(con)
        iec61850.IedConnection_destroy(con)
    
    def run(self):
        th = threading.Thread(target=self._start)
        th.start()
    
    def request_data(self):
        self.command_q.put(MMS_CLIENT_CMD.send_req)
        
    def stop(self):
        self.command_q.put(MMS_CLIENT_CMD.stop)
        