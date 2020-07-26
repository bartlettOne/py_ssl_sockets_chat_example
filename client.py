import socket
import select
import errno
import sys
import ssl
from threading import Thread

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
hostname = 'example.com'
server_cert = 'server.crt'
client_cert = 'client.crt'
client_key = 'client.key'

def receive_thread_func(sclient_socket):
    while True:
        try:
            # Receive our "header" containing username length, it's size is defined and constant
            username_header = sclient_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = sclient_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = sclient_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = sclient_socket.recv(message_length).decode('utf-8')

            # Print message
            print(f'{username} > {message}')

        except Exception as e:
            # Any other exception - something happened, exit
            print('Reading error: {}'.format(str(e)))
            sys.exit()

if __name__ == "__main__":
    my_username = input("Username: ")

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
    context.load_cert_chain(certfile=client_cert, keyfile=client_key)

    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sclient_socket = context.wrap_socket(client_socket, server_side=False, server_hostname=hostname)
    print(sclient_socket.version())

    # Connect to a given ip and port
    sclient_socket.connect((IP, PORT))

    # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
    sclient_socket.setblocking(True)

    # Start the thread to receive data
    receive_thread = Thread(target=receive_thread_func, args=(sclient_socket,), daemon=True).start()

    # Prepare username and header and send them
    # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    sclient_socket.send(username_header + username)

    while True:

        # Wait for user to input a message
        message = input(f'{my_username} > ')

        # If message is not empty - send it
        if message:

            # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            sclient_socket.send(message_header + message)

