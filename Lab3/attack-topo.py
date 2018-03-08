"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class AttTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

	cmd='/usr/sbin/sshd'
	opts='-D'

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        Attacker = self.addHost( 'att' )
        Victim = self.addHost( 'vic' )
        Legitimate = self.addHost( 'leg' )
        Switch = self.addSwitch( 's1' )

        # Add links
        self.addLink( Attacker, Switch )
        self.addLink( Legitimate, Switch )
        self.addLink( Switch, Victim )

topos = { 'att-topo': ( lambda: AttTopo() ) }
