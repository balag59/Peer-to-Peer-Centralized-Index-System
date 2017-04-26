import socket               # Import socket module
from threading import Thread
import os
import glob
import sys


#to listen to any peers requiring uploads
def upload_server():
    pass

#to send requests to the central server_host
def send_requests(note, server_host, server_port):
    client_socket = socket.socket()
    client_socket.connect((server_host, server_port))
    client_socket.send(note.encode())
    response = client_socket.recv(1024).decode()
    print('response from the central server :')
    print(response)
    client_socket.close()

#send a request to list all rfc's
def list_rfc(server_host, server_port):
    note = "LIST ALL P2P-CI/1.0\nHost: "+host+'\n'+"Port: "+str(port)
    send_requests(note, server_host, server_port)

#accept input and send requests to add rfc's
def add_rfc(server_host,server_port):
    print('please enter a RFC number')
    rfc = int(input())
    print('please enter the RFC title')
    title = input()
    note = "ADD RFC " +str(rfc)+" P2P-CI/1.0\nHost: "+host+'\n'+"Port: "+str(port)+'\n'+"Title: "+title
    send_requests(note, server_host, server_port)

#accept input and send requests to find a rfc
def lookup_rfc(server_host,server_port):
    print('please enter a RFC number')
    rfc = int(input())
    print('please enter the RFC title')
    title = input()
    note = "LOOKUP RFC " +str(rfc)+" P2P-CI/1.0\nHost: "+host+'\n'+"Port: "+str(port)+'\n'+"Title: "+title
    send_requests(note, server_host, server_port)

#to handle any user input
def handle_input():
    server_host = input("enter the host of the central server: ")
    server_port = 7734
    #for the first time a peer joins the system
    note = "JOIN P2P-CI/1.0\nHost: "+host+'\n'+"Port: "+str(port)
    send_requests(note, server_host, server_port)
    file_list = glob.glob('*.txt')
    for file in file_list:
        title = file.split('.')[0]
        rfc = int(title.split('c')[1])
        note = "ADD RFC " +str(rfc)+" P2P-CI/1.0\nHost: "+host+'\n'+"Port: "+str(port)+'\n'+"Title: "+title
        send_requests(note, server_host, server_port)
    #after the client joins sucessfully give functionality options
    while(True):
        print("What do you want to do?Enter number corresponding to an option you choose")
        print("1. Add RFC's")
        print("2. Lookup RFC's")
        print("3. List all available RFC's")
        print("4. Download a RFC file")
        print("5. Quit")
        option = int(input())
        print('option is ',option)
        if(option == 1):
            add_rfc(server_host, server_port)
        elif(option == 2):
            lookup_rfc(server_host, server_port)
        elif(option == 3):
            list_rfc(server_host, server_port)
        elif(option == 4):
            download_rfc(server_host, server_port)
        elif(option == 5):
            quit(server_host, server_port)
        else:
            print('please enter a valid choice')

#main client functionality

host = input("please enter an unused host name: ")
port = int(input("please enter an unused port number: "))
upload_thread = Thread(target=upload_server)
upload_thread.daemon = True
upload_thread.start()
handle_input()
