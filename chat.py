"""
@author Jon Halverson
"""

import sys
import socket
import select
import json


class Server:
    port = 0
    if sys.argv[1] == '-direct':
        port = int(sys.argv[2])
    address = ('127.0.0.1', port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_address = ''

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
            print('waiting for connection...')
            client_socket, self.client_address = self.s.accept()

            # output for after connection
            print('------------------- Server -------------------')
            print('connected to address: %s port: %s ' % self.client_address)
            print('.....\n.....\n.....')

            # receive message from connection
            while True:
                readable, writable, exceptional = select.select([sys.stdin, client_socket], [], [])

                if sys.stdin in readable:
                    message = input('')
                    json_message = self.build_json_message("direct", message)
                    json_string = json.dumps(json_message)
                    client_socket.sendall(json_string.encode('utf-8'))

                if client_socket in readable:
                    data = client_socket.recv(4096)

                    if data:
                        json_data = json.loads(data.decode('utf-8'))
                        message_topic = json_data["message"]["topic"]
                        message_text = json_data["message"]["text"]
                        print(message_topic, ":", message_text)
                    else:
                        break

    def build_json_message(self, topic, text):

        # includes ip and port of the source
        source = {"ip": self.address,
                  "port": self.port
                  }

        # includes ip and port of the destination
        destination = {"ip": self.client_address[0],
                       "port": self.client_address[1]
                       }

        # includes message topic and message text
        message = {"topic": topic,
                   "text": text
                   }

        # configure json message
        json_message = {"source": source,
                        "destination": destination,
                        "message": message}

        return json_message


class ClientDirect:
    
    addressList = [1, 0]
    if len(sys.argv) == 4:
        addressList = sys.argv[3].split(':')
        if len(addressList) == 2:
            address = (addressList[0], int(addressList[1]))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        print('connecting to address: %s port: %s' % self.address)
        print('.....\n.....\n.....')
        self.s.connect(self.address)
        self.run()

    def run(self):
        try:

            # receive message from connection
            while True:
                readable, writable, exceptional = select.select([sys.stdin, self.s], [], [])

                if sys.stdin in readable:
                    message = input('')
                    source_port = self.s.getsockname()[1]
                    json_message = self.build_json_message("direct", message, source_port)
                    json_string = json.dumps(json_message)
                    self.s.sendall(json_string.encode('utf-8'))

                if self.s in readable:
                    data = self.s.recv(4096)

                    if data:
                        json_data = json.loads(data.decode('utf-8'))
                        message_topic = json_data["message"]["topic"]
                        message_text = json_data["message"]["text"]
                        print(message_topic, ":", message_text)
                    else:
                        break
        finally:
            self.s.close()

    def build_json_message(self, topic, text, source_port):

        # includes ip and port of the source
        source = {"ip": self.addressList[0],
                  "port": source_port
                  }

        # includes ip and port of the destination
        destination = {"ip": self.addressList[0],
                       "port": self.addressList[1]
                       }

        # includes message topic and message text
        message = {"topic": topic,
                   "text": text
                   }

        # configure json message
        json_message = {"source": source,
                        "destination": destination,
                        "message": message}

        return json_message


class ClientTopic:

    addressList = sys.argv[2].split(':')
    address = ('', 0)
    if len(addressList) == 2:
        address = (addressList[0], int(addressList[1]))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    topic = ''
    if len(sys.argv) == 4:
        topic = sys.argv[3]

    def __init__(self):
        print('Topic: ', self.topic)
        print('connecting to address: %s port: %s' % self.address)
        print('.....\n.....\n.....')
        self.s.connect(self.address)

        # register with new connection and send info
        source_port = self.s.getsockname()[1]
        json_registration = self.build_json_registration(self.topic, source_port)
        json_string = json.dumps(json_registration)
        self.s.sendall(json_string.encode('utf-8'))

        # run server
        self.run()

    def run(self):
        try:

            # receive message from connection
            while True:
                readable, writable, exceptional = select.select([sys.stdin, self.s], [], [])

                if sys.stdin in readable:
                    message = input('')
                    source_port = self.s.getsockname()[1]
                    json_message = self.build_json_message(self.topic, message, source_port)
                    json_string = json.dumps(json_message)
                    self.s.sendall(json_string.encode('utf-8'))

                if self.s in readable:
                    data = self.s.recv(4096)

                    if data:

                        json_data = json.loads(data.decode('utf-8'))
                        message_topic = json_data["message"]["topic"]
                        message_text = json_data["message"]["text"]
                        print(message_topic, ":", message_text)
                    else:
                        break
        finally:
            self.s.close()

    def build_json_message(self, topic, text, source_port):

        # includes ip and port of the source
        source = {"ip": self.addressList[0],
                  "port": source_port
                  }

        # includes ip and port of the destination
        destination = {"ip": self.addressList[0],
                       "port": self.addressList[1]
                       }

        # includes message topic and message text
        message = {"topic": topic,
                   "text": text
                   }

        # configure json message
        json_message = {"source": source,
                        "destination": destination,
                        "message": message}

        return json_message

    def build_json_registration(self, topic, source_port):

        # source includes ip and port
        source = {"ip": self.addressList[0],
                  "port": source_port
                  }

        # configure json message
        json_message = {"source": source,
                        "topics": topic
                        }

        return json_message


if sys.argv[1] == "-direct":
    # Port argument is a non-zero number
    if int(sys.argv[2]):
        print('------------------- Server -------------------')
        server = Server()
        server.run()

    # Port argument is 0
    else:
        print('------------------- Client -------------------')
        client = ClientDirect()

if sys.argv[1] == "-topic":
    print('------------------- Client -------------------')
    client = ClientTopic()
