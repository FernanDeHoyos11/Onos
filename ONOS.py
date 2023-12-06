from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController

class MyLinearTopo(Topo):
    # Custom topology with flexible connections
    def __init__(self, ns, nh, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        switches = []
        hosts = []

        # Create switches
        for s in range(int(ns)):
            switches.append(self.addSwitch('s%s' % (s)))

        # Create hosts
        for h in range(int(nh)):
            hosts.append(self.addHost('h%s' % (h)))

        # Prompt user to make dynamic connections
        for s in range(int(ns)):
            choice = input(f"Seleccione hosts a conectar a switch s{s} (ejemplo: 0,1,2, o deje vacío): ")
            if choice:
                selected_hosts = [int(h) for h in choice.split(',')]
                for host_index in selected_hosts:
                    self.addLink(hosts[host_index], switches[s])

            dest = input(f"Seleccione switch a conectar con switch s{s} (ejemplo: 0, o deje vacío): ")
            if dest:
                self.addLink(switches[s], switches[int(dest)])

def runLinearTopo():
    ns = input('Ingrese número de Switch: ')
    nh = input('Ingrese número de Hosts: ')
    topo = MyLinearTopo(ns, nh)
    net = Mininet(topo, controller=None)  # Set controller to None to use external controller

    # Connect to ONOS controller
    onos_controller_ip = '192.168.1.116'  # Update with the actual IP of your ONOS controller
    onos_controller_port = 6653  # The default OpenFlow port used by ONOS
    net.addController('c0', controller=RemoteController, ip=onos_controller_ip, port=onos_controller_port)

    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    runLinearTopo()
