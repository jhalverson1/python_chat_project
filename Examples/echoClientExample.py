# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 06:03:31 2018

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
# The server needs to create its own socket using the same protocols
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# set address to localhost and port to 10000
# bind is used here to 'connect' to own address
# connect (used by a client) is used here to 'connect' to a 'remote' address
address = ('localhost', 10000)
print >> sys.stdout, 'connecting to address: %s port: %s' % address
mySocket.connect(address)

try:
    # create and send message
    message = 'This is my message'
    print >> sys.stdout, 'sending "%s" ' % message
    mySocket.sendall(message)
    
    amountReceived = 0
    amountExpected = len(message)
    
    # listen and receive response until the number of bytes that we sent is received
    while amountReceived < amountExpected:
        data = mySocket.recv(15)
        amountReceived += len(data)
        print >> sys.stdout, 'received "%s" ' % data
    
finally:
    print >> sys.stdout, 'closing socket'
    mySocket.close()