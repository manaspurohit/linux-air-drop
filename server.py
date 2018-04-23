import socket
from receive import receiveFile

bufsize = 4096

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 41779 # uncommonly used port

# bind the socket to host and port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    # accept connections from outside
    (clientsocket, address) = serversocket.accept()

    # TODO: send server string
    msg = 'Connected to server!'
    encodedmsg = msg.encode('ascii')
    serverstringbytes = 0
    while (serverstringbytes != len(encodedmsg)):
        serverstringbytes = clientsocket.send(encodedmsg)

    # Receive from client
    clientmsg = clientsocket.recv(bufsize)
    print(clientmsg.decode('ascii'), flush=True)

    receiveFile(clientsocket, "poop.txt")

    clientsocket.close()
