"""
@author Jon Halverson
"""

import sys
import socket
import select


class Server:
    port = int(sys.argv[2])
    address = ('127.0.0.1', port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):

        # bind server to address
        print('binding to address: %s port: %s' % self.address)
        self.s.bind(self.address)

        # listen for incoming connections
        self.s.listen(1)

    def run(self):
        # repeatedly listen and wait for connections
        while True:

            # accept blocks until a connection is received
            print('waiting for connection')
            client_socket, client_address = self.s.accept()

            try:
                print('connected to ', client_address)
                print('---------\n')

                # receive message from connection
                while True:
                    message = client_socket.recv(4096)
                    print(message.decode('utf-8'))
                    if message:
                        client_socket.sendall(message)
                    else:
                        print('all data received from ', client_address)
                        break
            finally:
                print('closing connection to ', client_address)
                client_socket.close()


class Client:
    addressList = [1, 0]
    if len(sys.argv) == 4:
        addressList = sys.argv[3].split(':')

    address = (addressList[0], int(addressList[1]))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        print('connecting to address: %s port: %s' % self.address)
        self.s.connect(self.address)
        self.run()

    def run(self):
        while True:
            readable, writable, exceptional = select.select([sys.stdin], [sys.stdout], [])
            if sys.stdout in writable:
                # create and send message
                message = input(">>> ")
                # print('sending "%s" ' % message)
                self.s.sendall(bytes(message, 'utf-8'))

                amount_received = 0
                amount_expected = len(message)

                # listen and receive response until the number of bytes that we sent is received
                while amount_received < amount_expected:
                    data = self.s.recv(4096)
                    amount_received += len(data)
                    print(data.decode('utf-8'))

            # finally:
            #     print('closing socket')
            #     self.s.close()



if int(sys.argv[2]):
    print('------------------- Server -------------------')
    server = Server()
    server.run()
else:
    print('------------------- Client -------------------')
    client = Client()