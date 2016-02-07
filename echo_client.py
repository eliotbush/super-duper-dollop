import socket
import sys

#server address/port
server_address = ('10.0.0.69', 12345)

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect socket to server port
print ('connecting to ' + str(server_address))
s.connect(server_address)
print ('username:')

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
