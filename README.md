# Tugas 2 - FTP Socket Programming On python
Tugas ini disusun oleh
Nama    : Akbar Muhammad Sadat
NIM     : 1203220154
Kelas   : IF-02-01

## Panduan Mengunduh File praktikum
#### Download File
> https://github.com/Codex2142/Prokjar2/blob/main/Assets.rar
silahkan download file diatas untuk keperluan praktikum

#### instalasi file
setelah selesai download file praktikum. klik kanan pada file tersebut lalu klik "extract to assets"
![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/Screenshot%20(12).png?raw=true)

setelah didownload, terdapat 4 file yang perlu diperhatikan
- server .py (kode program untuk server)
- client .py (kode program untuk client)
- client (direktori khusus client)
- server (direktori khusus server)


## Penjelasan kode program server

```python
import socket
import os

alamat = ('localhost', 12345)
recv = 1024

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = alamat
    server_socket.bind(server_address)
    server_socket.listen(1)
    print('Waiting for a connection...')
    client_socket, client_address = server_socket.accept()
    print(f'Connected by {client_address}')
    loopMessage(client_socket)

def loopMessage(client_socket):
    menu = '| ls        | \n| rm        | \n| download  | \n| upload    | \n| size      | \n| byebye    |'
    client_socket.sendall(menu.encode())
    while True:
        message = client_socket.recv(recv).decode()
        if message == 'byebye':
            break
        else:
            process_message(client_socket, message)

def process_message(client_socket, message):
    print(f"Received: {message}")
    response = "Apakah ada yang bisa dibantu? "
    client_socket.sendall(response.encode())
    perintah = message.split()
    if len(perintah) == 2 :
        menu, file = perintah
        print(menu)
        print(file)
        if menu == 'download':
            download(client_socket, file)
        elif menu == 'upload':
            upload(client_socket, file)
        elif menu == 'size':
            size(client_socket, file)
        elif message == 'rm':
            rm(client_socket, file)
    else:
        if message == 'ls':
            ls(client_socket)
        elif message == 'byebye':
            client_socket.close()

def ls(client_socket):
    path = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//server"
    dirList = os.listdir(path)
    print(dirList)
    client_socket.sendall(str(dirList).encode())

def download(client_socket, file):
    server_dir = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//server"
    client_dir = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//client"
    
    server_file_path = os.path.join(server_dir, file)
    
    client_file_path = os.path.join(client_dir, file)
    
    if os.path.exists(server_file_path):
        with open(server_file_path, 'rb') as server_file:
            file_content = server_file.read()
            
            with open(client_file_path, 'wb') as client_file:
                client_file.write(file_content)
        pesan = 'file berhasil didownload'
        client_socket.sendall(pesan.encode())

def upload(client_socket ,file):
    server_dir = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//server"
    client_dir = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//client"

    server_file_path = os.path.join(server_dir, file)
    client_file_path = os.path.join(client_dir, file)

    if os.path.exists(client_file_path):
        with open(client_file_path, 'rb') as client_file:
            file_content = client_file.read()

            with open(server_file_path, 'wb') as server_file:
                server_file.write(file_content)
            pesan = 'file berhasil diupload'
            client_socket.sendall(pesan.encode())

def size(client_socket, file):
    server_path = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//server"
    serverFile = os.path.join(server_path, file)
    
    if os.path.exists(serverFile):
        file_size_bytes = os.path.getsize(serverFile)
        file_size_kb = file_size_bytes / 1024
        size_message = f"Ukuran file {file}: {file_size_kb:.2f} kB"
        client_socket.sendall(size_message.encode())
    else:
        not_found_message = 'File tidak ditemukan'
        client_socket.sendall(not_found_message.encode())

def rm(client_socket, file):
    server_path = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//server"
    serverFile = os.path.join(server_path, file)
    
    if os.path.exists(serverFile):
        os.remove(serverFile)
        pesan = 'file berhasil dihapus'
        client_socket.sendall(pesan.encode())
    else:
        pesan = 'file tidak ditemukan'
        client_socket.sendall(pesan.encode())

if __name__ == '__main__':
    main()

```

sebelum membuat algoritma yang digunakan server. sebaiknya mendeklarasikan variabel secara global. hal ini diperlukan agar tidak menuliskan kode dengan panjang lebar nantinya
```python
import socket
import os

alamat = ('localhost', 12345)
recv = 1024
```
terdapat 8 fungsi utama yang akan dijalankan dalam program python. berikut ini adalah penjelasan tiap fungsinya
1. Fungsi main()
    ```python
    def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = alamat
    server_socket.bind(server_address)
    server_socket.listen(1)
    print('Waiting for a connection...')
    client_socket, client_address = server_socket.accept()
    print(f'Connected by {client_address}')
    loopMessage(client_socket)
    ```
    kode program diatas digunakan untuk membangun koneksi ke klien menggunakan protokol **TCP**. setelah terkoneksi, maka akan diarahkan ke fungsi **loopMessage()**
    
2. Fungsi loopMessage()
    ```python
    def loopMessage(client_socket):
    menu = '| ls        | \n| rm        | \n| download  | \n| upload    | \n| size      | \n| byebye    |'
    client_socket.sendall(menu.encode())
    while True:
        message = client_socket.recv(recv).decode()
        if message == 'byebye':
            break
        else:
            process_message(client_socket, message)
    ```
    fungsi diatas akan menerima parameter **client_socket** yang nantinya digunakan untuk mengirimkan pesan kepada klien
    saat fungsi **loopMessage()** dijalankan, maka akan mengirimkan pesan berupa menu layanan yang tersedia di server
    ![list menu](https://github.com/Codex2142/Prokjar2/blob/main/img/Capture.PNG?raw=true)
    setelah mengirimkan pesan kepada klien. server akan menerima respon pesan yang nantinya akan diproses dengan catatan, pesan yang diterima selain **'byebye'** lalu melanjutkan ke fungsi process_message()

3. Fungsi process_message()
    ```python
    def process_message(client_socket, message):
    print(f"Received: {message}")
    response = "Apakah ada yang bisa dibantu? "
    client_socket.sendall(response.encode())
    perintah = message.split()
    if len(perintah) == 2 :
        menu, file = perintah
        print(menu)
        print(file)
        if menu == 'download':
            download(client_socket, file)
        elif menu == 'upload':
            upload(client_socket, file)
        elif menu == 'size':
            size(client_socket, file)
        elif message == 'rm':
            rm(client_socket, file)
    else:
        if message == 'ls':
            ls(client_socket)
        elif message == 'byebye':
            client_socket.close()
    ```
    Fungsi **process_message()** menerima pesan dari klien, memprosesnya, dan memberikan respon. Jika pesan terdiri dari dua kata, dipisahkan menjadi **perintah** dan **nama file**. Jika perintah adalah 'download', 'upload', 'size', atau 'rm', fungsi akan memanggil fungsi yang telah ditentukan. Jika hanya satu kata dan itu adalah 'ls' atau 'byebye', fungsi akan memanggil fungsi yang ditentukan. Jika perintah tidak dikenali,maka perintah tidak akan dieksekusi

4. Fungsi ls()
    ```python
    def ls(client_socket):
        path = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//server"
        dirList = os.listdir(path)
        print(dirList)
        client_socket.sendall(str(dirList).encode())
    ```
    Fungsi **ls()** digunakan untuk mendapatkan daftar file dan direktori dalam suatu direktori pada server. Fungsi ini mengambil path dari direktori yang ingin di-list, kemudian menggunakan fungsi **os.listdir()** untuk mendapatkan daftar file dan direktori dalam path tersebut. Setelah itu, daftar tersebut dikirim kembali ke klien sebagai respon menggunakan soket klien dengan metode **sendall()**, setelah diubah menjadi string dan diencode terlebih dahulu.

5. Fungsi download()
    ```python
    def download(client_socket, file):
        server_dir = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//server"
        client_dir = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//client"
    
        server_file_path = os.path.join(server_dir, file)
    
        client_file_path = os.path.join(client_dir, file)
    
        if os.path.exists(server_file_path):
            with open(server_file_path, 'rb') as server_file:
                file_content = server_file.read()
            
                with open(client_file_path, 'wb') as client_file:
                    client_file.write(file_content)
            pesan = 'file berhasil didownload'
            client_socket.sendall(pesan.encode())
    ```
    Fungsi **download()** digunakan untuk mengunduh file dari server ke client. Pertama, fungsi ini mengambil path lengkap dari file yang ingin diunduh di server dan path lengkap tempat penyimpanan di client. Kemudian, fungsi mengecek apakah file tersebut ada di server menggunakan **os.path.exists()**. Jika file ada, maka file tersebut dibuka dalam mode binary untuk dibaca menggunakan **open()**, kemudian konten file tersebut dibaca dan ditulis ke file dengan path yang telah disiapkan di client. Setelah proses unduh selesai, pesan yang menyatakan bahwa unduhan berhasil dilakukan dikirim kembali ke klien menggunakan soket klien dengan metode **sendall()**
6. Fungsi Upload
    ```python
    def upload(client_socket ,file):
        server_dir = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//server"
        client_dir = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//client"

        server_file_path = os.path.join(server_dir, file)
        client_file_path = os.path.join(client_dir, file)

        if os.path.exists(client_file_path):
            with open(client_file_path, 'rb') as client_file:
                file_content = client_file.read()

                with open(server_file_path, 'wb') as server_file:
                    server_file.write(file_content)
                pesan = 'file berhasil diupload'
                client_socket.sendall(pesan.encode())
    ```
    Fungsi upload merupakan kebalikan dari fungsi **download()**. Fungsi ini digunakan untuk mengunggah file dari client ke server. Pertama, fungsi ini mengambil path lengkap dari file yang ingin diunggah di client dan path lengkap tempat penyimpanan di server. Kemudian, fungsi mengecek apakah file tersebut ada di client menggunakan **os.path.exists()**. Jika file ada, maka file tersebut dibuka dalam mode binary untuk dibaca menggunakan **open()**, kemudian konten file tersebut dibaca dan ditulis ke file dengan path yang telah disiapkan di server. Setelah proses unggah selesai, pesan yang menyatakan bahwa unggahan berhasil dilakukan dikirim kembali ke klien menggunakan soket klien dengan metode **sendall()**
    
7. Fungsi size()
    ```python
    def size(client_socket, file):
        server_path = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//server"
        serverFile = os.path.join(server_path, file)
    
        if os.path.exists(serverFile):
            file_size_bytes = os.path.getsize(serverFile)
            file_size_kb = file_size_bytes / 1024
            size_message = f"Ukuran file {file}: {file_size_kb:.2f} kB"
            client_socket.sendall(size_message.encode())
        else:
            not_found_message = 'File tidak ditemukan'
            client_socket.sendall(not_found_message.encode())
    ```
    
    Fungsi**size()** digunakan untuk mengirimkan ukuran file dari server ke klien. fungsi ini mengambil path lengkap dari file yang akan dicek ukurannya di server. Kemudian, menggunakan **os.path.exists()**, fungsi memeriksa apakah file tersebut ada di server. Jika file ditemukan, ukuran file dihitung menggunakan **os.path.getsize()**, kemudian diubah ke kilobit (kB) dan disertakan dalam pesan yang akan dikirimkan ke klien. Pesan tersebut mengandung informasi tentang nama file dan ukuran file dalam kB. Jika file tidak ditemukan, pesan "File tidak ditemukan" dikirimkan ke klien. Pesan-pesan tersebut dikirim menggunakan soket klien dengan metode **sendall()**
8. Fungsi rm()
    ```python
    def rm(client_socket, file):
        server_path = "G://Riwayat Kuliah//Semester 4//Pr. Pemrograman Jaringan//Week 6//server"
        serverFile = os.path.join(server_path, file)
    
        if os.path.exists(serverFile):
            os.remove(serverFile)
            pesan = 'file berhasil dihapus'
            client_socket.sendall(pesan.encode())
        else:
            pesan = 'file tidak ditemukan'
            client_socket.sendall(pesan.encode())
    ```
    Fungsi **rm()** digunakan untuk menghapus file dari server. Pertama, fungsi ini membentuk path lengkap dari file yang akan dihapus di server. Kemudian, menggunakan **os.path.exists()**, fungsi memeriksa apakah file tersebut ada di server. Jika file ditemukan, **os.remove()** digunakan untuk menghapus file tersebut. Selanjutnya, sebuah pesan yang menyatakan bahwa file berhasil dihapus disiapkan dan dikirimkan ke klien menggunakan metode **sendall()** dari soket klien. Jika file tidak ditemukan, pesan yang menyatakan bahwa file tidak ditemukan juga dikirimkan ke klien.
        
## Penjelasan kode program client
```python
import socket
alamat = ('localhost', 12345)
recv = 1024

def main():
    message = input('masukkan pesan: ')
    while message == 'connme':
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (alamat)
        client_socket.connect(server_address)
        loopMessage(client_socket)

def loopMessage(client_socket):
    while True:
        data = client_socket.recv(recv)
        print(f'{data.decode()}')
        message = input('Masukkan Pesan: ')
        client_socket.sendall(message.encode())
        if message == 'byebye':
            client_socket.close()
            break
        elif message == 'ls':
            ls = client_socket.recv(recv)
            print(ls)
        perintah = message.split()
        if len(perintah) == 2 :
            menu, file = perintah
            if menu == 'download':
                download(client_socket)
            elif menu == 'upload':
                upload(client_socket)
            elif menu == 'size':
                size(client_socket)
            elif message == 'rm':
                rm(client_socket)

def download(client_socket):
    pesan = client_socket.recv(recv)
    print(pesan.decode())

def upload(client_socket):
    pesan = client_socket.recv(recv)
    print(pesan.decode())

def size(client_socket):
    pesan = client_socket.recv(recv)
    print(pesan.decode())

def rm(client_socket):
    pesan = client_socket.recv(recv)
    print(pesan.decode())
if __name__ == '__main__':
    main()

```

1. Fungsi main()
    ```python
    def main():
    message = input('masukkan pesan: ')
    while message == 'connme':
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (alamat)
        client_socket.connect(server_address)
        loopMessage(client_socket)
    ```
    Fungsi **main()** bertujuan untuk menginisialisasi koneksi dengan server. Pertama, pengguna diminta untuk memasukkan pesan dengan menggunakan fungsi input. Jika pesan yang dimasukkan sama dengan string **'connme'**, maka program akan membuat soket klien dengan **socket.socket()**, kemudian menghubungkannya dengan server menggunakan **client_socket.connect()**. Setelah itu, fungsi loopMessage akan dipanggil untuk memulai proses komunikasi antara klien dan server. Program akan terus berjalan sampai pesan yang dimasukkan tidak lagi sama dengan **'connme'**
2. Fungsi loopMessage()
    ```python
    def loopMessage(client_socket):
    while True:
        data = client_socket.recv(recv)
        print(f'{data.decode()}')
        message = input('Masukkan Pesan: ')
        client_socket.sendall(message.encode())
        if message == 'byebye':
            client_socket.close()
            break
        elif message == 'ls':
            ls = client_socket.recv(recv)
            print(ls)
        perintah = message.split()
        if len(perintah) == 2 :
            menu, file = perintah
            if menu == 'download':
                download(client_socket)
            elif menu == 'upload':
                upload(client_socket)
            elif menu == 'size':
                size(client_socket)
            elif message == 'rm':
                rm(client_socket)
    ```
    
    Fungsi **loopMessage()** bertujuan untuk mengatur pesan antara klien dan server. klien menerima pesan dari server menggunakan **client_socket.recv()**, kemudian pesan tersebut dicetak menggunakan **print()**. Selanjutnya, klien diminta untuk memasukkan pesan menggunakan **input('Masukkan Pesan: ')**. Pesan yang dimasukkan oleh klien dikirimkan kembali ke server menggunakan **client_socket.sendall()**. Jika pesan yang dimasukkan adalah **'byebye'**, koneksi klien ditutup menggunakan **client_socket.close()** dan loop dihentikan dengan break. Jika pesan adalah **'ls'**, klien menerima daftar file dari server menggunakan **client_socket.recv()**, kemudian dicetak menggunakan **print()** dan menu seterusnya
Kemudian, pesan yang dimasukkan oleh klien dipisahkan menjadi dua bagian menggunakan message.split(), yaitu menu dan nama file. Jika panjang list hasil pemisahan adalah 2, artinya pesan mengandung perintah untuk mengelola file. Selanjutnya, klien melakukan operasi sesuai dengan perintah yang diterima.
3. Fungsi download()
    ```python
    def download(client_socket):
        pesan = client_socket.recv(recv)
        print(pesan.decode())
    ```
    Fungsi **download()** menerima pesan dari server yang berisi file yang didownload. Pesan tersebut kemudian di-decode dan dicetak menggunakan **print()**
4. Fungsi upload()
    ```python
    def upload(client_socket):
        pesan = client_socket.recv(recv)
        print(pesan.decode())
    ```
    Fungsi **upload()** menerima pesan dari server yang berisi file yang di upload. Pesan tersebut kemudian di-decode dan dicetak menggunakan **print()**
5. Fungsi size()
    ```python
    def size(client_socket):
        pesan = client_socket.recv(recv)
        print(pesan.decode())
    ```
   Fungsi **size()** menerima pesan dari server yang berisi file diketahui ukurannya. Pesan tersebut kemudian di-decode dan dicetak menggunakan **print()**
6. Fungsi ls()
    ```python
    def rm(client_socket):
        pesan = client_socket.recv(recv)
        print(pesan.decode())
    ```
    Fungsi **ls()** menerima pesan dari server yang berisi file yang akan dihapus. Pesan tersebut kemudian di-decode dan dicetak menggunakan **print()**
## Mempraktikkan hubungan antara klien dan server
1. Menjalankan Kedua program
    cara menjalankan kedua program diatas adalah dengan mengetikkan

    server:
    ```sh
    python server.py
    ```
    ![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/server.png?raw=true)
    
    client:
    ```sh
    python client.py
    ```
    ![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/client.png?raw=true)

2. Tampilan awal dari kedua program

    server:
    ![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/waiting.PNG?raw=true)
    
    client:
    ketikkan perintah dibawah ini supaya dapat terkoneksi dengan server
    ```sh
    connme
    ```
    ![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/connme.PNG?raw=true)
        menghubungkan ke server (client.py)


3. Mengakses layanan pada server menggunakan client .py
    - melihat list file pada direktori server
        ```sh
        ls
        ```
        ![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/ls.PNG?raw=true)
    - mendownload file dari server
        ```sh
        download download.txt
        ```
        ![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/download1.PNG?raw=true)
        dibawah ini adalah tampilan berhasil di downlaod
        ![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/download2.PNG?raw=true)
    - mengupload file ke server
        ```sh
        upload upload.txt
        ```
        ![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/upload1.PNG?raw=true)
        dibawah ini adalah tampilan berhasil di upload
        ![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/upload2.PNG?raw=true)
    - melihat ukuran file pada server
        ```sh
        size test.py
        ```
        ![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/size.PNG?raw=true)
    - menghapus file ke direktori server
        ```sh
        rm test.py
        ```
        ![hapus](https://github.com/Codex2142/Prokjar2/blob/main/img/rmf.PNG?raw=true)
    - mengakhiri koneksi dengan server
        ```sh
        byebye
        ```
        server dan klien akan otomatis tertutup dan koneksi terputus

## TUGAS TAMBAHAN
    kode server:
    ```python
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

    ```

kode untuk client:
```python
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

```

## Tampilan singkat

![extract file](https://raw.githubusercontent.com/Codex2142/Prokjar2/main/img/1t.PNG)
klien meminta untuk terkoneksi dengan mengetikkan
```sh
    connme
```

![extract file](https://raw.githubusercontent.com/Codex2142/Prokjar2/main/img/2t.PNG)
gambar untuk menampilkan file yang ada di direktori



![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/5t.PNG?raw=true)
![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/4t.PNG?raw=true)
![extract file](https://github.com/Codex2142/Prokjar2/blob/main/img/6t.PNG?raw=true)
