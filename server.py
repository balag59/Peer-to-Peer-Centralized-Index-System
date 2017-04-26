import socket               # Import socket module
from threading import Thread

def new_connection(client_socket):
    print('new connection')
    while(True):
         data = client_socket.recv(1024)
         client_socket.send(data)
    client_socket.close()



server_socket = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 7734                # Reserve a port for your service.
server_socket.bind((host, port))        # Bind to the port

server_socket.listen(5)                 # Now wait for client connection.
print("Server is awaiting a connection")
while True:
   client_socket, client_addr = server_socket.accept()     # Establish connection with client.
   print('Got connection from', client_addr)
   new_thread = Thread(target=new_connection,args=(client_socket,))
   new_thread.start()
server_socket.close()                # Close the connection
