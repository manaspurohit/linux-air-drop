import os
import socket
import struct

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

def prompt_user(clientsocket):
    # let client know we are ready to receive
    readyForNext(clientsocket)

    # get filename
    clientmsg = clientsocket.recv(bufsize)
    filename = clientmsg.decode('ascii')
    userresponse = ''
    while (userresponse != 'y' and userresponse != 'n'):
        # TODO: update with filename
        userresponse = input('Would you like to accept the following file (y/n): %s ' % filename)

    if (userresponse == 'n'):
        # TODO: send declined code to client
        clientsocket.send('declined'.encode('ascii'))
    else:
        newfilepath = 'placeholder'
        while (newfilepath != ''):
            try:
                newfilepath = input('Enter in the path for where you would like to save the file (/path/to/filename.txt): ')
                os.makedirs(os.path.dirname(newfilepath), exist_ok=True)
                readyForNext(clientsocket)
                receiveFile(clientsocket, newfilepath)
                return
            except:
                print('Invalid pathname!', flush=True)
                continue
