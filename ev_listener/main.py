from socket import *
import requests

# Set the socket parameters
host = 'localhost'
port = 1514
buf = 1024
addr = (host,port)

# Create socket and bind to address
UDPSock = socket(AF_INET,SOCK_DGRAM)
UDPSock.bind(addr)

headers = {'Content-Type': 'application/json'}

# Receive messages
while 1:
    data,addr = UDPSock.recvfrom(buf)
    if not data:
        print("Client has exited!")
        break
    else:
        requests.post('http://127.0.0.1:5001/events/parse', json={'event':data.decode("utf-8")}, headers=headers)
        print ("\nReceived message '", data.decode("utf-8"),"'")

# Close socket
UDPSock.close()
