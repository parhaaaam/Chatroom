import socket
import select
import errno
import sys 

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))


client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

def compile_message(msg):
    msg = msg.encode('utf-8')
    message_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
    return message_header + msg


def decode(txt):
    return txt.decode('utf-8')

def read_int(txt):
    return int(decode(txt).strip())


def run_client():
    while True:
        message = input(f'{my_username} > ')
        if message:
            client_socket.send(compile_message(message))
        try:
            while True:
                username_header = client_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    print('Connection closed by the server')
                    sys.exit()
                username_length = read_int(username_header)
                username = decode(client_socket.recv(username_length))
              
                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = read_int(message_header)
                message = decode(client_socket.recv(message_length))
                print(f'{username} > {message}')

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            continue
        except Exception as e:
            print('Reading error: '.format(str(e)))
            sys.exit()


if __name__ == '__main__':
  run_client()