import os
import array
import socket


def setup_unix_server(unix_path):
    userver = socket.socket(socket.AF_UNIX)
    if os.path.exists(unix_path):
        os.unlink(unix_path)
    userver.bind(unix_path)
    userver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    userver.listen(5)
    return userver

def setup_unix_client(unix_path):
    uclient = socket.socket(socket.AF_UNIX)
    uclient.connect(unix_path)
    return uclient

def setup_tcp_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", port))
    server_socket.listen(5)
    return server_socket


def send_fds(sock, msg, fds):
    return sock.sendmsg([msg], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, array.array("i", fds))])


def recv_fds(sock, msglen, maxfds):
    fds = array.array("i")   # Array of ints
    msg, ancdata, flags, addr = sock.recvmsg(msglen, socket.CMSG_LEN(maxfds * fds.itemsize))
    for cmsg_level, cmsg_type, cmsg_data in ancdata:
        if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
            fds.frombytes(cmsg_data[:len(cmsg_data) - (len(cmsg_data) % fds.itemsize)])
            
    return msg, list(fds)
