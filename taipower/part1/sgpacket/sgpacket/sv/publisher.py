from . import _lib61850
import time
import threading
import queue

class Publisher():
    def __init__(self, interface = 'eth0'):
        self.interface = interface
        self.command_q = queue.Queue()
        
    def _start(self):
        svPublisher = _lib61850.SVPublisher_create(None, self.interface)
        if svPublisher:
            asdu1 = _lib61850.SVPublisher_addASDU(svPublisher, "svpub1", None, 1)
            float1 = _lib61850.SVPublisher_ASDU_addFLOAT(asdu1)
            float2 = _lib61850.SVPublisher_ASDU_addFLOAT(asdu1)
            ts1 = _lib61850.SVPublisher_ASDU_addTimestamp(asdu1)
        
            _lib61850.SVPublisher_setupComplete(svPublisher)
            fVal1 = 1234.5678
            fVal2 = 0.12345
            
            while True:
                if not self.command_q.empty():
                    cmd = self.command_q.get()
                    if cmd == 87:
                        for i in range(3):
                            ts = _lib61850.Timestamp()
                            _lib61850.Timestamp_clearFlags(ts)
                            _lib61850.Timestamp_setTimeInMilliseconds(ts, int(time.time()))
                            
                            _lib61850.SVPublisher_ASDU_setFLOAT(asdu1, float1, fVal1)
                            _lib61850.SVPublisher_ASDU_setFLOAT(asdu1, float2, fVal2)
                            _lib61850.SVPublisher_ASDU_setTimestamp(asdu1, ts1, ts)
                    
                            _lib61850.SVPublisher_ASDU_increaseSmpCnt(asdu1);
                            fVal1 += 1.1
                            fVal2 += 0.1
                    
                            _lib61850.SVPublisher_publish(svPublisher)
                            time.sleep(0.5)
                    elif cmd == 88:
                        break
            _lib61850.SVPublisher_destroy(svPublisher)
        else:
            print("Failed to create SV publisher.")
    def run(self):
        th = threading.Thread(target=self._start)
        th.start()
    
    def publish_data(self):
        self.command_q.put(87)
        
    def stop(self):
        self.command_q.put(88)
    



