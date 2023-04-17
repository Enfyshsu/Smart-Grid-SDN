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

exec(open("/home/sgsdn/workspace/sflow-rt/extras/sflow.py").read())
subnet = '10.0.0.0/8'
net = SGContainernet(controller=RemoteController, ipBase=subnet)

info('*** Adding controller\n')
c1 = net.addController('c1', ip='127.0.0.1', port=6633)

info('*** Adding docker containers\n')
vpn = net.addSGVPN('vpn', ip='10.0.0.250', mac='00:00:00:00:99:99', subnet=subnet)

SGHosts = []
p1 = net.addSGHost('p1', ip='10.0.0.1', mac='00:00:00:00:00:01')
#p2 = net.addPMUHost('p2', ip='10.0.0.2', mac='00:00:00:00:00:02')
#p3 = net.addSGHost('p3', ip='10.0.0.3', mac='00:00:00:00:00:03')
#p4 = net.addSGHost('p4', ip='10.0.0.4', mac='00:00:00:00:00:04')
#p5 = net.addSGHost('p5', ip='10.0.0.5', mac='00:00:00:00:00:05')

p6 = net.addPMUHost('p6', ip='10.0.0.6', mac='00:00:00:00:00:06')
#p7 = net.addSGHost('p7', ip='10.0.0.7', mac='00:00:00:00:00:07')
#p8 = net.addSGHost('p8', ip='10.0.0.8', mac='00:00:00:00:00:08')
#p9 = net.addSGHost('p9', ip='10.0.0.9', mac='00:00:00:00:00:09')
#p10 = net.addSGHost('p10', ip='10.0.0.10', mac='00:00:00:00:00:10')

p11 = net.addSGHost('p11', ip='10.0.0.11', mac='00:00:00:00:00:11')
#p12 = net.addPMUHost('p12', ip='10.0.0.12', mac='00:00:00:00:00:12')
#p13 = net.addSGHost('p13', ip='10.0.0.13', mac='00:00:00:00:00:13')
#p14 = net.addSGHost('p14', ip='10.0.0.14', mac='00:00:00:00:00:14')

d1 = net.addOpenPDCHost('d1', ip='10.0.0.15', mac='00:00:00:00:00:15')

#SGHosts += [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, d1]
SGHosts += [p1, p6, p11, d1]

info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
s3 = net.addSwitch('s3')
s4 = net.addSwitch('s4')

info('*** Creating links\n')
net.addLink(s1, vpn)

net.addLink(s1, p1)
#net.addLink(s1, p2)
#net.addLink(s1, p3)
#net.addLink(s1, p4)
#net.addLink(s1, p5)

net.addLink(s2, p6)
#net.addLink(s2, p7)
#net.addLink(s2, p8)
#net.addLink(s2, p9)
#net.addLink(s2, p10)

net.addLink(s3, p11)
#net.addLink(s3, p12)
#net.addLink(s3, p13)
#net.addLink(s3, p14)

net.addLink(s4, d1)

net.addLink(s1, s2)
net.addLink(s2, s3)
net.addLink(s3, s4)
#net.addLink(s1, s4)
# net.addLink(s3, s1, cls=TCLink, bw=1)

info('*** Starting network\n')
net.start()

for host in SGHosts:
    net.enableNAT(host, '10.0.0.250')

info('*** Testing connectivity\n')
#net.ping([p1, d1])
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()

