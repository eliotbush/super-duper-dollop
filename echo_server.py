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
                    ## Interpret empty result as closed connection
                    ##print >>sys.stderr, 'closing', client_address, 'after reading no data'
                    #print('closing ' + str(client_address) + ' after reading no data')
                    ## Stop listening for input on the connection
                    #if s in outputs:
                        #outputs.remove(s)
                    #inputs.remove(s)
                    #s.close()
    
                    ## Remove message queue
                    #del message_queues[s] 
                    
            except KeyError:
                print("waiting on username")
                s.send("Welcome to the chat room.".encode('ascii'))
                names[s] = s.recv(1024).decode('ascii')
                
    # Handle outputs
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            pass
            # No messages waiting so stop checking for writability.
            #print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
            #print('output queue for ' + str(s.getpeername()) + ' is empty')
            #outputs.remove(s)
        except KeyError:
            pass
        else:
            #print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
            if next_msg != 'SERVER_UPDATE!':
                print('sending ' + next_msg + ' to ' + str(s.getpeername()))
                s.send(next_msg.encode('ascii'))
            
    # Handle "exceptional conditions"
    for s in exceptional:
        #print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
        print('handling exceptional condition for ' + str(s.getpeername()))
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]


#conn, addr = s.accept()
##print(str(addr) + " connecting...")
#username = conn.recv(1024).decode('ascii')
##print("User " + username + " " + str(addr) + " connected.")
#while True:
    #data = conn.recv(1024).decode('ascii')
    ##print("received from " + username + " " + str(addr) + " at " + time.ctime(time.time()) + ": " + data)
    #send_message(conn, username, data)
#conn.close()

