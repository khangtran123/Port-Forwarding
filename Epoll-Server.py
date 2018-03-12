#! /usr/bin/python3
'''
File: Epoll-Server.py
Date: February 16, 2018
Designers: Huu Khang Tran, Anderson Phan
Description: This scripts covers edge-triggered server implementing the Epoll system.
             We will be handling connections using e-poll (edge-triggered) since
             it's more efficient in handling various numbers of clients.
'''

import socket
import select
import time
import sys
from socket import error as SocketError

exitFlag = 0
LineEnd1 = b"\n\n"
LineEnd2 = b"\n\r\n"
echoEnd = b'done'

global clientConnection
global serverSocket
global dataBuffer
global epoll
global dataReceive
global dataSent
global connections
global clientID
global output_file

connections = {}; clientID = {};

output_file = open('Epoll_Server-Output.txt','w')
dataBuffer = 2048
dataSent = 0
dataReceive = 0
clientConnection = 0
epoll = select.epoll()

# -------- Kill Server should be called on to output final result to file ---------
# s = socket created, opened, and initialized for when a client connects
# clientConnection = how many client sessions connect to this server
# recvMsg = total amount of data received from the client
# sentMsg = total amount of data sent back to the client
#def kill_server(s, clientConnection, recvMsg, sentMsg):
#    output_file = open('Multithreading_Server-Output.txt','w')

#    output_file.write("\n Total connections: " + str(clientConnection))
#    output_file.write("\n Total amount of data received from the client" + str(recvMsg))
#    output_file.write("\n Total amount of data sent to the client" + str(sentMsg))
    #now we have to close/end the session if the server was to be terminated
#    s.close()
#    print ("The client socket session is now closed.")
    #to avoid getting a SystemExit exception which can be viewed as an error,
    # we use sys.exit() to get around it
#    sys.exit()

#defining a function that will having all new connections that's coming to the server
def newConnection():
    global serverSocket
    global clientConnection
    global connections
    global clientID

    while True:
        try:
            clientSocket, clientAddress = serverSocket.accept()
            clientConnection += 1
            clientSocket.setblocking(0)
            connections.update({clientSocket.fileno(): clientSocket})
            clientID.update({clientSocket.fileno(): clientAddress})
            epoll.register(clientSocket, select.EPOLLIN | select.EPOLLET)
            print ("client connection received: \n" + str(clientAddress))
            output_file.write("\n The client machine is now connected with an ip address of: " + str(clientAddress))
        except:
            break

#defining a function that will handle incoming data and echo it back.
def dataEcho(fileno):
    global epoll
    global connections
    global clientID
    global dataSent
    global dataReceive
    global dataBuffer

    clientSocket = connections.get(fileno)
    try:
        data = clientSocket.recv(dataBuffer)
        dataReceive += len(data)
        if(data != "" and data != b"done"):
            print ("received data from a client " + str(clientID[fileno]) + " / message length: " + str(len(data)))
            clientSocket.sendall(data)
            dataSent += len(data)
        elif(data == b"done" or data == ""):
            print("Client reponse of finished, releasing client socket.")
            epoll.modify(clientSocket, select.EPOLLHUP | select.EPOLLET)
            clientSocket.shutdown(socket.SHUT_RDWR)
            #connections[fileno].close()
            #epoll.unregister(fileno)
            #clientSocket.close()
            #del connections[fileno]
    except SocketError as e:
        print ("socket error occured.")
        if e.errno != errno.ECONNRESET:
            raise
        pass

'''
Now we need to use locks to synchronize access to shared resources.
If you have multiple threads running at the same time who all needs resources,
a lock has to be aquired by the first thread which means other threads can't use
it until the first thread is done with it.
'''

def main():
    global serverSocket
    global epoll
    global connections
    global dataBuffer
    global dataReceive
    global dataSent
    global clientConnection

    #startTime = time.ctime(time.time())
    #start = time.time()
    # clientConnection is a list to keep track of all the clients who connect to this server
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = '0.0.0.0'
    port = 7005
    #listens up to 50 connections/clients. depending on how many incoming connections this may be raised
    epoll.register(serverSocket.fileno(), select.EPOLLIN | select.EPOLLET)
    connections.update({serverSocket.fileno(): serverSocket})
    serverSocket.bind((host,port))
    serverSocket.listen(socket.SOMAXCONN)
    serverSocket.setblocking(0)
    print ("Server Started")

    try:
        while True:
            events = epoll.poll(1)
            #listens on 1 second intervals
            for fileno, event in events:
                #accepts a new incoming connection
                if fileno == serverSocket.fileno():
                    newConnection()
                elif event & select.EPOLLIN:
                    #this is where epoll gets messages flagged as inbound
                    dataEcho(fileno)
                elif (event & select.EPOLLHUP) or (event & select.EPOLLERR):
                    #once echoing is done, close the socket connection
                    print("terminating used client resources")
                    epoll.unregister(fileno)
                    connections[fileno].close()
                    del connections[fileno]
				# This section will write to the file for client info
                output_file.write("\n Number of sessions: " + str(clientConnection))
				#if userOption == 'connect':

    except KeyboardInterrupt as e:
        # s = socket created, opened, and initialized for when a client connects
        # clientConnection = how many client sessions connect to this server
        # recvMsg = total amount of data received from the client
        # sentMsg = total amount of data sent back to the client
        #kill_server(s, clientConnection, 0, 0)
        print ("\n terminal interruption of server via control+c, \n shutting down server and server sockets")
        epoll.unregister(serverSocket.fileno())
        epoll.close()
        serverSocket.close()
        sys.exit(0)

		
if __name__ == "__main__": main()
