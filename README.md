# Socket-Programming-II

### Demo Link:
[![IMAGE ALT TEXT HERE]https://raw.githubusercontent.com/cynicphoenix/Socket-Programming-II/master/Screenshot%20(97).png?token=AK7XLBX67RZGOTR4ZGIWGTC7BWXPA)](https://www.youtube.com/watch?v=sKeVvWHrjAU)
<br/>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This assignment includes some element from Socket Programming Assignment-I. In the Socket Programming assignment, I created a peer-to-peer network of multiple nodes which were able to
communicate with one-another by exchanging messages (there were a total of 6 Nodes A, B, C
and D, a client node and a server node).<br/>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Let us extend the capabilities of that peer-to-peer network to transfer a file of moderate
size from one node to another.  need to perform an application level framing of the file in order
to transfer it from one node to another. Fix the size of the frames to be 100 KB or I can take
frame size as input from the user (in KBs). Let us say when the authentication is successful, the client needs to upload a file (like
assignment submisison) to the server. The server however directs all the frames from a user
(authenticated client) to the node which maintains the username and password for that particular
user. Moreover, for the purpose of more system reliability, we use two servers nodes in the
network. Both the servers are all the same except for their own IP addresses and port numbers. In
addition, these servers also cause random delays (the minimum delay is the RTT between client
and server nodes) in the forwarding of frames to the destination nodes.
The client knows about both the servers and for each message/frame, it chooses one of
the servers alternatively.<br/>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For the file transfer, here is a sample text file: Sakoontala or The Lost Ring: http://
www.gutenberg.org/cache/epub/12169/pg12169.txt
However, I am free choose any other of my favourite books’ text file from the Gutenberg
project as samples for this assignment. I must test my implementation with 2-3 sample files
of different sizes.
Further, to ensure an error free delivery of the frames, I should implement a checksum
based error detection method for the frames. The checksum should be transmitted with each
frame. In case, the received frames get corrupted during the transmission, such frames must be
retransmitted. Basically, I have to implement Stop-and-Wait ARQ protocol.
<br/>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;As I would not note any error in the transmission in the LAN of my Lab, create a
mechanism that corrupts the frames with some probability p. Take the value of p as an input from
the user. Yo can set p = 0.1 as default value.
At the ultimate destination of each file, the data in the frames must be combined in a
particular order so that the original text file can be recovered. Only when the complete file is
recovered, the destination node should send a message of successful data transfer to the client
node.

<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Note: I must display all the intermediate message exchanges on the consoles of all the nodes
of I peer-to-peer network.
Topic (in that order) Marks
Correct transfer of file with framing 20
Server replica with random delays 10
Checksum and Stop-and-Wait ARQ 20
