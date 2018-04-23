import os
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

        clientmsg = clientsocket.recv(bufsize)

def readyForNext(clientsocket):
    clientsocket.send(next)

def prompt_user(clientsocket):
    userresponse = ''
    while (userresponse != 'y' and userresponse != 'n'):
        # TODO: update with filename
        userresponse = input('Would you like to accept the following file (y/n): %s ' % 'foo.txt')

    if (userresponse == 'n'):
        # TODO: send declined code to client
        clientsocket.send('declined'.encode('ascii'))
    else:
        newfilepath = 'placeholder'
        while (newfilepath != ''):
            try:
                newfilepath = input('Enter in the path for where you would like to save the file (/path/to/filename.txt): ')
                os.makedirs(os.path.dirname(newfilepath), exist_ok=True)
                # TODO: call receiveFile with newfilepath
                newfile = open(newfilepath, 'w')
                newfile.close()
                return
            except:
                print('Invalid pathname!', flush=True)
                continue
