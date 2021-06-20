from unix_sock import *

uclient = setup_unix_client("unix.sock")

msg, fds = recv_fds(uclient, 4096, 10)

print(msg)

csock = socket.fromfd(fds[0], socket.AF_INET, socket.SOCK_STREAM)

while True:
    data = csock.recv(4096)
    if data == b"exit" or data == b"":
        print("bye")
        csock.close()
        break
    else:
        csock.send(b"recv " + data)
