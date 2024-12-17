from socket import *
from flask import request





# Set the socket parameters
host = 'localhost'
port = 1514
buf = 1024
addr = (host,port)

# Create socket and bind to address
UDPSock = socket(AF_INET,SOCK_DGRAM)
UDPSock.bind(addr)



# Receive messages
while 1:
    data,addr = UDPSock.recvfrom(buf)
    if not data:
        print("Client has exited!")
        break
    else:
        print ("\nReceived message '", data,"'")
        request.post()


# Close socket
UDPSock.close()
