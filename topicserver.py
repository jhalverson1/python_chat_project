
import socket
import sys
import queue
import select
import json

print('...\n...\n...')


class Server:
    port = sys.argv[2]
    address = ('127.0.0.1', int(port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    inputs = [s]
    outputs = []
    message_queue = {}
    topic_dictionary = {}

    def __init__(self):
        print('binding to address: %s port: %s' % self.address)
        self.s.bind(self.address)

        # listen for incoming connections
        self.s.listen(5)

    def run(self):
        print("running...")
        while True:

            # Wait for something to happen
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

                # connection has data for us
                else:
                    data = current_read.recv(4096)

                    # if there is data, send it to all clients in the sender's topic
                    if data:
                        json_data = json.loads(data.decode('utf-8'))
                        message_topic = json_data["message"]["topic"]
                        message_text = json_data["message"]["text"]
                        print(message_topic, ":", message_text)

                    # if there is no data, close the connection
                    else:
                        self.inputs.remove(current_read)
                        current_read.close()
                        del self.message_queue[current_read]



if sys.argv[1] == "-topic":
    server = Server()
    server.run()

if sys.argv[1] == "-direct":
    print("topicserver.py cannot be launched in -direct mode, try -topic.")
