from socket import *
import sys

# Set the socket parameters
host = "localhost"
port = 1514
buf = 1024
addr = (host,port)

# Create socket
UDPSock = socket(AF_INET,SOCK_DGRAM)

def_msg = "===Enter message to send to server===";
print("\n",def_msg)

# Send messages
while (1):
    data = input()
    if not data:
        break
    else:
        if(UDPSock.sendto(data.encode(),addr)):
            print("Sending message '",data,"'.....")

# Close socket
UDPSock.close()