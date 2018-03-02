"""
@author Jon Halverson
"""

import sys
import socket
import select
import queue


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
        # list of objects to check for incoming data to be read
        inputs = [self.s]
        # list of objects to check for outgoing data to be written
        outputs = []

        message_queue = {}

        # for each connection we are monitoring
        while inputs:

            # wait for something to happen
            readable, writable, exceptional = select.select(inputs, outputs, inputs)

            # loop through the list of readable objects
            for current_read in readable:

                # there is an incoming connection
                if current_read is self.s:
                    client_socket, client_address = current_read.accept()
                    print('\nNew connection from ', client_address, '\n')
                    client_socket.setblocking(0)
                    inputs.append(client_socket)

                    # keep a queue for data we want to send across the new connection
                    message_queue[client_socket] = queue.Queue()

                # a connection has data for us to read
                else:
                    data = current_read.recv(256)

                    # if there is data send it back to the client
                    if data:
                        print(data.decode('utf-8'))
                        message_queue[current_read].put(data)

                        #
                        if current_read not in outputs:
                            outputs.append(current_read)

                    # if there is no data (data is empty) just close the connection
                    else:
                        print('...closing connection to ', current_read.getpeername())

                        # remove from outputs if possible
                        if current_read in outputs:
                            outputs.remove(current_read)

                        # remove from inputs, close connection, and delete from message queue
                        inputs.remove(current_read)
                        current_read.close()
                        del message_queue[current_read]
                        print('\nWaiting for new connection...')

            # for each available connection with a pending write, write
            for current_write in writable:
                try:
                    msg = message_queue[current_write].get_nowait()

                # no messages waiting so remove from outputs
                except queue.Empty:
                    # print('output queue for ', current_write.getpeername(), ' is empty')
                    outputs.remove(current_write)

                # send message
                else:
                    # print('sending "%s" to %s' % (msg, current_write.getpeername()))
                    current_write.send(msg)


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


if int(sys.argv[2]):
    print('------------------- Server -------------------')
    server = Server()
    server.run()
else:
    print('------------------- Client -------------------')
    client = Client()