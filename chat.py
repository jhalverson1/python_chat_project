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

            print('connected to ', client_address)
            print('---------\n')

            # receive message from connection
            while True:
                readable, writable, exceptional = select.select([sys.stdin, client_socket], [], [])

                if sys.stdin in readable:
                    message = input(">>> ")
                    client_socket.sendall(bytes(message, 'utf-8'))

                if client_socket in readable:
                    data = client_socket.recv(4096)

                    if data:
                        print(data.decode('utf-8'))
                    else:
                        break


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
        try:

            while True:
                readable, writable, exceptional = select.select([sys.stdin, self.s], [], [])

                if sys.stdin in readable:
                    message = input(">>> ")
                    self.s.sendall(bytes(message, 'utf-8'))
                    # print("Client self.s", self.s)

                if self.s in readable:
                    message = self.s.recv(4096)
                    print(message.decode('utf-8'))
        finally:
            self.s.close()







                # amount_received = 0
                # amount_expected = len(message)
                #
                # # listen and receive response until the number of bytes that we sent is received
                # while amount_received < amount_expected:
                #     data = self.s.recv(4096)
                #     amount_received += len(data)
                #     print(data.decode('utf-8'))

if int(sys.argv[2]):
    print('------------------- Server -------------------')
    server = Server()
    server.run()
else:
    print('------------------- Client -------------------')
    client = Client()