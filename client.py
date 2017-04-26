import socket               # Import socket module
from threading import Thread
import os
import glob

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







host = socket.gethostname() # Get local machine name
port = int(input("please enter an unused port number: "))
upload_thread = Thread(target=upload_server)
upload_thread.start()
handle_input()
