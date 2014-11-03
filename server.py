import socket
import system

# Create a TCP/IP socket
sock = socket.socket(socke.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 6461)
print >>sys.stderr, 'start up on %s port %s' % server_address
sock.bind(server_address)

# list for incoming connectiosn
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Recieves the data in small chunkcs and retransmit it
        while True:
            data = connection.recv(16)
            print >>sys.stderr, 'recieved "%s"' % data
            if data:
                print >>sys.stderr, 'sending back to client'
                connection.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
    finally:
        # Clean up the connection
        connection.close()
