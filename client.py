#!/bin/python2

'''
File: client.py
Date: March 30, 2018
Designers: Huu Khang Tran, Anderson Phan
Description: This scripts covers the general client that will spawn a bunch of
             other clients to connect to either the multi-threaded, select, or
             epoll servers.
'''

import threading
import socket
import sys
import time
import os
import random
from signal import signal, SIGPIPE, SIG_DFL

global output_file
global clients
global echoedNUM
global RTT
global totalRTT
global avgRTT
global totalMessages
global totalRequests
#  totalRequests - How many requests meaning connections and echoes included towards the server
global totalRequests

#  THis function invokes multi-threading to create multiple clients
def spawn_clients(machineAddr, clients, portForwarderAddr, portForwarderPort, echoedMsg, echoedNUM, totalRequests, output_file):
    threadQueue = []
    clientID = 1
    totalMessages = ""
    totalRTT = 0
    for i in range(clients):
        #  threading.Thread() starts a new thread and passes in args
        thread = threading.Thread(target=start_engine, args=(i, machineAddr, clients, portForwarderAddr, portForwarderPort, echoedMsg, echoedNUM, totalRequests, output_file, totalMessages, totalRTT))
        #  now we want to load up the array "threadQueue"
        threadQueue.append(thread)
        print ("Starting Client #" + str(clientID))
        thread.start()
        clientID += 1

    #  We iterate through all the threads and join() waits for each thread to finish execution
    for thread in threadQueue:
        thread.join()


def start_engine(clientID, machineAddr, clients, portForwarderAddr, portForwarderPort, echoedMsg, echoedNUM, totalRequests, output_file, totalMessages, totalRTT):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((portForwarderAddr, portForwarderPort))
    done = ""

    # this iterates through the user-specified number of echoes that will be sent out
    for i in range(echoedNUM + 1):
        # start the time once msg is sent to server
        startTime = time.time()
        echoData = str(echoedMsg)
        totalLenData = len(echoData)
        # this condition is meant for select/epoll server: once the list of messages have been iterated and sent
        # this specific client has to send a quit so that the server can move on to another client session
        if i == echoedNUM:
            print ("We're done with the server now. Time to terminate this session eh!")
            print ("Client: " + str(clientID) + " --> has iterated through total number of messages to echo out. Server will be notified.")
            done = "done"
            s.send(done.encode('utf-8'))
        else:
            s.send(echoData.encode('utf-8'))
            print ("Message was sent: " + str(totalLenData) + " Bytes")
            # This value will continuously increment in value after every msg sent --> will output the total bytes sent to client
            totalMessages += echoData

        recvMsg = s.recv(2048)
        totalLenRecv = len(recvMsg)
        # once we receive the echo back from server, we end the timer
        endTime = time.time()
        # Now we gather the round trip time of the msg being sent from client to server and then from back from server to client.
        RTT = endTime - startTime
        totalRTT += RTT
        avgRTT = RTT / totalRTT
        clientSleep = random.randint(0,9)
        time.sleep(clientSleep)
        i += 1

    #  now we want to output the results of this echo stats to the log file
    output_file.write("\n Client #" + str(clientID) + " sent out a total of " + str(echoedNUM) + " messages with a total roundtrip time of " + str(RTT) + " seconds.")
    output_file.write("\n")
    result_to_file(clients, totalRTT, avgRTT, totalMessages, totalRequests, output_file)

def result_to_file(clients, totalRTT, avgRTT, totalMessages, totalRequests, output_file):
    totalLenMsgs = len(totalMessages)
    output_file.write("\n")
    output_file.write("\n -------------------RESULTS-------------------")
    output_file.write("\n Total Number of Clients: " + str(clients))
    output_file.write("\n Total Number of Requests: " + str(totalRequests))
    output_file.write("\n Total Data Sent to server: " + str(totalLenMsgs) + " Bytes")
    output_file.write("\n Total Roundtrip Time for each echo: " + str(totalRTT) + " seconds")
    output_file.write("\n Average Roundtrip Time for each echo: " + str(avgRTT) + " seconds")
    output_file.write("\n")


def main():

    #portForwarderAddr = raw_input("Enter the server ip address: ")

    portForwarderAddr = '192.168.0.11'
    portForwarderPort = 7007

    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((serverIP, port))
    output_file = open('Client-Output.txt','w')
    signal(SIGPIPE, SIG_DFL)

    #machineAddr = raw_input("What is your IP Address? (i.e. 192.168.0.X) ")
    machineAddr = '192.168.0.11'
    #clients = raw_input("How many clients would you like to spawn? (Enter an Integer value) ")
    clients = '800'
    #echoedMsg = raw_input("What do you want to echo to the server? (Enter a string) ")
	# the data we will be sending is 2000 Bytes in size
    echoedMsg = """Hey there server. It's me, your friendly neighbour Spiderman. Wait is that even right? Spiderman is the
        most insane character in the MCU and come on.... Peter Parker is awesome especially his relationship with Mary Jane! I am
        so getting out of context here. I am getting too hyped with MCU eversince we all went to go see Black Panther. T'Challa was
        such a crazy character and don't even get me started with Erik Killmonger. His character is soo complex. It's like peeling an
        oniong meaning it's just layers and layers of mystery. Everything about that movie is amazing! Empahsizes so much on unity and
        how you use that empowerment to overcome any other obstacles. The point I wanted to get out was just a simple hello! I must
        say that the MCU have really outdone themself with the expansion of the team. Like come on! Who isn't excited for the new
        Infinity War against the almighty Thanos, the destroyer and true ruler of the universe.  Once he has all the infinity stones
        that dude would be unstoppable no matter how big the team is. Disney is just a monster house buying every company there is.
        Good job to them and bad job with Star Wars: The Last Jedi LIKE COME ON!!!!!
        the destroyer and true ruler of the universe."""
    #echoedNUM = raw_input("How many times do you want this message echoed from each client to the server? (Enter an integer value) ")
    echoedNUM = '15'
    option = raw_input("Would you like to commence the echo program? (type 'begin') ")

    totalRequests = ((int(clients) * int(echoedNUM)) + int(clients))

    if option == "begin":
        # we want to makes sure we're not passing a null msg to the server
        if echoedMsg == "":
            print ("The message cannot be null! You must send something")
            echoedMsg = raw_input("What do you want to echo to the server? (Enter a string)")
        else:
            spawn_clients(machineAddr, int(clients), portForwarderAddr, portForwarderPort, echoedMsg, int(echoedNUM), totalRequests, output_file)


if __name__ == "__main__": main()
