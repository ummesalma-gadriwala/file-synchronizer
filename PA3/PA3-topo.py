#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s7, h7)
    s7s6 = {'delay':'100'}
    net.addLink(s7, s6, cls=TCLink , **s7s6)
    s7s5 = {'delay':'100'}
    net.addLink(s7, s5, cls=TCLink , **s7s5)
    s7s4 = {'delay':'100'}
    net.addLink(s7, s4, cls=TCLink , **s7s4)
    s7s3 = {'delay':'100'}
    net.addLink(s7, s3, cls=TCLink , **s7s3)
    s7s2 = {'delay':'100'}
    net.addLink(s7, s2, cls=TCLink , **s7s2)
    s7s1 = {'delay':'100'}
    net.addLink(s7, s1, cls=TCLink , **s7s1)
    s1s2 = {'delay':'1000'}
    net.addLink(s1, s2, cls=TCLink , **s1s2)
    s2s3 = {'delay':'1000'}
    net.addLink(s2, s3, cls=TCLink , **s2s3)
    s3s4 = {'delay':'1000'}
    net.addLink(s3, s4, cls=TCLink , **s3s4)
    s4s5 = {'delay':'1000'}
    net.addLink(s4, s5, cls=TCLink , **s4s5)
    s5s6 = {'delay':'1000'}
    net.addLink(s5, s6, cls=TCLink , **s5s6)
    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s3)
    net.addLink(h4, s4)
    net.addLink(h5, s5)
    net.addLink(h6, s6)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s4').start([c0])
    net.get('s2').start([c0])
    net.get('s7').start([c0])
    net.get('s3').start([c0])
    net.get('s5').start([c0])
    net.get('s6').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

