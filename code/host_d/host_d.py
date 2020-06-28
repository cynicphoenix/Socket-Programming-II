import sys
import csv
import socket

ip = ''
port = 0
filename = 'attendance_percentage.csv' # filename of csv file-name
data = []
ex = 80


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
        if count == 4:
            break
    file_reader.close()


# Read CSV file
def file_read():
    with open(filename,'r') as login_file:
        reader = csv.reader(login_file)
        fields = reader.__next__() 
        for row in reader:
            data.append(row)


# Calculate attendance
def attendance(username) :
    att = 0
    for row in data:
        if(row[0] == username):
            att = float(row[1])
            break
    if att >= ex:
        return '1'
    return '0'


# Main Function
def main():
    global ip, port
    get_ip()
    file_read()
    # Create socket and bind
    host_d_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_d_socket.bind ((ip, port))
    except:
        print("Bind Failed! Error : " + str(sys.exc_info()))
        sys.exit()


    host_d_socket.listen(5)
    print('Socket is now listening!')
    print('-'*40)
    while True:
        try:
            # Connect to a client
            client_socket, address = host_d_socket.accept()
            ip, port = str(address[0]), str(address[1])
            print("Connected with " + ip + " : " + port)
        except:
            print("Connection failed!")
            continue

        # Get username and password
        username = client_socket.recv(1024).decode()
        client_socket.send(('ACK : Username received by Host-D!').encode())
        print('Username received!')
        error = client_socket.recv(1024).decode()
        client_socket.send((attendance(username).encode()))

        client_socket.close()
        print("Connection " + ip + ":" + port + " closed!")
        print('-'*40)

    host_d_socket.close()
    print('Socket Closed!')
    print('-'*40)


# Run main
main()

        

