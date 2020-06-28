import os
import sys
import csv
import math
import socket

ip = ''
port = 0
filename = 'login_credentials2.csv' # filename of csv file-name
data = {}
BUFFER_SIZE = 100000
SEPARATOR = "<SEPARATOR>"


# Read ip and port 
def get_ip():
    global ip, port
    file_reader = open("StarkHUB.rtl", "r")
    lines = file_reader.readlines()
    flag = 0
    count = 0
    print('-'*40)
    for line in lines:
        host = line[0:line.find('|')]
        ip = line[line.find('|') + 1: line.find('|', line.find('|') + 1)]
        port = int(line[line.find('|', line.find('|') + 1) + 1:])
        count = count + 1
        if count == 2:
            break
    file_reader.close()


# Read CSV file
def file_read():
    with open(filename,'r') as login_file:
        reader = csv.reader(login_file)
        for row in reader:
            if row[0] != 'Username':
                data[row[0]] = row[1]


# Function to validate authentication
def validate_login(username, password):
    if (data.get(username)) is None:
        return '0'
    elif (data[username] == password):
        return '2'
    else:
        return '0'


# Main Function
def main():
    global ip, port
    get_ip()
    file_read()
    # Create socket and bind
    host_b_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_b_socket.bind ((ip, port))
    except:
        print("Bind Failed! Error : " + str(sys.exc_info()) + ".")
        sys.exit()


    host_b_socket.listen(5)
    print('Socket is now listening!')
    print('-'*100)
    while True:
        try:
            # Connect to a client
            client_socket, address = host_b_socket.accept()
            client_ip, client_port = str(address[0]), str(address[1])
            print("Connected with " + client_ip + " : " + client_port + ".")
        except:
            print("Connection failed.")
            continue

        method = client_socket.recv(1024).decode()
        if method == 'login':
            print('-'*100)
            # Get username and password
            client_socket.send(('ACK : Login method by Host-B ' + ip + ':' + str(port) + ' initiated.').encode())
            print('Received from server ' + client_ip + ' : ' + str(client_port) + ' login-request.')
            username = client_socket.recv(1024).decode()
            client_socket.send(('ACK : Received by Host-B ' + ip + ' : ' + str(port) + ' username.').encode())
            print('Received from server ' + client_ip + ' : ' + str(client_port) + ' username.')
            password = client_socket.recv(1024).decode()
            client_socket.send(('ACK : Received by Host-B ' + ip + ' : ' + str(port) + ' password.').encode())
            print('Received from server ' + client_ip + ' : ' + str(client_port) + ' password.')
            error = client_socket.recv(1024).decode()
            client_socket.send((validate_login(username, password)).encode())
        else :
            print('-'*100)
            # Upload method
            client_socket.send(('ACK : Upload method by Host-B ' + ip + ' : ' + str(port) + ' initiated.').encode())
            print('Received from server ' + client_ip + ' : ' + str(client_port) + ' upload-request.')
            received = client_socket.recv(BUFFER_SIZE).decode()
            client_socket.send(('ACK : Received by Host-B ' + ip + ' : ' + str(port) + ' file-data.').encode())
            print('Received from server ' + client_ip + ' : ' + str(client_port) + ' file-data.')
            filename, filesize = received.split(SEPARATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)
            count  = 0
            total_packet = str(math.ceil(filesize/BUFFER_SIZE))

            with open(filename, "wb") as f:
                while(count != int(total_packet)):
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    count = count + 1
                    client_socket.send(('ACK : Recieved by Host-B ' + ip + ' : ' + str(port) + '. Packet : ' + str(count) + '/' + total_packet + '.').encode())
                    # print('Recieved from server ' + client_ip + ' : ' + str(client_port) + '. Packet : ' + str(count) + '/' + total_packet + '.')
                    f.write(bytes_read)
            
        client_socket.close()
        print("Connection " + client_ip + " : " + client_port + " Closed.")
        print('-'*100)

    host_b_socket.close()
    print('Socket Closed!')
    print('-'*100)

# Run the main function
main()
