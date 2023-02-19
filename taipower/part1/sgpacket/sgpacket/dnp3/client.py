import queue
import threading
from datetime import datetime
from pydnp3 import opendnp3, openpal
from ._master import Master, MyLogger, AppChannelListener, SOEHandler, MasterApplication
from ._master import command_callback, restart_callback

class Client():
    def __init__(self, local_ip = "0.0.0.0", port = 20000, server_ip = "127.0.0.1"):
        self.log_levels = opendnp3.levels.NORMAL | opendnp3.levels.ALL_COMMS
        self.local_ip = local_ip
        self.port = port
        self.server_ip = server_ip
        self.command_q = queue.Queue()
        
        
    def _start(self):
        app = Master(log_handler=MyLogger(), listener=AppChannelListener(), soe_handler=SOEHandler(), master_application=MasterApplication(), log_levels = self.log_levels, local_ip = self.local_ip, port = self.port, host_ip = self.server_ip)
        while True:
            item = self.command_q.get()
            if item == 87:
                app.send_direct_operate_command(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON), 5, command_callback)
            if item == 88:
                app.shutdown()
                break
            
    def run(self):
        th = threading.Thread(target=self._start)
        th.start()
        
    def send_o1(self):
        self.command_q.put(87)
        
        
    def stop(self):
        self.command_q.put(88)
