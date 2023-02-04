#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Mininet
from sgcontainernet.net import SGContainernet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')


exec(open("/home/sgsdn/sflow-rt/extras/sflow.py").read())
#net = Containernet(controller=Controller)
subnet = '10.0.0.0/8'
net = SGContainernet(controller=RemoteController, ipBase=subnet)
info('*** Adding controller\n')
c1 = net.addController('c1', ip='127.0.0.1', port=6633)

info('*** Adding docker containers\n')
vpn = net.addSGVPN('vpn', '10.0.0.87', subnet)

SGHosts = []
d1 = net.addSGHost('d1', ip='10.0.0.251') 
d2 = net.addSGHost('d2', ip='10.0.0.252')
SGHosts += [d1, d2]

s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
info('*** Creating links\n')
net.addLink(vpn, s1)
net.addLink(d1, s1)
net.addLink(s1, s2, cls=TCLink, bw=1)
net.addLink(s2, d2)

info('*** Starting network\n')
net.start()

for host in SGHosts:
    net.enableNAT(host, '10.0.0.87')

info('*** Testing connectivity\n')
net.ping([d1, d2])
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()

