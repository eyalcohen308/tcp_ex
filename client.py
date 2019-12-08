import socket
import sys
import os


def mode_0_listener_client(dest_ip, dest_port, local_port):
	sock = connect(dest_ip, dest_port)
	# create list of files names in the current directory
	files_list = os.listdir(".")
	files_list_string = ",".join(files_list)
	msg_to_server = "1 {0} {1}".format(str(local_port), files_list_string)
	# TODO: delete the next print line.
	print("msg:", msg_to_server)
	sock.send(msg_to_server.encode())
	sock.close()


def mode_0_client_server(local_port):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_ip = '0.0.0.0'
	server_port = local_port
	server.bind((server_ip, server_port))
	server.listen(5)

	while True:
		client_socket, client_address = server.accept()
		data = client_socket.recv(1024).decode()
		send_file(data, client_socket)


def mode1_user_client(ip, port):
	while True:
		print("Search: ", end='')
		search_txt = input()
		sock = connect(ip, port)
		msg_to_server = "2 {0}".format(search_txt)
		sock.send(msg_to_server.encode())
		resp = sock.recv(4096).decode()
		sock.close()

		resp = resp.split(',')
		file_ip_port_tuples_list = [tuple(x.split(' ')) for x in resp]
		file_ip_port_tuples_list.sort(key=lambda tup: tup[0])
		for i, client_data in enumerate(file_ip_port_tuples_list):
			print(i + 1, client_data[0])
		print("Choose: ", end='')
		choice = int(input())
		client_data = resp[choice - 1]
		get_file(client_data[0], client_data[1], int(client_data[2]))


def send_file(file_name, sock):
	file_reader = open(file_name, 'rb')
	buff = file_reader.read(1024)
	while buff:
		sock.send(buff)
		buff = file_reader.read(1024)
	file_reader.close()
	sock.close()


def get_file(file_name, ip, port):
	sock = connect(ip, port)
	sock.send(file_name.encode())
	file_writer = open(file_name, 'wb')
	buff = sock.recv(1024)
	while buff:
		file_writer.write(buff)
		buff = sock.recv(1024)
	file_writer.close()
	sock.close()


def connect(ip, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port))
	return s


if __name__ == '__main__':
	args = sys.argv[1:]
	if len(args) < 2:
		raise NotImplementedError("balagan")

	choice = args[0]
	if choice == "0":
		dest_ip, dest_port, local_port = args[1], int(args[2]), int(args[3])
		mode_0_listener_client(dest_ip, dest_port, local_port)
		mode_0_client_server(local_port)
	elif choice == "1":
		ip, port = args[1], int(args[2])
		mode1_user_client(ip, port)
