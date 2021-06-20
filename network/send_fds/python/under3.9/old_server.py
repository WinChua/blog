from unix_sock import *


unix_server = setup_unix_server("unix.sock")
print("ready to connect to unix server")
unix_client, addr = unix_server.accept()
print(unix_client, addr)

server_socket = setup_tcp_server(12345)
client_socket, addr = server_socket.accept()

print("ready")

send_fds(unix_client, b"Hello", [client_socket.fileno()])

