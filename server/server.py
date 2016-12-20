import socket
import os
import threading
import time
import select


BUFF = 1024
current_directory = os.path.abspath('.')
ip_address = ''
# print ip_address
port = 30000
allow_delete = True

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
        self.address = address
        self.base_working_directory = current_directory
        self.current_working_directory = self.base_working_directory
        self.pasive_mode = False
        self.username = ""
        self.login = False

    def run(self):
        self.connection.send('220 Welcome! FTP server\r\n')
        self.connection.send('220 Team: bayu, rifat, rey, stevenkur\r\n')
        self.connection.send('220 Please Check: https://github.com/stevenkur/FPprogjar\r\n')
        while True:
            try:
                command = self.connection.recv(BUFF)

                print command.split()[0]
                # print command
                if str(command.split()[0]).upper() == "USER" or str(command.split()[0]).upper() == "PASS" or self.login:
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
            except:
                continue

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
        if self.checkExist(command):
            os.chdir(change_working_directory)
            self.connection.send('250 OK.\r\n')
            if change_working_directory =='/':
                self.current_working_directory =self.base_working_directory
            elif change_working_directory[0]=='/':
                self.current_working_directory=os.path.join(self.base_working_directory,change_working_directory[1:])
            else:
                self.current_working_directory=os.path.join(    self.current_working_directory,change_working_directory)

        else:
            self.connection.send('404 Not Found.\r\n')

    def CDUP(self,cmd):
        if not os.path.samefile(self.cwd,self.basewd):
            #learn from stackoverflow
            self.cwd=os.path.abspath(os.path.join(self.cwd,'..'))
        self.conn.send('200 OK.\r\n')

    def PASV(self, cmd):  # from http://goo.gl/3if2U
        self.pasive_mode = True
        self.pasive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pasive_socket.bind((ip_address, 0))
        self.pasive_socket.listen(1)
        self.data_ip, self.data_port = self.pasive_socket.getsockname()
        print self.data_ip
        print 'open', self.data_ip, self.data_port
        self.connection.send('227 Entering Passive Mode (%s,%u,%u).\r\n' %
                       (','.join(self.data_ip.split('.')), self.data_port >> 8 & 0xFF, self.data_port & 0xFF))

    def start_datasock(self):
        if self.pasive_mode:
            self.data_socket, addr = self.pasive_socket.accept()
            print 'connect:', addr
        else:
            self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.data_socket.connect((self.data_ip, self.data_port))

    def stop_datasock(self):
        self.data_socket.close()
        if self.pasive_mode:
            self.pasive_socket.close()

    def QUIT(self, command):
        self.connection.send('221 Goodbye.\r\n')
        self.login = False

    def LIST(self,cmd):

        self.connection.send('150 List directory.\r\n')
        print 'list:', self.current_working_directory
        self.start_datasock()
        listFile=''
        for t in os.listdir(self.current_working_directory):
            listFile+=self.detail(os.path.join(self.current_working_directory,t))
            listFile+='\r\n'
        print listFile
        self.data_socket.sendall(listFile)
        self.stop_datasock()
        self.connection.send('226 Directory send OK.\r\n')

    def detail(self, fn):
        st = os.stat(fn)
        fullmode = 'rwxrwxrwx'
        mode = ''
        for i in range(9):
            mode += ((st.st_mode >> (8 - i)) & 1) and fullmode[i] or '-'
        d = (os.path.isdir(fn)) and 'd' or '-'
        ftime = time.strftime(' %b %d %H:%M ', time.gmtime(st.st_mtime))
        return d + mode + ' 1 user group ' + str(st.st_size) + ftime + os.path.basename(fn)

    def HELP(self, command):
        pesan = "Commands may be abbreviated. Commands are:\n USER\t PASS\t CWD\t QUIT\n RETR\t STOR\t RNTO\t DELE\n RMD\t MKD\t PWD\t LIST\n HELP\n"
        self.connection.send(pesan)

    def checkExist(self, command):
        cmd = command.split(' ', 1)[1]
        if os.path.isdir(str(cmd.strip())):
            print "true"
            return True
        elif os.path.isfile(str(command.strip())):
            print "true"
            return True
        else:
            print "false"
            return False

    def RNFR(self, cmd):
        if self.checkExist(cmd):
            self.rnfr = os.path.join(self.current_working_directory, str(cmd.split(' ', 1)[1]).strip())
            print 'rnfr: ' + self.rnfr
            self.connection.send('350 Ready.\r\n')
        else:
            self.connection.send('404 Not Found\r\n')

    def RNTO(self, cmd):
        rnto = os.path.join(self.current_working_directory, str(cmd.split(' ', 1)[1]).strip())
        print 'rnto: ' + rnto
        os.rename(self.rnfr, rnto)
        self.connection.send('250 File renamed.\r\n')

    def MKD(self, command):
        dirname = os.path.join(self.current_working_directory, command.split(" ", 1)[1].strip())
        # print dirname
        os.mkdir(dirname)
        self.connection.send('257 Directory created.\r\n')

    def RMD(self, command):
        dirname = os.path.join(self.current_working_directory, command.split(" ", 1)[1].strip())
        if self.checkExist(command):
            if allow_delete:
                os.rmdir(dirname)
                self.connection.send('250 Directory deleted.\r\n')
            else:
                self.connection.send('450 Not allowed.\r\n')
        else:
            self.connection.send('404 Not Found.\r\n')

    def DELE(self, command):
        filename = os.path.join(self.current_working_directory, command.split(" ", 1)[1].strip())
        if self.checkExist(command):
            if allow_delete:
                os.remove(filename)
                self.connection.send('250 File delete.\r\n')
            else:
                self.connection.send('450 Not allowed.\r\n')
        else:
            self.connection.send('404 Not Found.\r\n')
    def RETR(self,command):
        print command
        requestedfile=os.path.join(self.current_working_directory,command.split()[1].strip())
        print 'Downloading: ', requestedfile
        filesize=os.stat(requestedfile).st_size
        print filesize
        self.connection.send('filesize: '+ str(filesize))
        inputfile=open(requestedfile,'rb')
        self.connection.send('150 Opening data connection.\r\n')
        data=inputfile.read(1024)
        self.start_datasock()
        while data:
            self.data_socket.send(data)
            data=inputfile.read(1024)
        inputfile.close()
        self.stop_datasock()
        self.connection.send('226 Transfer complete.\r\n')

    def STOR(self,command):
        requestedfile=os.path.join(self.current_working_directory,command.split()[1].strip())
        print 'Uploading: ', requestedfile
        outputfile=open(requestedfile,'wb')
        self.connection.send('150 Opening data connection.\r\n')
        self.start_datasock()
        while True:
            data=self.data_socket.recv(1024)
            if not data: break
            outputfile.write(data)
        outputfile.close()
        self.stop_datasock()
        self.connection.send('226 Transfer complete.\r\n')

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