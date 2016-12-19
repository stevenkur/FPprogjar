import socket
import os
from select import select

BUFFER = 1024

class Client:
    def __init__(self, (ip, port)):
        self.serverIp = ip
        self.port = port
        self.server = None
        self.data_sock	= None
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
                    print "masuk getattr"
                    command+='\r\n'
                    print "masuk getattr 2"
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


def main():
    new_client = Client(('localhost',300000))
    # new_client = Client(('10.151.43.17', 12345))
    new_client.run()

if __name__ == '__main__':
    main()