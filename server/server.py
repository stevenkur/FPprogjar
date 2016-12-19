import socket
import threading

class FTPmain(threading.Thread):
    def __init__(self, server_address):
        super(FTPmain, self).__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(server_address)

    def run(self):
        print "FTPmain jalan"

    def stop(self):
        self.server_socket.close()

if __name__ == '__main__':
    server_address = ('', 30000)
    ftp=FTPmain(server_address)
    ftp.daemon=True
    ftp.start()
    print 'server ', server_address[0], ':', server_address[1]
    raw_input('Press Enter to Stop\n')
    ftp.stop()