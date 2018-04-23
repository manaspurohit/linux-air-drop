import nmap
from neighborhood import get_subnet_sweep_params

port = 41779

def find_live_hosts():
    print('finding live hosts')
    nm = nmap.PortScanner()
    print('determining subnet block')
    subnet_sweep_params = get_subnet_sweep_params(True)
    print('sweeping on subnet: {0}'.format(subnet_sweep_params))

    # scan the subnet for live hosts
    port_str = '{0}-{0}'.format(port)

    args = '-sP'
    # args = '-n -sP -PE -PA21,' + str(port)
    nm.scan(hosts=subnet_sweep_params, arguments=args)
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    print(hosts_list)

find_live_hosts()
