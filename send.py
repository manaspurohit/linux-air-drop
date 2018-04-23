import socket
import os
import struct

bufsize = 4096

def sendFile(clientsocket, filename):

    # wait for server to be ready
    waitForNext(clientsocket)

    # send filename and filesize
    filenameencoded = filename.encode('ascii')
    clientsocket.send(filenameencoded)
    waitForNext(clientsocket)
    filesize = os.path.getsize(filename)
    clientsocket.send(struct.pack("Q", filesize))
    waitForNext(clientsocket)

    f = open(filename, 'rb')

    while True:
        datasize = 0
        if filesize > bufsize:
            datasize = bufsize
        else:
            datasize = filesize

        data = f.read(datasize)
        clientsocket.send(data)
        waitForNext(clientsocket)
        filesize = filesize - datasize
        if filesize == 0:
            break

    f.close()

def waitForNext(clientsocket):
    clientmsg = clientsocket.recv(bufsize)
    next = clientmsg.decode('ascii')
    if next != "next":
        print(next)
