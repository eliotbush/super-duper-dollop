import socket
import sys

server_address = ('127.0.0.1', 10000)

# Create a TCP/IP socket
socks = [ socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          ]

# Connect the socket to the port where the server is listening
#print >>sys.stderr, 'connecting to %s port %s' % server_address
for s in socks:
    s.connect(server_address)
    
for message in messages:

    # Send messages on both sockets
    for s in socks:
        #print >>sys.stderr, '%s: sending "%s"' % (s.getsockname(), message)
        print("sending " + message)
        s.send(message.encode('ascii'))

    # Read responses on both sockets
    for s in socks:
        data = s.recv(1024).decode('ascii')
        print("received " + data)
        #print >>sys.stderr, '%s: received "%s"' % (s.getsockname(), data)
        if not data:
            #print >>sys.stderr, 'closing socket', s.getsockname()
            print('closing socket' + str(s.getsockname))
            s.close()