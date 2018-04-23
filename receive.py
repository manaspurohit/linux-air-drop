import socket

def receiveFile(clientsocket, filename):
    bufsize = 4096

    clientmsg = clientsocket.recv(bufsize)

    more = "more"

    while clientmsg.decode('ascii') == more:
        clientmsg = clientsocket.recv(bufsize)
        print(clientmsg.decode('ascii'), flush=True)

        clientmsg = clientsocket.recv(bufsize)
