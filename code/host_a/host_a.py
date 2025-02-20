import sys
import csv
import socket

ip = ''
port = 0
filename = 'login_credentials1.csv' # filename of csv file-name
data = {}


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
        if count == 1:
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
        return '1'
    else:
        return '0'


# Main Function
def main():
    global ip, port
    get_ip()
    file_read()
    # Create socket and bind
    host_a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_a_socket.bind ((ip, port))
    except:
        print("Bind Failed! Error : " + str(sys.exc_info()))
        sys.exit()


    host_a_socket.listen(5)
    print('Socket is now listening!')
    print('-'*40)
    while True:
        try:
            # Connect to a client
            client_socket, address = host_a_socket.accept()
            ip, port = str(address[0]), str(address[1])
            print("Connected with " + ip + " : " + port)
        except:
            print("Connection failed!")
            continue

        # Get username and password
        username = client_socket.recv(1024).decode()
        client_socket.send(('ACK : Username received by Host-A!').encode())
        print('Username received!')
        password = client_socket.recv(1024).decode()
        client_socket.send(('ACK : Password received by Host-A!').encode())
        print('Password received!')
        error = client_socket.recv(1024).decode()
        send_bit = validate_login(username, password)
        client_socket.send(send_bit.encode())

        client_socket.close()
        print("Connection " + ip + ":" + port + " Closed!")
        print('-'*40)

    host_a_socket.close()
    print('Socket Closed!')
    print('-'*40)
# Run the main function
main()
