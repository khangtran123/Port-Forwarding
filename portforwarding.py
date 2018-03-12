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
    text_file = open("config-file.txt","r")
    text_file.read()
    for line in text_file:
        # first need to remove all spaces in the line 
        line.strip()
        # we need to split lines in the txt file based on a comma delimiter that 
        # splits up the host and it's client (destination)
        # 0 = host address:port
        # 1 = destination address:port
        segment = line.split(",")
        host = segment[0].split(":")
        sourceAddress = host[0]
        sourcePortNum = host[1]
        client = segment[1].split(":")
        destAddress = client[0]
        destPortNum = client[1]
        return sourceAddress, sourcePortNum, destAddress, destPortNum
    
    sourceIP.append(sourceAddress)
    sourcePort.append(sourcePortNum)
    destIP.append(destAddress)
    destPort.append(destPortNum)
    
    print ("Source IP Address: " + str(sourceIP))
    print ("Source Port Number: " + str(sourcePortNum))
    print ("Destination IP Address" + str(destAddress))
    print ("Destination Port Number: " + str(destPort))    
    

if __name__ == "__main__":
    sourceIP = []
    sourcePort = []
    destIP = []
    destPort = []
    readFromFile()