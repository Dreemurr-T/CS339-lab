#!usr/bin/env python3

from socket import *
import sys,os
from threading import Thread
import time

HOST = '0.0.0.0'
PORT = 12345
FILE_PATH = '/home/thy/ftp/'
ADDR = (HOST,PORT)

class Server(Thread):
    def __init__(self,conn):
        super().__init__()
        self.conn = conn
    
    def get_list(self):
        file_list = os.listdir(FILE_PATH)
        if not file_list:
            self.conn.send('The directory is empty.'.encode())
            return
        else:
            self.conn.send('LS READY'.encode())

        time.sleep(0.1)
        files = '\n'.join(file_list)
        self.conn.send(files.encode())
    
    def upload_file(self,filename):
        if os.path.exists(FILE_PATH+filename):
            self.conn.send('File already exists.'.encode())
            return
        else:
            self.conn.send('UPLOAD READY'.encode())
        
        f = open(FILE_PATH+filename,'wb')
        while True:
            data = self.conn.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()

    def download_file(self,filename):
        try:
            f = open(FILE_PATH+filename,'rb')
        except Exception:
            self.conn.send('File does not exist'.encode())
            return
        else:
            self.conn.send('DOWNLOAD READY'.encode())

        time.sleep(0.1)
        
        while True:
            data = f.read(1024)
            if not data:
                time.sleep(0.1)
                self.conn.send(b'##')
                break
            self.conn.send(data)

        f.close()
    
    def run(self):
        while True:
            cli_fb = self.conn.recv(1024).decode()
            if not cli_fb or cli_fb == 'EXIT':
                return
            elif cli_fb[:4] == 'LIST':
                self.get_list()
            elif cli_fb[:6] == 'UPLOAD':
                filename = cli_fb.split(' ')[-1]
                self.upload_file(filename)
            elif cli_fb[:8] == 'DOWNLOAD':
                filename = cli_fb.split(' ')[-1]
                self.download_file(filename)

def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(3)
    while True:
        try:
            conn,addr = s.accept()
        except Exception as e:
            print(e)
            continue
        except KeyboardInterrupt:
            sys.exit('Closing server...')
        
        t = Server(conn)
        t.setDaemon(True)
        t.start()

if __name__ == '__main__':
    main()



