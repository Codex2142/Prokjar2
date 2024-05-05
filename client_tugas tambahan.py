import socket
import threading

address = 'localhost'
port = 5555
buff = 1024

def recv():
    while True:
        try:
            message = client_socket.recv(buff)
            if not message:
                print("[SERVER] bye bye")
                break
            print('\n[SERVER] : \n'+message.decode() + '\n')
        except ConnectionResetError:
            print("[CONNECTION] koneksi di reset")
            break

def send():
    while True:
        try:
            message = input('\n[YOU] : ')
            client_socket.send(message.encode())
        except ConnectionAbortedError:
            print("[CONNECTION ERROR] Connection to the server was aborted.")
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (address, port)

connme = input('ketik [connme] untuk koneksi: ')
if connme == 'connme':
    client_socket.connect(server_address)

    recv_thread = threading.Thread(target=recv, args=())
    send_thread = threading.Thread(target=send, args=())

    recv_thread.start()
    send_thread.start()

    # Menunggu kedua thread selesai sebelum melanjutkan
    recv_thread.join()
    send_thread.join()

    # Setelah kedua thread selesai, tutup socket
    client_socket.close()
else:
    print("Koneksi tidak dibuat.")
