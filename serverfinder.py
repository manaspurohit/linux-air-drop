import socket
import requests


port = 41779

url_ip = 'https://api.ipify.org/?format=json'
url_lookup = 'https://airdrop-lookup.herokuapp.com'

def find_lan_hosts():
    print('falling back to port sweep')
    import nmap
    from neighborhood import get_subnet_sweep_params

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

def get_internal_ip():
    return socket.gethostbyname(socket.gethostname())

def get_external_ip():
    r = requests.get('{0}/{1}'.format(url_lookup, 'heartbeat'))

    if r.status_code != 200:
        # no internet, nothing we can do
        return

    r = requests.get(url_ip)

    if r.status_code != 200:
        raise Exception('has internet connection, but ip lookup is down!')

    results = r.json()
    return results['ip']

def get_ips():
    return (get_external_ip(), get_internal_ip())

def register():
    r = requests.get('{0}/{1}'.format(url_lookup, 'heartbeat'))

    if r.status_code != 200:
        # no internet, don't bother trying to register
        print('failed to register daemon')
        return

    (external, internal) = get_ips()

    r = requests.get('{0}/{1}/{2}/{3}'.format(url_lookup, 'add', external, internal))

    if r.status_code != 200:
        print('failed to register daemon')
        return

    print('daemon registered')

def find_live_hosts():
    r = requests.get('{0}/{1}'.format(url_lookup, 'heartbeat'))

    if r.status_code != 200:
        return find_lan_hosts()

    (external, internal) = get_ips()

    r = requests.get('{0}/{1}/{2}'.format(url_lookup, 'lookup', external))

    results = r.json()

    live_list = results['results']

    # remove your own ip address from the list of results if it's present
    if internal in live_list:
        live_list.remove(internal)

    return live_list

def ask_host():
    hosts = find_live_hosts()
    print('the following computers are ready to recieve files:')

    for i in range(len(hosts)):
        print('{0}: {1}'.format(str(i + 1), hosts[i]))

    print('which one would you like to send to?')

    result = input()

    while not (result.isdigit() or (int(result) > 0 and int(result) <= len(hosts))):
        print('Invalid. Which host would you like to send to?')
        result = input()

    return hosts[int(result) - 1]
