import socket
from select import select

def server():
    server_socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        yield
        client_socket, addr = server_socket.accept() # read
        print('Connection from', addr)
        client(client_socket)


def client(client_socket):
    while True:
        request = client_socket.recv(4096) # read
        if not request:
            break
        else:
            response = 'Hello world\n'.encode()
            client_socket.send(response) # write

    print("outside inner while loop")
    client_socket.close()


server()
