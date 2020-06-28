# This is the client code
import socket 
import tqdm
import math
import sys
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 100000

def get_checksum(bytes_read):
    checksum = 0
    for c in bytes_read:
        checksum = checksum + int(c)
    checksum = -(checksum % 256)
    return checksum


def upload(client_socket, ip, port):
    print('-'*30+"Assignment Submission"+'-'*30+'\n')
    filename = input('Enter file-name : ')
    try:
        filesize = os.path.getsize(filename)
        total_packet = str(math.ceil(filesize/BUFFER_SIZE))
    except:
        print('No such file exist.')
        client_socket.send(('Exit').encode())
        return
    client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
    print(client_socket.recv(BUFFER_SIZE).decode())

    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while(True):
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            client_socket.sendall(bytes_read)
            print(client_socket.recv(BUFFER_SIZE).decode())
            progress.update(len(bytes_read))
    print("Transmission succesful by client.")
    return


def main():
    ip = '172.21.5.133' #input('Enter ip of server : ')
    port = 1024 #input('Enter Port : ')
    print('-'*100)
    welcome_msg = 'WELCOME!'

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, int(port)))
        print('Connection Successful to server ' + ip + ' : ' + str(port) + '.\n')
        print(welcome_msg)
    except:
        print("Connection Error.")
        print('-'*100)
        sys.exit()
        
    # print("Enter 'EXIT' to terminate!")
    # username = input('Enter Username : ')
    # if username == 'EXIT':
    #     client_socket.send(("EXIT").encode())
    #     print(client_socket.recv(1024).decode())
    # else:
    #     client_socket.send(username.encode())
    #     print(client_socket.recv(1024).decode())
    #     password = input('Enter Password : ')
    #     if password == 'EXIT' :
    #         client_socket.send(("EXIT").encode())
    #         print(client_socket.recv(1024).decode())
    #     else:
    #         client_socket.send(password.encode())
    #         print(client_socket.recv(1024).decode())
    #         client_socket.send(('Error').encode())
    #         validate_bit = client_socket.recv(1024).decode()
    #         if validate_bit == '0':
    #             print('Access Denied.')
    #         else:
    #             print('Authentication Successful.')
                # Lab Assignment Part 2
    upload(client_socket, ip, port)

    client_socket.close()
    print('Socket closed.')
    print('-'*100)

# Run main
main()