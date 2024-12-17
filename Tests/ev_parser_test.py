from socket import *
import sys
import time


# Set the socket parameters
host = "localhost"
port = 1514
buf = 1024
addr = (host,port)

# Create socket
UDPSock = socket(AF_INET,SOCK_DGRAM)

event = "Mar 10 10:00:10 avas named[6986]: client 127.0.0.1#55867: query: <somequerydata>"

start_time = time.time()
for i in range(1,10000):
    nevent = event + str(i)
    if(UDPSock.sendto(nevent.encode(),addr)):
            print("Sending event no:",i," '",nevent,"'.....")
print("--- %s seconds ---" % (time.time() - start_time))
# Close socket
UDPSock.close()