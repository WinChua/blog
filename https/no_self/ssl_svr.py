import ssl
import socket

cert = "mycert.pem"
key = "mykey.pem"
#cert = "/etc/pki/CA/cacert.pem"
#key = "/etc/pki/CA/private/cakey.pem"
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert, key)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('localhost', 8443))
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        conn.send(b"hello")
        ## conn.send(b"hello")
