"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's3' )
        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( leftHost, leftSwitch, bw=10, delay='5ms' )
        self.addLink( leftSwitch, rightSwitch, bw=2, delay='2ms' )
        self.addLink( rightSwitch, rightHost, bw=10, delay='5ms' )

        '''
        1 - h1-s3 bw = 10, delay = 5
        2 - s4-h2 bw = 10, delay = 5
        3 - s3-s4 bw = 2, delay = 2
        '''



topos = { 'mytopo': ( lambda: MyTopo() ) }
