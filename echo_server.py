#python C:\Users\Eliot\Python\echo_server.py
import time
import select
import socket
import sys
import queue

host = ''   # Symbolic name, meaning all available interfaces
port = 12345 # Arbitrary non-privileged port

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

#Bind socket to local host and port
try:
    server.bind((host, port))
except socket.error as msg:
    sys.exit()

# Listen for incoming connections
server.listen(5)

# Sockets from which we expect to read
inputs = [ server ]

# Sockets to which we expect to write
outputs = [ ]

# Outgoing message queues (socket:Queue)
message_queues = {}

#usernames
names = {}
names[server] = "RESERVED!"


#main server loop
while inputs:

    # Wait for at least one of the sockets to be ready for processing
    #print("\nwaiting for the next event")
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    
    # Handle inputs
    for s in readable:
        # A "readable" server socket is ready to accept a connection
        if s is server:
            connection, client_address = s.accept()
            print("new connection from " + str(client_address))
            connection.setblocking(0)
            inputs.append(connection)
            # Give the connection a queue for data we want to send
            message_queues[connection] = queue.Queue()
        
        # A connection has been established with a client that sent data
        else:
            try:
                username = names[s]
                print(username)
                data = s.recv(1024).decode('ascii')
                if data:
                    # A readable client socket has data
                    if str(data)=="SERVER_KILL!":
                        server.close()
                        
                    elif str(data)=="SERVER_UPDATE!":
                        # Add output channel for response
                        if s not in outputs:
                            outputs.append(s)
                            
                    else:
                        print('received ' + str(data) + " from " + str(s.getpeername()))
                        for i in message_queues:
                            message_queues[i].put(username + "         " + time.ctime(time.time()) + ":\n" + data + "\n")
                        # Add output channel for response
                        if s not in outputs:
                            outputs.append(s)
                else:
                    outputs.append(s)
                    
            except KeyError:
                print("got username from" + str(s.getpeername()))
                s.send("Welcome to the chat room.".encode('ascii'))
                names[s] = s.recv(1024).decode('ascii')
                
    # Handle outputs
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            pass
        except KeyError:
            pass
        else:
            if next_msg != 'SERVER_UPDATE!':
                print('sending ' + next_msg + ' to ' + str(s.getpeername()))
                s.send(next_msg.encode('ascii'))
            
    # Handle "exceptional conditions"
    for s in exceptional:
        print('handling exceptional condition for ' + str(s.getpeername()))
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]

