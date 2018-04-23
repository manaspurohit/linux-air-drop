import os
import socket

def receiveFile(clientsocket, filename):
    bufsize = 4096

    clientmsg = clientsocket.recv(bufsize)

    more = "more"

    while clientmsg.decode('ascii') == more:
        clientmsg = clientsocket.recv(bufsize)
        print(clientmsg.decode('ascii'), flush=True)

        clientmsg = clientsocket.recv(bufsize)

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
