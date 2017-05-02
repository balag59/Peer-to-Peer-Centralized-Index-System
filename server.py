import socket               # Import socket module
from threading import Thread

#Node for Linked Lists:
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

#LinkedLists and it's methods
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

host2port_dic = {}
host2rfc_dic = {}
rfc2host_dic = {}
title2rfc_dic = {}
#handle new peers joining
def client_join(data_list,client_socket):
    host = data_list[1].split(':')[1]
    port = data_list[2].split(':')[1]
    host2port_dic[host] = port
    active_peers.add(PeerItem(host,port))
    client_socket.send('You have sucessfully joined the P2P network'.encode())

#handle rfc's add request
def client_add(data_list,client_socket):
    host = data_list[1].split(':')[1]
    title = data_list[3].split(':')[1]
    rfc = data_list[0].split(' ')[2]
    port = data_list[2].split(':')[1]
    if host in host2rfc_dic:
        host2rfc_dic[host].append(rfc)
    else:
        host2rfc_dic[host] = [rfc]
    if rfc in rfc2host_dic:
        rfc2host_dic[rfc].append(host)
    else:
        rfc2host_dic[rfc] = [host]
    if title not in title2rfc_dic:
        title2rfc_dic[title] = rfc
    rfc_index.add(RFCItem(rfc,title,host))
    response = "P2P-CI/1.0 200 OK\n" + "RFC " + str(rfc) + title + host + str(port)
    client_socket.send(response.encode())

#handle list rfc request
def client_list(client_socket):
    response = "P2P-CI/1.0 200 OK\n"
    for item in rfc_index:
        rfc = item.getData().rfc_number
        title = item.getData().rfc_title
        host = item.getData().rfc_host
        port = host2port_dic[host]
        response += "RFC " + str(rfc) + title + host + str(port)+'\n'
    client_socket.send(response.encode())

#handle lookup rfc quest
def client_lookup(data_list,client_socket):
    title = data_list[3].split(':')[1]
    rfc = data_list[0].split(' ')[2]
    if rfc in rfc2host_dic:
        if title in title2rfc_dic:
          if title2rfc_dic[title] == rfc:
            response = "P2P-CI/1.0 200 OK\n"
            host_list = rfc2host_dic[rfc]
            for host in host_list:
                response += "RFC " + str(rfc) + title + host + str(host2port_dic[host])+'\n'
        else:
            response = "P2P-CI/1.0 400 Bad request\n"

    else:
            response = "P2P-CI/1.0 404 Not Found\n"

    client_socket.send(response.encode())

#client exit
def client_exit(data_list,client_socket):
    host = data_list[1].split(':')[1]
    port = data_list[2].split(':')[1]
    print('host {0} at port {1} is quitting'.format(host,port))
    #for item in rfc_index:
    #    if host = item.getData().rfc_host:
    #        rfc_index.remove(item)        
    client_socket.send('Bye'.encode())

#handle every new connection from a client
def new_connection(client_socket):
    data = client_socket.recv(1024).decode()
    print('new request from client')
    data_list  = data.split('\n')
    for line in data_list:
        print(line)
    if data_list[0].split(' ')[0] == 'JOIN':
        client_join(data_list,client_socket)
    elif data_list[0].split(' ')[0] == 'ADD':
        client_add(data_list,client_socket)
    elif data_list[0].split(' ')[0] == 'LIST':
        client_list(client_socket)
    elif data_list[0].split(' ')[0] == 'LOOKUP':
        client_lookup(data_list,client_socket)
    elif data_list[0].split(' ')[0] == 'EXIT':
        client_exit(data_list,client_socket)
    else:
        client_badrequest(data_list,client_socket,data)


#main functionlity of the central server
server_socket = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
server_host = socket.gethostbyname(socket.gethostname())
port = 7734                # Reserve a port for your service.
server_socket.bind((server_host, port))        # Bind to the port
print('central server host is ',server_host)
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
