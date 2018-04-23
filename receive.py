import os
import socket
import struct
import hashlib

next = "next".encode('ascii')
bufsize = 4096

def receiveFile(clientsocket, filepath):
    # get filesize
    clientmsg = clientsocket.recv(bufsize)
    filesize = struct.unpack("Q", clientmsg)[0]
    readyForNext(clientsocket)

    f = open(filepath, 'wb')

    while True:
        datasize = 0
        if (filesize > bufsize):
            datasize = bufsize
        else:
            datasize = filesize

        receive_data(clientsocket, f, datasize)

        filesize = filesize - datasize
        if filesize == 0:
            break

    print("done")
    f.close()

def receive_data(clientsocket, file, datasize):
    clientmsg = clientsocket.recv(datasize)
    readyForNext(clientsocket)
    hash = clientsocket.recv(bufsize)
    myhashlib = hashlib.md5()
    myhashlib.update(clientmsg)
    if hash != myhashlib.digest():
        clientsocket.send("hash doesn't match".encode('ascii'))
        receive_data(clientsocket, file, datasize)
    else:
        file.write(clientmsg)
        readyForNext(clientsocket)

def readyForNext(clientsocket):
    clientsocket.send(next)

def prompt_user(clientsocket):
    # let client know we are ready to receive
    readyForNext(clientsocket)

    # get filename
    clientmsg = clientsocket.recv(bufsize)
    filename = clientmsg.decode('ascii')
    userresponse = ''
    while (userresponse != 'y' and userresponse != 'n'):
        userresponse = input('Would you like to accept the following file (y/n): %s ' % filename)

    if (userresponse == 'n'):
        clientsocket.send('declined'.encode('ascii'))
    else:
        newfilepath = 'placeholder'
        while True:
            try:
                newfilepath = input('Enter in the path for where you would like to save the file (/path/to/filename.txt): ')
                os.makedirs(os.path.expanduser(os.path.dirname(newfilepath)), exist_ok=True)
            except:
                print('Invalid pathname!', flush=True)
                continue

            readyForNext(clientsocket)
            receiveFile(clientsocket, os.path.expanduser(newfilepath))
            return
