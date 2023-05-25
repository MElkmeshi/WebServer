import threading
from socket import *

def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        connectionSocket.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
    except IOError:
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        connectionSocket.close()

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 80
serverSocket.bind(("127.0.0.1", serverPort))
serverSocket.listen(5)

while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
    client_thread.start()

serverSocket.close()
