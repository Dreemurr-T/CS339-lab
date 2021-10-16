#!usr/bin/env python3

from socket import *
import sys,os
import time

HOST = '0.0.0.0'
PORT = 12345
ADDR = (HOST,PORT)
# FILE_PATH = '/home/thy/Desktop/CNLab'

class Client:
    def __init__(self,socketfd):
        self.socketfd = socketfd
    
    def get_list(self):
        self.socketfd.send('LIST'.encode())
        data = self.socketfd.recv(128).decode()
        if data == 'LS READY':
            data = self.socketfd.recv(1024*1024*10).decode()
            print(data)
        else:
            print(data)

    def upload_file(self,filename):
        try:
            f = open(filename,'rb')
        except Exception:
            print("File does not exist.")
            return
        filename = filename.split('/')[-1]
        self.socketfd.send(('UPLOAD '+filename).encode())
        data = self.socketfd.recv(128).decode()
        time.sleep(0.1)
        if data == 'UPLOAD READY':
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.socketfd.send(b'##')
                    break
                self.socketfd.send(data)
            f.close()
        else:
            print(data)

    def download_file(self,filename):
        self.socketfd.send(('DOWNLOAD '+filename).encode())
        data = self.socketfd.recv(128).decode()
        if data == 'DOWNLOAD READY':
            f = open(filename,'wb')
            time_start = time.time()
            while True:
                data = self.socketfd.recv(1024)
                if data == b'##':
                    break
                f.write(data)
            f.close()
            time_end = time.time()
            dur = time_end - time_start
            print("Download time is %f sec" % dur)

        else:
            print(data)

    def quit(self):
        self.socketfd.send('EXIT'.encode())
        self.socketfd.close()
        sys.exit('Leaving client...')

def main():
    socketfd = socket()
    try:
        socketfd.connect(ADDR)
    except Exception as e:
        print(e)
        return
    
    ftp = Client(socketfd)

    while True:
        cmd = input("Client>>")
        if cmd == 'ls':
            ftp.get_list()
        elif cmd[:2] == 'up':
            filename = cmd.split(' ')[-1]
            ftp.upload_file(filename)
        elif cmd[:4] == 'down':
            filename = cmd.split(' ')[-1]
            ftp.download_file(filename)
        elif cmd == 'exit':
            ftp.quit()
        else:
            print('Please input a valid command')
        

if __name__ == '__main__':
    main()
