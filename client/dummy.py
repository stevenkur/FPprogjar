import socket
import os
from select import select

ip_server = 'localhost'
BUFFER = 1024

currentDirectory = os.path.abspath('.')


# print currentDirectory


class Client:
    def __init__(self, (ip, port)):
        self.serverIp = ip
        self.port = port
        self.server = None
        self.data_sock = None
        self.recvData = ""
        self.currentDirectory = currentDirectory
        self.isi = ""

    def run(self):
        self.open_socket()
        while True:
            # input command
            command = raw_input('Command: ')
            if not command:
                break
            else:
                print '---- Command:', command.split()[0].strip().upper()
                try:
                    function = getattr(self, command.split()[0].strip().upper())
                    # print "masuk getattr"
                    command += '\r\n'
                    # print "masuk getattr 2"
                    function(command)
                except Exception, e:
                    print 'ERROR:', e

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.serverIp, self.port))
        # msg = self.server.recv(2048)
        # print msg
        while True:
            reads, writes, errors = select([self.server], [], [], 1)
            if not reads:
                break
            else:
                for read in reads:
                    msg = self.server.recv(2048)
                    print msg.strip()

    def USER(self, command):
        self.server.send(command)
        msg = self.server.recv(BUFFER)
        print msg.rstrip()

    def PASS(self, command):
        self.server.send(command)
        msg = self.server.recv(BUFFER)
        print msg.rstrip()

    def PWD(self, command):
        self.server.send(command)
        msg = self.server.recv(BUFFER)
        print msg.rstrip()

    def QUIT(self, command):
        self.server.send(command)
        msg = self.server.recv(BUFFER)
        print msg.rstrip()

    def CWD(self, command):
        self.server.send(command)
        msg = self.server.recv(BUFFER)
        print msg.rstrip()

    def LIST(self, command):

        port = self.PASV("PASV\r\n")

        self.server.send(command)
        msg = self.server.recv(BUFFER)
        print msg.strip()

        self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_sock.connect((self.serverIp, port))

        self.recvdata = self.data_sock.recv(1024)
        print self.recvdata.strip()
        msg = self.server.recv(1024)
        print msg.strip()

    def PASV(self, command):
        self.server.send(command)
        msg = self.server.recv(1024)
        print msg.strip()
        data = msg.strip()
        if "Entering Passive Mode" in msg:
            tp = data.split('(')[1].split(')')[0].split(',')
            port = int(tp[4]) * 256 + int(tp[5])
        return port

    def MKD(self, command):
        self.server.send(command)
        msg = self.server.recv(BUFFER)
        print msg.rstrip()

    def RNTO(self, command):
        self.server.send(command)
        msg = self.server.recv(BUFFER)
        print msg.rstrip()

    def RNFR(self, command):
        self.server.send(command)
        msg = self.server.recv(BUFFER)
        print msg.rstrip()

    def HELP(self, command):
        print "masuk sini"
        self.server.send(command)
        msg = self.server.recv(BUFFER)
        print msg.rstrip()

    def CDUP(self, command):
        self.server.send(command)
        msg = self.server.recv(BUFFER)
        print msg.rstrip()

    def RMD(self, command):
        self.server.send(command)
        msg = self.server.recv(BUFFER)
        print msg.rstrip()

    def DELE(self, command):
        self.server.send(command)
        msg = self.server.recv(BUFFER)
        print msg.rstrip()

    def RETR(self, command):
        filename = os.path.join(self.currentDirectory, command[5:].strip())
        port = self.PASV("PASV\r\n")
        self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_sock.connect((ip_server, port))
        command += "\r\n"
        self.server.send(command)
        msg = self.server.recv(1024)
        msg1 = self.server.recv(1024)
        print msg.strip()
        print msg1.strip()
        filesize = long(msg.split(" ")[1])
        with open(filename, 'wb') as f:
            self.isi = ""
            receive_size = 0
            while (receive_size < filesize):
                # f.write(self.isi)
                self.isi += self.data_sock.recv(4096)
                receive_size = len(self.isi)
                # print receive_size
        msg = self.server.recv(1024)
        print msg.strip()

    def STOR(self, command):
        filename = os.path.join(self.currentDirectory, command[5:].strip())
        port = self.PASV("PASV\r\n")
        self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_sock.connect((ip_server, port))

        command += "\r\n"
        self.server.send(command)
        msg = self.server.recv(1024)
        print msg.strip()

        f = open(filename, 'rb')
        l = f.read()
        f.close()
        self.data_sock.sendall(l)
        self.data_sock.close()

        msg = self.server.recv(1024)
        print msg.strip()


def main():
    new_client = Client((ip_server, 21))
    # new_client = Client(('10.151.43.17', 12345))
    new_client.run()


if __name__ == '__main__':
    main()