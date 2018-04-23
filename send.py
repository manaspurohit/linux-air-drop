import socket
import os
import struct
import hashlib

bufsize = 4096

def sendFile(clientsocket, filename):

    # wait for server to be ready
    waitForNext(clientsocket)

    # send filename and filesize
    filenameencoded = filename.encode('ascii')
    clientsocket.send(filenameencoded)
    if waitForNext(clientsocket) == False:
        return
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
        send_data(clientsocket, data)
        filesize = filesize - datasize
        if filesize == 0:
            break

    f.close()

def send_data(clientsocket, data):
    clientsocket.send(data)
    waitForNext(clientsocket)
    myhashlib = hashlib.md5()
    myhashlib.update(data)
    clientsocket.send(myhashlib.digest())
    if not waitForNext(clientsocket):
        send_data(clientsocket, data)

def waitForNext(clientsocket):
    clientmsg = clientsocket.recv(bufsize)
    next = clientmsg.decode('ascii')
    if next != "next":
        print(next)
        return False
    else:
        return True
