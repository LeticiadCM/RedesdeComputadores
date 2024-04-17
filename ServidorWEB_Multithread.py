import socket
import threading

def client(clientSocket):
    
    try:
        message = clientSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()

        clientSocket.send("HTTP/1.1 200 OK\r\n".encode())
        clientSocket.send("Content-Type: text/html\r\n".encode())
        clientSocket.send("\r\n".encode())

        for i in range(0, len(outputdata)):
            clientSocket.send(outputdata[i].encode())
        clientSocket.close()

    except IOError:
        clientSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        clientSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        clientSocket.close()

def server():
    
    serverPort = 12000
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)
    print('The server is ready.')

    while True:
        connectionSocket, addr = serverSocket.accept()

        client_handler = threading.Thread(target = client, args = (connectionSocket,))
        client_handler.start()

    serverSocket.close()

if __name__ == "__main__":
    server()
