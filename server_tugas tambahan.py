import socket
import os
import argparse

buff = 1024

def response(client_socket):
    while True:
        try:
            message = client_socket.recv(buff).decode()
            command = message.split()

            # ls 
            if command[0] == 'ls':
                ls(client_socket, command[1] if len(command) > 1 else '.')

            # rm
            elif command[0] == 'rm':
                if len(command) > 1:
                    result = rm(command[1])
                else:
                    result = '[SERVER] Usage: rm filename'
                client_socket.sendall(result.encode())

            # upload 
            elif command[0] == 'upload':
                if len(command) > 1:
                    filename = command[1]
                    dir_path = 'client_folder'

                    if not os.path.exists(dir_path):
                        result = '[SERVER] Directory does not exist'
                    else:
                        result = upload(client_socket, filename, dir_path)

                    client_socket.sendall(result.encode())
                else:
                    client_socket.sendall(b'[SERVER] Usage: upload filename')

            # download
            elif command[0] == 'download':
                if len(command) > 1:
                    filename = command[1]
                    download(client_socket, filename)
                else:
                    client_socket.sendall(b'[SERVER] Usage: download filename')

            # size
            elif command[0] == 'size':
                if len(command) > 1:
                    filename = command[1]
                    result = get_size(filename)
                    client_socket.sendall(result.encode())
                else:
                    client_socket.sendall(b'[SERVER] Usage: size filename')

            # connme
            elif command[0] == 'connme':
                client_socket.sendall(b'[SERVER] You are connected!')

            # byebye 
            elif command[0] == 'byebye':
                client_socket.close()
                break

            # exception
            else:
                client_socket.sendall(b'[SERVER] Invalid command')

        except Exception as e:
            print("Error:", e)
            client_socket.sendall(b'[SERVER] An error occurred')
            break

def ls(client_socket, directory='.'):
    try:
        files = os.listdir(directory)
        files_str = '\n'.join(files)
        client_socket.sendall(files_str.encode())
    except Exception as e:
        client_socket.sendall(str(e).encode())

def rm(filename):
    try:
        if os.path.exists(filename):
            os.remove(filename)
            return '[SERVER] File {} deleted successfully'.format(filename)
        else:
            return '[SERVER] File {} not found'.format(filename)
    except Exception as e:
        return str(e)

def upload(client_socket, filename, upload_dir='.'):
    try:
        upload_dir = os.path.abspath(upload_dir)

        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        file_dst = os.path.join(upload_dir, filename)

        if os.path.exists(file_dst):
            user_input = input('File {} already exists. Do you want to overwrite it? (y/n): '.format(filename))
            if user_input.lower() != 'y':
                return '[SERVER] Upload canceled'

        with open(file_dst, 'wb') as file:
            file_data = client_socket.recv(buff)
            while file_data:
                file.write(file_data)
                file_data = client_socket.recv(buff)

        return "[SERVER] File {} uploaded successfully to {}".format(filename, file_dst)
    except Exception as e:
        return str(e)

def get_size(filename):
    try:
        if os.path.exists(filename):
            size_bytes = os.path.getsize(filename)
            size_kb = size_bytes / 1024
            return '{} = {} KB'.format(filename, size_kb)
        else:
            return '[SERVER] 404 File {} not found'.format(filename)
    except Exception as e:
        return str(e)

def download(client_socket, filename, download_dir='.'):
    try:
        download_dir = os.path.abspath(download_dir)
        file_path = os.path.join(download_dir, filename)

        if os.path.exists(file_path):
            # Sending file size
            file_size = os.path.getsize(file_path)
            client_socket.sendall(str(file_size).encode())

            # Sending file data
            with open(file_path, 'rb') as file:
                while True:
                    data = file.read(buff)
                    if not data:
                        break
                    client_socket.sendall(data)

            return '[SERVER] File {} downloaded successfully from {}'.format(filename, file_path)
        else:
            client_socket.sendall(b'[SERVER] 404 File not found')
    except Exception as e:
        client_socket.sendall(str(e).encode())


def main():
    host = 'localhost'
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print('[SERVER] Server is listening on port', port)

    while True:
        try:
            client_socket, address = server_socket.accept()
            print('[SERVER] Client connected from', address)
            response(client_socket)
        except Exception as e:
            print("Error:", e)
            break

    server_socket.close()

if __name__ == "__main__":
    main()
