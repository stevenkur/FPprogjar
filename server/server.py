import socket
import os
import threading

current_directory = os.path.abspath('./Dataset')
ip_address = ''
port = 30000

file_user = open('user_ftp.txt', 'r')
user_ftp = []
count_user = 0
while True:
    u = file_user.readline()
    if not u:
        break
    user_ftp.append((u.split()[0],u.split()[1]))
    count_user += 1

class clientHandler(threading.Thread):
    def __init__(self, (connection, address)):
        super(clientHandler, self).__init__()
        self.connection = connection
        self.base_working_directory = current_directory
        self.current_working_directory = self.base_working_directory
        self.username = ""
        self.login = False

    def run(self):
        self.connection.send('220 Welcome! FTP server\r\n')
        self.connection.send('220 Team: bayu, rifat, rey, kurkur\r\n')
        self.connection.send('220 Please Check: https://github.com/stevenkur/FPprogjar\r\n')
        while True:
            command = self.connection.recv(BUFF)
            print command[:4]
            if command[:4] == "USER" or command[:4] == "PASS" or self.login:
                print self.getName() + " using " + command
                try:
                    function = getattr(self, command.split()[0].strip().upper())
                    function(command)
                except Exception, e:
                    print 'ERROR:', e
                    self.connection.send('500 Syntax Error.\r\n')
            elif not command:
                self.connection.close()
                break
            else:
                self.connection.send('530 Please login with USER and PASS\r\n')

    def USER(self, command):
        self.username = command.strip().split()[1]
        kirim = '331 Password required for ' + self.username + '\r\n'
        self.connection.send(kirim)

    def PASS(self, command):
        password = command.strip().split()[1]
        flag = False
        for i in range(len(user_ftp)):
            if self.username == user_ftp[i][0] and password == user_ftp[i][1]:
                flag = True
        if flag:
            self.connection.send('230 Logged on\r\n')
            self.login = True
        else:
            self.connection.send('530 Login or password incorrect!\r\n')
            self.username = ""
            self.login = False

    def PWD(self,command):
        current_working_directory= os.path.relpath(self.current_working_directory,self.base_working_directory)
        if current_working_directory == '.':
            current_working_directory = '/'
        else:
            current_working_directory = '/' + current_working_directory
        self.connection.send('257 \"%s\"\r\n' % current_working_directory)

    def CWD(self,command):
        change_working_directory = command[4:-2]
        if change_working_directory =='/':
            self.current_working_directory =self.base_working_directory
        elif change_working_directory[0]=='/':
            self.current_working_directory=os.path.join(self.base_working_directory,change_working_directory[1:])
        else:
            self.current_working_directory=os.path.join(self.current_working_directory,change_working_directory)
        self.connection.send('250 OK.\r\n')

class FTPmain(threading.Thread):
    def __init__(self, server_address):
        super(FTPmain, self).__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(server_address)
        self.input_socket = [self.server_socket]

    def run(self):
        self.server_socket.listen(3)
        while True:
            read_ready, write_ready, exception = select.select(self.input_socket, [], [])
            # print read_ready
            for socket in read_ready:
                if socket == self.server_socket:
                    thr = clientHandler(self.server_socket.accept())
                    thr.daemon = True
                    thr.start()

    def stop(self):
        self.server_socket.close()

if __name__ == '__main__':
    server_address = (ip_address, port)
    ftp=FTPmain(server_address)
    ftp.daemon=True
    ftp.start()
    print 'On', server_address[0], ':', server_address[1]
    raw_input('Press Enter to Stop\n')
    ftp.stop()