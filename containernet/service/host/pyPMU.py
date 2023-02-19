from synchrophasor.frame import *
from synchrophasor.pmu import Pmu
import functools
import re
import subprocess
import argparse
"""
pyPMU is custom configured PMU simulator. Code below represents
PMU described in IEEE C37.118.2 - Annex D.
"""

def get_host_ip():
    ip_a = subprocess.check_output("ip a", shell=True).decode('utf-8')
    ips = re.findall(r'-eth0@.*\n.*\n.*inet (.*)/', ip_a)
    assert len(ips) == 1
    return ips[0]

def get_pmu_name():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pmu_name', '-name', type=str, required=True, help='PMU name')
    pmu_name = parser.parse_args().pmu_name
    return pmu_name

def set_time_slower(self, soc=None, frasec=None):
        t = time()-5  # Get current timestamp
        print('slow')
        if soc:
            self.set_soc(soc-5)
        else:
            self.set_soc(int(t))  # Get current timestamp

        if frasec:
            if isinstance(frasec, collections.Sequence):
                self.set_frasec(*frasec)
            else:
                self.set_frasec(frasec)  # Just set fraction of second and use default values for other arguments.
        else:
            # Calculate fraction of second (after decimal point) using only first 7 digits to avoid
            # overflow (24 bit number).
            self.set_frasec(int((((repr((t % 1))).split("."))[1])[0:6]))

if __name__ == "__main__":
    host_ip = get_host_ip()
    pmu_name = get_pmu_name()
    print('Host Address:', host_ip)
    pmu = Pmu(ip=host_ip, port=9991)
    pmu.logger.setLevel("DEBUG")

    ph_v_conversion = int(300000.0 / 32768 * 100000)  # Voltage phasor conversion factor
    ph_i_conversion = int(15000.0 / 32768 * 100000)  # Current phasor conversion factor

    cfg = ConfigFrame2(7,  # PMU_ID
                       1000000,  # TIME_BASE
                       1,  # Number of PMUs included in data frame
                       pmu_name,  # Station name
                       7734,  # Data-stream ID(s)
                       (False, False, True, False),  # Data format - Check ConfigFrame2 set_data_format()
                       4,  # Number of phasors
                       3,  # Number of analog values
                       1,  # Number of digital status words
                       ["VA", "VB", "VC", "I1", "ANALOG1", "ANALOG2", "ANALOG3", "BREAKER 1 STATUS",
                        "BREAKER 2 STATUS", "BREAKER 3 STATUS", "BREAKER 4 STATUS", "BREAKER 5 STATUS",
                        "BREAKER 6 STATUS", "BREAKER 7 STATUS", "BREAKER 8 STATUS", "BREAKER 9 STATUS",
                        "BREAKER A STATUS", "BREAKER B STATUS", "BREAKER C STATUS", "BREAKER D STATUS",
                        "BREAKER E STATUS", "BREAKER F STATUS", "BREAKER G STATUS"],  # Channel Names
                       [(ph_v_conversion, "v"), (ph_v_conversion, "v"),
                        (ph_v_conversion, "v"), (ph_i_conversion, "i")],  # Conversion factor for phasor channels
                       [(1, "pow"), (1, "rms"), (1, "peak")],  # Conversion factor for analog channels
                       [(0x0000, 0xffff)],  # Mask words for digital status words
                       60,  # Nominal frequency
                       1,  # Configuration change count
                       30)  # Rate of phasor data transmission)

    hf = HeaderFrame(7,  # PMU_ID
                     "Hello I'm nanoPMU!")  # Header Message

    df = DataFrame(7,  # PMU_ID
                   ("ok", True, "timestamp", False, False, False, 0, "<10", 0),  # STAT WORD - Check DataFrame set_stat()
                   [(14635, 0), (-7318, -12676), (-7318, 12675), (1092, 0)],  # PHASORS (3 - v, 1 - i)
                   2500,  # Frequency deviation from nominal in mHz
                   0,  # Rate of Change of Frequency
                   [100, 1000, 10000],  # Analog Values
                   [0x3c12],  # Digital status word
                   cfg)  # Data Stream Configuration
    
    #cfg.set_time = functools.partial(set_time_slower, cfg)
    #hf.set_time = functools.partial(set_time_slower, hf)
    #df.set_time = functools.partial(set_time_slower, df)
    
    pmu.set_configuration(cfg)
    pmu.set_header(hf)

    pmu.run()

    while True:
        if pmu.clients:
            pmu.send(df)

    pmu.join()
