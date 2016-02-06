import socket
import sys

#server address/port
server_address = ('127.0.0.1', 10000)

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect socket to server port
print ('connecting to ' + str(server_address))
s.connect(server_address)
print ('username:')

#data = s.recv(1024).decode('ascii')
#print(data)
#message = input()
##send message
##print("sending " + message)
#s.send(message.encode('ascii'))
    
while True:
    message = input()
    
    #send message
    #print("sending " + message)
    s.send(message.encode('ascii'))

    #read response
    data = s.recv(1024).decode('ascii')
    print(data)
    if not data:
        print('closing socket' + str(s.getsockname))
        s.close()