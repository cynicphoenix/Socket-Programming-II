# This is the server code
import os
import csv
import socket 
import math
import sys
import traceback
from threading import Thread


# filename of csv-file
host = ''
port = 0
filename = 'StarkHUB.rtl'
data = {}
BUFFER_SIZE = 100000
SEPARATOR = "<SEPARATOR>"

# upload function
def upload(client_socket, host_ip, host_port, client_ip, client_port):
    # Connection to client
    received = client_socket.recv(BUFFER_SIZE).decode()
    if received == 'Exit':
        return
    print("Upload Method Initiated from client " + client_ip + " : " + str(client_port) + ".")
    client_socket.send(('ACK : Recieved by server ' + host + ' : ' + port + ' file-data.' ).encode())
    print('Filename & Filesize Recieved from client ' + client_ip + ' : ' + str(client_port) + '.')
    filename, filesize = received.split(SEPARATOR)
    filesize = int(filesize)
    count  = 0
    total_packet = str(math.ceil(filesize/BUFFER_SIZE))

    # Connect to host
    host_port = str(int(host_port))
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_socket.connect((host_ip, int(host_port)))
        print('-'*100)
        print("Connected to host " + host_ip + " : " + host_port + ".")
    except:
        print('-'*100)
        print("Connection to host " + host_ip + " : " + host_port + " failed.")
        print('-'*100)
        return
    method = 'upload'
    host_socket.send(method.encode())
    print(host_socket.recv(BUFFER_SIZE))
    host_socket.send(f"{filename}{SEPARATOR}{filesize}".encode()) 
    print(host_socket.recv(BUFFER_SIZE))

    
    while(count != int(total_packet)):     
        bytes_read = client_socket.recv(BUFFER_SIZE)   
        if not bytes_read:
            break
        count = count + 1
        client_socket.send(('ACK : Recieved by server ' + host + ' : ' + str(port) + '. Packet : ' + str(count) + '/' + total_packet + '.').encode())
        ('Recieved from client ' + client_ip + ' : ' + str(client_port) + '. Packet : '+ str(count) + '/' + total_packet + '.')

        host_socket.sendall(bytes_read)
        (host_socket.recv(BUFFER_SIZE).decode())
    
    print('Transmission succesfull from host ' + host_ip + ' : ' + str(host_port) + '.')
    host_socket.close()
    print("Connection to host "+host_ip+" : "+host_port+" closed.")
    print('-'*100)

    print('Transmission succesfull from client ' + client_ip + ' : ' + str(client_port) + '.')
    return

# Function to get IP of wifi 
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def validate_host(host_ip, host_port, username, password):
    host_port = str(int(host_port))
    method  = 'login'
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_socket.connect((host_ip, int(host_port)))
        print('-'*100)
        print("Connected to host "+host_ip+" : "+host_port)
    except:
        print('-'*100)
        print("Connection to host "+host_ip+" : "+host_port+" failed.")
        print('-'*100)
        return '0'
    host_socket.send(method.encode())
    print(host_socket.recv(1024).decode())
    host_socket.send(username.encode())
    print(host_socket.recv(1024).decode())
    host_socket.send(password.encode())
    print(host_socket.recv(1024).decode())
    host_socket.send(('Error!').encode())
    valid = host_socket.recv(1024).decode()
    host_socket.close()
    print("Connection to host "+host_ip+" : "+host_port+" closed.")
    print('-'*100)
    return valid


# Function to validate authentication
def validate_login(username, password, transfer_ip, transfer_port):
    file_reader = open(filename, "r")
    lines = file_reader.readlines()
    flag = 0
    count = 0
    print('-'*40)
    for line in lines:
        host = line[0:line.find('|')]
        host_ip = line[line.find('|') + 1: line.find('|', line.find('|') + 1)]
        host_port = line[line.find('|', line.find('|') + 1) + 1:]
        host_port = str(int(host_port))
        if count == 4 :
            break
        return_flag = int(validate_host(host_ip, host_port, username, password))
        if return_flag == 1:
            flag = 1
            transfer_ip = host_ip
            transfer_port = host_port
        count = count + 1 
    file_reader.close()

    if flag == 1:
        # Check attendance
        host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            host_socket.connect((host_ip, int(host_port)))
            print('-'*100)
            print("Connected to host "+host_ip+" : "+host_port)
        except:
            print('-'*100)
            print("Connection to host "+host_ip+" : "+host_port+" failed.")
            print('-'*100)
            return '0'
        host_socket.send(username.encode())
        print(host_socket.recv(1024).decode())
        host_socket.send(('Error!').encode())
        valid = host_socket.recv(1024).decode()
        print("Connection to host "+host_ip+" : "+host_port+" closed.")
        print('-'*100)
        return valid 
    else:
        return '0'


# Function to start the server
def start_server():
    global host, port
    # Create socket and bind
    host = '172.21.5.133' #get_ip_address()
    port = 1024 #input('Enter Port : ')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind ((host, int(port)))
    except:
        print("Bind failed! error : " + str(sys.exc_info()) + " .")
        sys.exit()
    
    
    server_socket.listen(5)
    print("Hostname : " + host)
    print('Socket is now listening...')
    print('-'*100)

    while True:
        # Connect to a client
        client_socket, address = server_socket.accept()
        ip, port = str(address[0]), str(address[1])
        print('-'*100)
        print("Connected with " + ip + " : " + port)

        try:
            Thread(target = client, args=(client_socket, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()
    server_socket.close()


# Function to interact with client
def client(client_socket, client_ip, client_port):
    global host, port
    upload(client_socket, '127.0.0.1', '1312', client_ip, client_port)
    # Get username and password
    # username = client_socket.recv(1024).decode()
    # if username == 'EXIT':
    #     client_socket.send(('ACK : Received by server ' + host + ' : ' + str(port) + ' EXIT.').encode()) 
    #     print("Received from client "+ip+" : "+port+" EXIT.")
    # else:
    #     client_socket.send(('ACK : Received by server ' + host + ' : ' + str(port) + ' username.').encode()) 
    #     print("Received from client "+ip+" : "+port + " username.")
    #     password = client_socket.recv(1024).decode()
    #     if password == 'EXIT':
    #         client_socket.send(('ACK : Received by server ' + host + ' : ' + str(port) + ' EXIT.').encode()) 
    #         print("Received from client "+ip+" : "+port+" EXIT.")
    #     else :
    #         client_socket.send(('ACK : Received by server ' + host + ' : ' + str(port) + ' password.').encode()) 
    #         print("Received from client "+ip+" : "+port + " password.")
    #         error = client_socket.recv(1024).decode()
    #         # Validate authentication
            # transfer_ip = ''
            # transfer_port = 0
    #         if validate_login(username, password, transfer_ip,) != '0':
    #             client_socket.send(('1').encode())
    #             # Lab Assignment Part 2
    #             upload(client_socket, transfer_ip, transfer_port, client_ip, client_port)
    #         else:
    #             client_socket.send(('0').encode())
    # Close client socket
    client_socket.close()
    print("Connection to client " + client_ip + " : " + client_port + " closed.")
    print('-'*100)


# Main function
def main():
    start_server()

# Run the main function
main()