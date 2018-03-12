#!/bin/python3


import socket
import threading
import time
import sys
import os



if __name__ == "__main__":
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
