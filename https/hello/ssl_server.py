import ssl
import socket
from ssl import SSLContext
context = SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain(certfile="cert.pem", keyfile="cert.pem")
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
srv_sock.bind(("127.0.0.1", 8443))
srv_sock.listen(5)
ssock = context.wrap_socket(srv_sock, server_side = True)
print(ssock._closed)
conn, addr = ssock.accept()
print("accept connect from", addr)
data = conn.recv(4096)
print("data is", data.decode("utf8"))

