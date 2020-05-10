import socket
import ssl

#hostname = 'www.python.org'
hostname = "localhost"
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
#context = ssl.create_default_context()
#context.load_verify_locations('cert/mycertfile.pem')
context.load_verify_locations("yourcert.pem")


with socket.create_connection((hostname, 8443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version())
