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

subnet = '10.0.0.0/8'
net = SGContainernet(controller=RemoteController, ipBase=subnet)

info('*** Adding controller\n')
c1 = net.addController('c1', ip='127.0.0.1', port=6633)

info('*** Adding docker containers\n')
vpn = net.addSGVPN('vpn', ip='10.0.0.250', subnet=subnet)

SGHosts = []
e1 = net.addSGHost('e1', ip='10.0.1.211')
e2 = net.addSGHost('e2', ip='10.0.1.212')
e3 = net.addSGHost('e3', ip='10.0.1.213')
d1 = net.addSGHost('d1', ip='10.0.1.221')
v1 = net.addSGHost('v1', ip='10.0.1.231')

e4 = net.addSGHost('e4', ip='10.0.2.211')
e5 = net.addSGHost('e5', ip='10.0.2.212')
e6 = net.addSGHost('e6', ip='10.0.2.213')
d2 = net.addSGHost('d2', ip='10.0.2.221')
v2 = net.addSGHost('v2', ip='10.0.2.231')

e7 = net.addSGHost('e7', ip='10.0.3.211')
e8 = net.addSGHost('e8', ip='10.0.3.212')
e9 = net.addSGHost('e9', ip='10.0.3.213')
d3 = net.addSGHost('d3', ip='10.0.3.221')
v3 = net.addSGHost('v3', ip='10.0.3.231')

SGHosts += [e1, e2, e3, d1, v1, e4, e5, e6, d2, v2, e7, e8, e9, d3, v3]

info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
s3 = net.addSwitch('s3')

info('*** Creating links\n')
net.addLink(s1, vpn)

net.addLink(s1, e1)
net.addLink(s1, e2)
net.addLink(s1, e3)
net.addLink(s1, d1)
net.addLink(s1, v1)

net.addLink(s2, e4)
net.addLink(s2, e5)
net.addLink(s2, e6)
net.addLink(s2, d2)
net.addLink(s2, v2)

net.addLink(s3, e7)
net.addLink(s3, e8)
net.addLink(s3, e9)
net.addLink(s3, d3)
net.addLink(s3, v3)

net.addLink(s1, s2, cls=TCLink, bw=1)
net.addLink(s2, s3, cls=TCLink, bw=1)
# net.addLink(s3, s1, cls=TCLink, bw=1)

info('*** Starting network\n')
net.start()

for host in SGHosts:
    net.enableNAT(host, '10.0.0.250')

info('*** Testing connectivity\n')
net.ping([d1, d2])
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()

