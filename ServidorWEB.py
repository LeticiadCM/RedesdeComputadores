#import socket module
from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
serverPort = 12000 # Assign a port number
serverSocket.bind(('', serverPort)) # Bind the socket to server address and server port
serverSocket.listen(1) # Listen to at most 1 connection at a time

while True:
    
    #Establish the connection
    print ('The server is ready.')
    connectionSocket, addr = serverSocket.accept()
    
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()
        #Send one HTTP header line into socket

        #Send the content of the requested file to the client
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n".encode())
        connectionSocket.send("\r\n".encode()) 

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
        
    except IOError:
        #Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n". encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        #Close client socket
        connectionSocket.close()
        
serverSocket.close()
