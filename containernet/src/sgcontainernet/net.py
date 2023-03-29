from mininet.net import Containernet

class SGContainernet(Containernet):
    def addSGHost(self, name, ip, mac):
        d = self.addDocker(name=name, ip=ip, mac=mac, dimage='sgsdn_host', ports=[22, 3000], cap_add=["NET_ADMIN"], dcmd='/init', network_mode='none', dns=['8.8.8.8'])
        d.cmd('./ssh_entrypoint.sh')
        return d

    def enableNAT(self, SGHost, gateway):
        SGHost.cmd('ip route add default via', gateway)

    def addSGVPN(self, name, ip, mac, subnet):
        d = self.addDocker(name=name, ip=ip, mac=mac, dimage='sgsdn_host', ports=[22], network_mode='bridge',cap_add=["NET_ADMIN"], sysctls={'net.ipv4.ip_forward':1}, dns=['8.8.8.8'])
        d.cmd('./ssh_entrypoint.sh')
        d.cmd('iptables -F')
        d.cmd('iptables -t nat -F')
        d.cmd('iptables -A FORWARD -i', name + '-eth0 -s', subnet, '-j ACCEPT')
        d.cmd('iptables -A FORWARD -i eth0 -d', subnet, '-j ACCEPT')
        d.cmd('iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE')
        return d

    def addPMUHost(self, name, ip, mac):
        d = self.addDocker(name=name, ip=ip, mac=mac, dimage='sgsdn_host', ports=[22, 3000], cap_add=["NET_ADMIN"], dcmd='/init', network_mode='none', dns=['8.8.8.8'])
        d.cmd('./ssh_entrypoint.sh')
        return d

    def addOpenPDCHost(self, name, ip, mac):
        d = self.addDocker(name=name, ip=ip, mac=mac, dimage='pdc_host', ports=[8500], network_mode='none', dns=['8.8.8.8'], dcmd='./init.sh')
        #d = self.addDocker(name=name, ip=ip, mac=mac, dimage='pdc_host', ports=[8500], network_mode='none', dns=['8.8.8.8'], volumes=['/home/sgsdn/workspace/containernet/service/pdc_host/volume/openPDC.db:/opt/openPDC/ConfigurationCache/openPDC.db'], dcmd='./init.sh')
        #d.cmd('/bin/bash')
        #d.cmd('./init.sh')
        return d

    def addTPHost(self, name, ip, mac):
        # d = self.addDocker(name=name, ip=ip, mac=mac, dimage='sgsdn_taipower', ports=[22, 3000], cap_add=["NET_ADMIN"], sysctls={'net.ipv4.tcp_rmem':20971520, 'net.ipv4.tcp_rmem':20971520}, dcmd='/init',  network_mode='none', dns=['8.8.8.8'], volumes=['/home/sgsdn/workspace/taipower/part1/sgpacket:/sgpacket'])
        d = self.addDocker(name=name, ip=ip, mac=mac, dimage='sgsdn_taipower', ports=[22, 3000], cap_add=["NET_ADMIN"], dcmd='/init',  network_mode='none', dns=['8.8.8.8'], volumes=['/home/sgsdn/workspace/taipower/part1/sgpacket:/sgpacket'])
        d.cmd('./ssh_entrypoint.sh')
        return d
