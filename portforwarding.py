#!/bin/python3

'''
File: portforwarding.py
Date: March 11, 2018
Designers: Huu Khang Tran, Anderson Phan
Description: This script creates and deploys a network application that uses
             advanced TCP/IP Programming that implements "Port Forwarding"

Purpose: Design and implement a port forwarding server that will forward
         incoming connection requests to specific ports/services from any
         IP address, to any user-specified IP address and port. For example,
         an inbound connection from 192.168.1.5 to port 80 may be forwarded
         to 192.168.1.25, port 80, or to 192.168.1.25, port 8005.

Constraints
1) Forward any IP: port pair to any other user-specified IP: port pair.
2) The application must support multiple inbound connection requests,
   as well as simultaneous two-way traffic.
3) Only TCP connections will be forwarded by the basic implementation.
4) You are required to provide a detailed test case that will document the
   complete functionality of the port forwarding application. For example,
   beyond the basic functionality tests you may want to test and see how
   well your application performs under a heavy load, i.e., heavy throughput
   from multiple clients.
5) Your application will read the IP: port combinations to forward to from
   a separate configuration file.

Think of this as the middle man, we will read from a text file to transfer pkts
to client
'''

import socket
import threading
import time
import sys
import os

recvMsg = 0
sentMsg = 0
sourceIP = []
sourcePort = []
destIP = []
destPort = []
ListofConnections = []
config_file = "/root/Documents/Actual_Final_Code/config-file.txt"

# s = socket created, opened, and initialized for when a client connects
# clientConnection = how many client sessions connect to this server
# recvMsg = total amount of data received from the client
# sentMsg = total amount of data sent back to the client
def kill_server(s, clientConnection, recvMsg, sentMsg, output_file):

    output_file.write("\n Total connections: " + str(clientConnection))
    output_file.write("\n Total amount of data received from the client: " + str(recvMsg) + " Bytes")
    output_file.write("\n Total amount of data sent to the client: " + str(sentMsg) + " Bytes")
    #now we have to close/end the session if the server was to be terminated
    s.close()
    print ("\n The client socket session is now closed.")
    print ("\n")
    print ("---------------Results---------------")
    print ("\n Total connections: " + str(clientConnection))
    print ("\n Total amount of data received from the client: " + str(recvMsg) + " Bytes")
    print ("\n Total amount of data sent to the client: " + str(sentMsg) + " Bytes")
    #to avoid getting a SystemExit exception which can be viewed as an error,
    # we use sys.exit() to get around it
    sys.exit()


'''
This function gets called by the readFromFile() where it takes each line of text
in the file
Line in text should look like this: What this function sees
192.168.0.11:7005, 192.168.0.12:7006
'''
def splitByDelimiter(line):
    # we need to split lines in the txt file based on a comma delimiter that
    # splits up the host and it's client (destination)
    # 0 = host address:port
    # 1 = destination address:port
    segment = line.split(",")
    host = segment[0].split(":")
    sourceAddress = host[0]
    sourcePortNum = host[1]
    client = segment[1].split(":")
    #  lstrip() removes any leading white spaces in a given string segment
    destAddress = client[0].lstrip()
    destPortNum = client[1]
    #  remove all spaces and special characters after the last set of strings in the text file
    destPortNum = destPortNum.strip(' \t\n\r')

    return sourceAddress, sourcePortNum, destAddress, destPortNum


'''
Function readFromFile: Reads from the text file that contains the
                       sourceAddress:sourceIP +
                       destinationAddress:destinationPort
Text File
192.168.0.11:7005, 192.168.0.12:7006
'''
def readFromFile():
    global sourceIP
    global sourcePort
    global destIP
    global destPort
    text_file = open(config_file,"r")
    # now we iterate through each line in config-file and call on the splitByDelimiter() to get the segments
    for line in text_file:
        sourceAddr, sourcePt, destAddr, destPt = splitByDelimiter(line)

        sourceIP.append(sourceAddr)
        sourcePort.append(sourcePt)
        destIP.append(destAddr)
        destPort.append(destPt)

        print ("Source IP Address: " + str(sourceIP))
        print ("Source Port Number: " + str(sourcePort))
        print ("Destination IP Address" + str(destIP))
        print ("Destination Port Number: " + str(destPort))
        #  now we want to make an instance of a specific network
        network = Network(sourceAddr, sourcePt, destAddr, destPt)
        #  once we create this instance, we will add it to the list of current connections
        ListofConnections.append(network)


'''
Class: Network
Purpose: We want to create an object reference that will hold these attributes
         that represents a specific network connection between two different
         client machines. In our config file, we can have more than two sets
         of network interfaces trying to communicate with one another. If
         more are added --> will create a new object reference for it.
'''
class Network(object):
    sourceIP = ""
    sourcePort = ""
    destIP = ""
    destPort = ""

    def __init__(self, sourceIP, sourcePort, destIP, destPort):
        self.sourceIP = sourceIP
        self.sourcePort = sourcePort
        self.destIP = destIP
        self.destPort = destPort


'''
Function echoData: Taken from our previous assignment, this function simply
                           echos the data to the destined machine. What's different
                           now is that we will be accepting sockets from both the
                           client and server as this Port Forward Server acts as
                           a middle man

destinationSocket --> established socket connection with the Server
destinationProfile --> The server's IP address and Port number
recvMsg --> The counter to check how many messages came through this machine
sentMsg --> The counter to check how many messages were forwarded both to the client and Server
output_file --> the countermeasures in writing to the text file
clientSocket --> established socket connection with the client machines
clientAddress --> The client's IP Address and Port number
clientConnection --> The counter that uniquely identifies the client
'''
def echoData(destinationSocket, destinationProfile, recvMsg, sentMsg, output_file, clientSocket, clientAddress, clientConnection):
    #declaring these as global variables so it can be accessed in another function
    #global recvMsg
    #global sentMsg

    print ("Thread is online")
    #this makes sure the server is always receiving a message from the client
    #purpose of an echo server
    while True:
        # Server receives msg from client
        data = clientSocket.recv(2048)
        actualData = data.decode()
        totalLenData = len(data)
        recvMsg += totalLenData
        #if the data received is greater than 0 bytes, send it back to the client
        if totalLenData > 0:
            if actualData != 'done':
                print ("Data received from client # " + str(clientConnection) + " --> " + str(recvMsg) + " Bytes")
                output_file.write("\n Data received from the client # " + str(clientConnection) + " --> " + str(recvMsg) + " Bytes")
                destinationSocket.send(data)
                print ("Data sent back to client # " + str(clientConnection) + " --> " + str(sentMsg) + " Bytes")
                totalSentData = len(data)
                sentMsg += totalSentData
                output_file.write("Data sent back to client # " + str(clientConnection) + " --> " + str(sentMsg) + " Bytes")
                #output_file.write("\n Data sent to the client: " + str(sentMsg) + " Bytes")
            else:
                clientSocket.close()
                print ("Client has terminated the session")
        else:
            print ("Client message was null")


def startThread(networkProfile, portforwarderAddress, portforwarderPort):
    #startTime = time.ctime(time.time())
    #start = time.time()
    # clientConnection is a list to keep track of all the clients who connect to this server
    clientConnection = 0
    output_file = open('Multithreading_Server-Output.txt','w')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((portforwarderAddress, portforwarderPort))
    #lock = threading.Lock()

    print ("Server Started")
    #destPortNumber = int(str(connection.destPort))
    #print (float(int(connection.destPort)))
    #listens up to 50 connections/clients
    s.listen(socket.SOMAXCONN)

    try:
        while True:
            # accept() accepts an incoming connection
            clientSocket, clientAddress = s.accept()
            destinationSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # we use connect() instead of bind() here becuase we are not binding a local server but rather conenct to the destination server that is remote from this computer
            destPortNumber = int(networkProfile.destPort)
            destinationProfile = (networkProfile.destIP, destPortNumber)
            destinationSocket.connect(destinationProfile)
            print ("The client machine is now connected with an ip address of: " + str(networkProfile.destIP))
            #userOption is the data recieved from the client: client is to send data in a string of either
            #"get", "send", or "q"
            #userOption = clientSocket.recv(1024)
            # This section will write to the file for client info
            #output_file.write("\n The client machine is now connected with an ip address of: " + str(clientAddress) + " --> ID# " + str(clientConnection))
            clientConnection += 1
            # output_file.write("\n Number of sessions: " + str(clientConnection))
            #threadFromClient happening when the client is sending data to the portforwarder and then to the server
            #threadFromServer is happening when the server is sending data back to the forwarder and then back to the client
            threadFromClient = threading.Thread(target=echoData, args=(destinationSocket, destinationProfile, recvMsg, sentMsg, output_file, clientSocket, clientAddress, clientConnection))
            threadFromServer = threading.Thread(target=echoData, args=(clientSocket, clientAddress, recvMsg, sentMsg, output_file, destinationSocket, destinationProfile, clientConnection))
            #  now since this is a server that should always stay online, if a thread was to be killed
            #  the daemon should still be active for other clients
            threadFromClient.setDaemon(True)
            threadFromServer.setDaemon(True)
            threadFromClient.start()
            threadFromServer.start()

    except KeyboardInterrupt:
        # s = socket created, opened, and initialized for when a client connects
        # clientConnection = how many client sessions connect to this server
        # recvMsg = total amount of data received from the client
        # sentMsg = total amount of data sent back to the client
        kill_server(s, clientConnection, recvMsg, sentMsg, output_file)


if __name__ == "__main__":
    print("Welcome Bitches!! This is our Port Forwarder!")
    readFromFile()
    portforwarderAddress = "192.168.0.11"
    portforwarderPort = 7007
    for networkProfile in ListofConnections:
        #print ("This is the port number of destination server: " + networkProfile.destPort)
        pwThreadServer = threading.Thread(target=startThread, args=(networkProfile, portforwarderAddress, portforwarderPort))
        pwThreadServer.start()
