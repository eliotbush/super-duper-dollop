import socket
import sys
import time
import threading

def send_message(s):
    #global s
    while True:
        #send message
        message = input()
        s.send(message.encode('ascii'))
        
def get_update(s):
    while True:
        s.send("UPDATE!".encode('ascii'))
        time.sleep(5)
    
    

#server address/port
server_address = ('10.0.0.69', 12345)

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect socket to server port
print ('connecting to ' + str(server_address))
s.connect(server_address)
print ('username:')
t_prev = time.clock()
while True:      
    getInput = threading.Thread(name='input', target=send_message(s))
    updateText = threading.Thread(name='update', target=get_update)
    getInput.start()
    updateText.start()

    #read response
    data = s.recv(1024).decode('ascii')
    print(data)
    if not data:
        print('closing socket' + str(s.getsockname))
        s.close()