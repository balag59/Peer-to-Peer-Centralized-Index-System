import socket               # Import socket module
from threading import Thread

#to listen to any peers requiring uploads
def upload_server():
    pass

#to send requests to the central server_host
def send_requests(note, server_host, server_port):
    client_socket = socket.socket()
    client_socket.connect((server_host, server_port))
    client_socket.send(note)
    response = client_socket.recv(1024)
    print('response :')
    print(response)
    client_socket.close()



#to handle any user input
def handle_input():
    server_host = input("enter the host of the central server: ")
    server_port = 7734
    #for the first time peer joins the system
    message = "JOIN P2P-CI/1.0 Host: "+host+" Port: "+str(port)
    send_requests(note, server_host, server_port)




host = socket.gethostname() # Get local machine name
port = int(input("please enter an unused port number: "))
upload_thread = Thread(target=upload_server)
upload_thread.start()
handle_input()
