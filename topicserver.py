
import socket
import sys
import queue
import select

print('...\n...\n...')


class Server:
    port = sys.argv[2]
    address = ('127.0.0.1', int(port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    inputs = [s]
    outputs = []
    message_queue = {}

    def __init__(self):
        print('binding to address: %s port: %s' % self.address)
        self.s.bind(self.address)

        # listen for incoming connections
        self.s.listen(5)

    def run(self):
        print("running...")
        while True:

            # Wait for something to happen
            print('Waiting...')
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)

            # loop through list of readable objects
            for current_read in readable:

                # there is an incoming connection
                if current_read is self.s:
                    client_socket, client_address = current_read.accept()
                    print('New connection from ', client_address)
                    client_socket.setblocking(0)
                    self.inputs.append(client_socket)
                    print("Number of Connections Outside Connections: ", len(self.inputs) - 1)

                    # keep a queue for data we want to send across the new connection
                    self.message_queue[client_socket] = queue.Queue()






if sys.argv[1] == "-topic":
    server = Server()
    server.run()

if sys.argv[1] == "-direct":
    print("topicserver.py cannot be launched in -direct mode, try -topic.")
