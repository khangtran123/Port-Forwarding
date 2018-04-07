# Port-Forwarding
This script creates and deploys a network application that uses advanced TCP/IP Programming that implements "Port Forwarding"

*** Remember to set ulimit on each machine: ulimit -n 10000 ***

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
   a separate configuration file
