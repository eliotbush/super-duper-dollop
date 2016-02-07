import socket

ip = "10.0.0.69"
port = 50149

# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# Send the data
message = 'Hello, world'
print('Sending : "%s"' % message)
len_sent = s.send(message.encode('ascii'))

# Receive a response
response = s.recv(len_sent).decode('ascii')
print('Received: "%s"' % response)

# Clean up
s.close()