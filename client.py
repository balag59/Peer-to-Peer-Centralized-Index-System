import socket               # Import socket module

client_socket = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 7734               # Reserve a port for your service.

client_socket.connect((host, port))
while True:
    data = input("message: ")
    client_socket.send(data.encode())
    response = client_socket.recv(1024)
    print(response)
client_socket.close()                     # Close the socket when done
