import socket

def sendFile(clientsocket, filename):
    bufsize = 4096

    f = open(filename, 'r')

    more = "more".encode('ascii')

    data = f.read(bufsize)
    while data != '':
        clientsocket.send(more)
        encodeddata = data.encode('ascii')
        clientsocket.send(encodeddata)
        data = f.read(bufsize)

    clientsocket.send("end".encode('ascii'))

    f.close()
