import socket
import struct

next = "next".encode('ascii')

def receiveFile(clientsocket, filename):
    bufsize = 4096

    # let client know we are ready to receive
    readyForNext(clientsocket)

    # get filesize
    clientmsg = clientsocket.recv(bufsize)
    filesize = struct.unpack("Q", clientmsg)[0]
    readyForNext(clientsocket)

    f = open(filename, 'wb')

    while True:
        datasize = 0
        if (filesize > bufsize):
            datasize = bufsize
        else:
            datasize = filesize

        clientmsg = clientsocket.recv(datasize)
        print(clientmsg)
        f.write(clientmsg)
        readyForNext(clientsocket)
        filesize = filesize - datasize
        if filesize == 0:
            break

    f.close()

def readyForNext(clientsocket):
    clientsocket.send(next)
