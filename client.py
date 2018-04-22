import socket

bufsize = 4096

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 41779 # uncommonly used port

# connect the socket to host and port
clientsocket.connect((host, port))

# Wait for server response
# Receive no more than bufsize bytes
msg = clientsocket.recv(bufsize)

# Send to server
clientid = "This is the client"
encodedclientid = clientid.encode('ascii')
clientsocket.send(encodedclientid)

clientsocket.close()

print (msg.decode('ascii'))
