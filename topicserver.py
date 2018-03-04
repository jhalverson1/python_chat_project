"""
@author Jon Halverson
"""

import socket
import sys
import queue
import select
import json

print('...\n...\n...')


class Server:

    port = sys.argv[1]
    address = ('127.0.0.1', int(port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    inputs = [s]
    outputs = []
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
                    client_socket.setblocking(0)
                    self.inputs.append(client_socket)

                # connection has data for us
                else:
                    data = current_read.recv(4096)

                    # if there is data, send it to all clients in the sender's topic
                    if data:
                        json_data = json.loads(data.decode('utf-8'))

                        # register client
                        if len(json_data) == 2:
                            json_registration = json.loads(data.decode('utf-8'))
                            topic = json_registration['topics']
                            print(client_address, "connected to topic:", topic)
                            if topic in self.topic_dictionary:
                                self.topic_dictionary[topic].append(client_socket)
                            else:
                                self.topic_dictionary[topic] = [client_socket]

                        # process message
                        elif len(json_data) == 3:
                            message_topic = json_data["message"]["topic"]
                            message_text = json_data["message"]["text"]

                            # Uncomment to print message in server as well
                            # print(message_topic, ":", message_text)

                            # send message to all subscribers to the topic
                            for subscriber in self.topic_dictionary[message_topic]:
                                subscriber.sendall(data)

                    # if there is no data, close the connection
                    else:
                        self.inputs.remove(current_read)

                        # remove from topics list, the ugly solution
                        for topic in self.topic_dictionary:
                            for socket in self.topic_dictionary[topic]:
                                if socket == current_read:
                                    self.topic_dictionary[topic].remove(socket)

                        current_read.close()


server = Server()
server.run()

