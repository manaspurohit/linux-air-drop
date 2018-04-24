import socket
from send import sendFile
import serverfinder
import sys
import os.path

bufsize = 4096

DEBUG = False

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 41779 # uncommonly used port

connected = False

while not connected:
    host = socket.gethostname() if DEBUG else serverfinder.ask_host()

    print('attempting to connect to ' + host)

    # connect the socket to host and port
    try:
        clientsocket.connect((host, port))
        connected = True
    except:
        print('could not connect to ' + host + '\n')


# Wait for server response
# Receive no more than bufsize bytes
msg = clientsocket.recv(bufsize)

# Send to server
clientid = "This is the client"
encodedclientid = clientid.encode('ascii')
clientsocket.send(encodedclientid)

filename = sys.argv[1]
print(filename)
if not os.path.isfile(filename):
    print("file not found!")
else:
    sendFile(clientsocket, filename)

clientsocket.close()
