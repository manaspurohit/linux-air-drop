import socket
import struct

next = "next".encode('ascii')

def receiveFile(clientsocket):
    bufsize = 4096

    # let client know we are ready to receive
    readyForNext(clientsocket)

    # get filename and filesize
    clientmsg = clientsocket.recv(bufsize)
    filename = clientmsg.decode('ascii')
    readyForNext(clientsocket)
    clientmsg = clientsocket.recv(bufsize)
    filesize = struct.unpack("Q", clientmsg)[0]
    readyForNext(clientsocket)

    while True:
        datasize = 0
        if (filesize > bufsize):
            datasize = bufsize
        else:
            datasize = filesize

        clientmsg = clientsocket.recv(datasize)
        print(clientmsg)
        readyForNext(clientsocket)
        filesize = filesize - datasize
        if filesize == 0:
            break

def readyForNext(clientsocket):
    clientsocket.send(next)
