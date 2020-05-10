import ssl
import socket
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations("cert.pem")
cli = context.wrap_socket(socket.socket(), server_hostname="localhost")
cli.connect(("localhost", 8443))
cli.send(b"hello")
