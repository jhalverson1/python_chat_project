# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 6:25:13 2018

@author: ryanbrummet
"""

import socket
import sys
import select
import Queue

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

# unlike the previous example, we set the socket to be unblocking
mySocket.setblocking(0)

# set address to localhost and port to 10000
# bind is used here to 'connect' to own address
# connect (used by a client) is used here to 'connect' to a 'remote' address
address = ('localhost', 10000)
print >> sys.stdout, 'binding to address: %s port: %s' % address
mySocket.bind(address)

# listen for incoming connections
# parameter gives the number of connections to accept before refusing new connections
mySocket.listen(5)

# select takes 3 (technically 4 but the forth is optional; optional param is the number of seconds to wait) params
# (1) list of objects to check for incoming data to be read
# (2) list of objects to check for outgoing data to be written
# (3) sub list of objects from 1 and 2 that may have errors (generally not needed, we just use input)
inputs = [ mySocket ]
outputs = [ ]

# ignore for now, we'll use this in a bit
messageQueue = {}

# for each connection we are monitoring
while inputs:
    
    # wait for something to happen
    print >> sys.stdout, 'Waiting'
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    
    # loop through the list of readable objects
    for currentRead in readable:
        
        # there is an incoming connection
        if currentRead is mySocket:
            connection, clientAddress = currentRead.accept()
            print(type(connection))
            print >> sys.stdout, 'New connection from ', clientAddress
            connection.setblocking(0)
            inputs.append(connection)
            
            # keep a queue for data we want to send across the new connection
            messageQueue[connection] = Queue.Queue()
        
        # a connection has data for us to read            
        else:
            data = currentRead.recv(256)
            
            # if there is data send it back to the client
            if data:
                print >> sys.stdout, 'received "%s"' % data
                messageQueue[currentRead].put(data)
                
                #
                if currentRead not in outputs:
                    outputs.append(currentRead)
            
            # if there is no data (data is empty) just close the connection
            else:
                print >> sys.stdout, 'closing connection to ', currentRead.getpeername()
                
                # remove from outputs if possible
                if currentRead in outputs:
                    outputs.remove(currentRead)
                
                # remove from inputs, close connection, and delete from message queue
                inputs.remove(currentRead)
                currentRead.close()
                del messageQueue[currentRead]
                
    # for each available connection with a pending write, write
    for currentWrite in writable:
        try:
            msg = messageQueue[currentWrite].get_nowait()
        
        # no messages waiting so remove from outputs
        except Queue.Empty:
            print >> sys.stdout, 'output queue for ', currentWrite.getpeername(), ' is empty'
            outputs.remove(currentWrite)
            
        # send message
        else:
            print >> sys.stdout, 'sending "%s" to %s' % (msg, currentWrite.getpeername())
            currentWrite.send(msg)
            
            