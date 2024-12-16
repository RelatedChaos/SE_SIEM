from app import db
from app.models import Event
from socket import *





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
        e = Event(raw_event = data)
        database = get_db()
        print ("\nReceived message '", data,"'")
        database.session.add(e)
        database.session.commit()

        database.session.add(data)


# Close socket
UDPSock.close()
