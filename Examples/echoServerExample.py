# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 05:46:24 2018

@author: ryanbrummet
"""

import socket
import sys

print >> sys.stdout, '...'
print >> sys.stdout, '...'
print >> sys.stdout, '...'

# create socket with ip4 address and TCP transport layer
# socket.AF_INET means use address family inet (ip4)
# socket.SOCK_STREAM means use TCP
#
# This only CREATES one socket, we need to bind it to an address
# The client needs to create its own socket using the same protocols
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set address to localhost and port to 10000
# bind is used here to 'connect' to own address
# connect (used by a client) is used here to 'connect' to a 'remote' address
address = ('localhost', 10000)
print >> sys.stdout, 'binding to address: %s port: %s' % address
mySocket.bind(address)

# listen for incoming connections
# parameter gives the number of connections to accept before refusing new connections
mySocket.listen(1)

# repeatedly listen and wait for connections
while True:
    # get connection.
    # accept blocks until a connection is received
    print >> sys.stdout, 'waiting for connection'
    connection, clientAddress = mySocket.accept()
    
    try:
        print >> sys.stdout, 'connected to ', clientAddress
        
        # receive data from connection
        while True:
            data = connection.recv(16)
            print >> sys.stdout, 'received "%s"' % data
            if data:
                print >> sys.stdout, 'sending data back to client '
                connection.sendall(data)
            else:
                print >> sys.stdout, 'all data received from ', clientAddress
                break
    finally:
        print >> sys.stdout, 'closing connection to ', clientAddress
        connection.close()