import socket
import sys

if sys.argv[1] == "_direct":
    print("\nEntering Direct Mode...\n")

    # set port number
    portNumber = int(sys.argv[2])

    # set IP Address and port number string
    IpPortString = sys.argv[3]

    # socket.AF_INET means use address family inet (ip4)
    # socket.SOCK_STREAM means use TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # set address to localhost and port to 10000
    address = ('localhost', portNumber)
    print('connecting to address: %s port: %s\n' % address)

    # this client is in charge of hosting server
    if portNumber:
        # bind is used here to 'connect' to own address
        print("HOST")
        s.bind(address)

        # listen for incoming connections
        # parameter gives the number of connections to accept before refusing new connections
        s.listen(1)

        # repeatedly listen and wait for connections
        while True:
            # get connection.
            # accept blocks until a connection is received
            print('waiting for connection')
            clientSocket, clientAddress = s.accept()

            try:
                print('connected to ', clientAddress)

                # receive data from connection
                while True:
                    data = clientSocket.recv(16)
                    print('received "%s"' % data.decode('UTF-8'))
                    if data:
                        print('sending data back to client ')
                        clientSocket.sendall(data)
                    else:
                        print('all data received from ', clientAddress)
                        break
            finally:
                print('closing connection to ', clientAddress)
                clientSocket.close()

    # this client will connect to the other client's server
    else:
        print("CLIENT")
        # connect (used by a client) is used here to 'connect' to a 'remote' address
        s.connect(address)

        try:
            # create and send message
            message = input("Type Message:\n").encode('UTF-8')
            print('sending "%s" ' % message.decode('UTF-8'))
            s.sendall(message)

            amountReceived = 0
            amountExpected = len(message)

            # listen and receive response until the number of bytes that we sent is received
            while amountReceived < amountExpected:
                data = s.recv(15)
                amountReceived += len(data)
                print('received "%s" ' % data.decode('UTF-8'))

        finally:
            print('closing socket')
            s.close()


if sys.argv[1] == "_topic":
    print("\nEntering Indirect Mode...\n")

    # set IP Address and port number string
    IpPortString = sys.argv[2]

    # set the topic the user is interested in
    topic = sys.argv[3]