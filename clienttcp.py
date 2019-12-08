import socket, sys
from os import listdir
from os.path import isfile


def mode0(dest_ip, dest_port, local_port):
    s = connect(dest_ip, dest_port)
    files = [f for f in listdir('.') if isfile(f)]
    msg = "1" + " " + str(local_port) + " " + str(files)[1:-1].replace(" ","").replace("'","")
    print("my msg",msg)
    s.send(msg.encode())
    s.close()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '0.0.0.0'
    server_port = local_port
    server.bind((server_ip, server_port))
    server.listen(5)

    while True:
        client_socket, client_address = server.accept()
        data = client_socket.recv(1024).decode()
        send_file(data, client_socket)


def mode1(ip, port):
    while True:
        print("Search: ", end='')
        search = input()
        s = connect(ip, port)
        msg = "2 " + search
        s.send(msg.encode())
        resp = s.recv(4096).decode()
        s.close()
        resp = resp.split(',')
        resp = [tuple(x.split(' ')) for x in resp]
        resp.sort(key=lambda tup: tup[0])
        for i in range(len(resp)):
            print(i+1, resp[i][0])
        print("Choose: ", end='')
        choice = int(input())
        usr = resp[choice-1]
        get_file(usr[0], usr[1], int(usr[2]))


def send_file(file_name, s):
    # s = connect(ip, port)
    f = open(file_name,'rb')
    buff = f.read(1024)
    while buff:
        s.send(buff)
        buff = f.read(1024)
    f.close()
    s.close()


def get_file(file_name, ip, port):
    s = connect(ip, port)
    s.send(file_name.encode())
    f = open(file_name, 'wb')
    buff = s.recv(1024)
    while buff:
        f.write(buff)
        buff = s.recv(1024)
    f.close()
    s.close()


def connect(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == "1":
        mode0(args[1], int(args[2]), int(args[3]))
    elif args[0] == "2":
        mode1(args[1], int(args[2]))
