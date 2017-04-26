import socket               # Import socket module
from threading import Thread

#Linked List:
class Node:
    def __init__(self,initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self,newdata):
        self.data = newdata

    def setNext(self,newnext):
        self.next = newnext

class LinkedList:

    def __init__(self):
        self.head = None

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current
            current = current.next

    def add(self,item):
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp

    def size(self):
        current = self.head
        count = 0
        while current != None:
              count = count + 1
              current = current.getNext()

        return count

    def search(self,item):
         current = self.head
         found = False
         while current != None and not found:
                if current.getData() == item:
                   found = True
                else:
                   current = current.getNext()

         return found

    def remove(self,item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()

        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())

#create a new linked list for active peers
active_peers = LinkedList()

#create a new linked list for index of RFC's
rfc_index = LinkedList()

#Active peers item:
class PeerItem:
    def __init__(self,peer_host,peer_port):
        self.peer_host = peer_host
        self.peer_port = peer_port

#RFC index item:
class RFCItem:
    def __init__(self,rfc_number,rfc_title,rfc_host):
        self.rfc_number = rfc_number
        self.rfc_title = rfc_title
        self.rfc_host = rfc_host

#handle new peers joining
def client_join(data_list,client_socket):
    host = data_list[1].split(':')[1]
    port = data_list[2].split(':')[1]
    active_peers.add(PeerItem(host,port))
    client_socket.send('You have sucessfully joined the P2P network'.encode())


def client_add(data_list,client_socket,data):
    host = data_list[1].split(':')[1]
    title = data_list[3].split(':')[1]
    rfc = title.split('c')[1]
    port = data_list[2].split(':')[1]
    rfc_index.add(RFCItem(rfc,title,host))
    response = "P2P-CI/1.0 200 OK\n" + "RFC " + str(rfc) + title + host + str(port)
    client_socket.send(response.encode())

#handle every new connection from a client
def new_connection(client_socket):
    data = client_socket.recv(1024).decode()
    print('new request from client')
    data_list  = data.split('\n')
    for line in data_list:
        print(line)
    if data_list[0].split(' ')[0] == 'JOIN':
        client_join(data_list,client_socket)
    if data_list[0].split(' ')[0] == 'ADD':
        client_add(data_list,client_socket,data)


#main functionlity of the central server
server_socket = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 7734                # Reserve a port for your service.
server_socket.bind((host, port))        # Bind to the port
print('central server host is ',host)
print('central server port is ',port)


server_socket.listen(5)                 # Now wait for client connection.
print("Central server is awaiting a connection")
while(True):
        client_socket, client_addr = server_socket.accept()     # Establish connection with client.
        print('Got connection from', client_addr)
        new_thread = Thread(target=new_connection,args=(client_socket,))
        new_thread.start()
print('shutting down central server')
server_socket.close()                # Close the connection
