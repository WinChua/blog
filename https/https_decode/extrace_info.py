with open("https_client_hello.bin", "rb") as f:
    data = f.read()


def get_byte_value(byte):
    value = 0
    for b in byte:
        value = (value << 8) + b
    return value

def get_client_hello(data):
    record_type = data[0]
    protocol_version = data[1:3]
    msg_len = data[3:5]
    return record_type, protocol_version, get_byte_value(msg_len)

def get_handshake_header(data):
    return data[0], get_byte_value(data[1:4])

def get_client_version(data):
    return data[:2]

def get_client_random(data):
    return data[:32]

def get_session_info(data):
    session_len = data[0]
    session_id = get_byte_value(data[1:1+session_len])
    return session_len, session_id

print("header info:", get_client_hello(data))
print("handshake info:", get_handshake_header(data[5:]))
print("client version info:", get_client_version(data[9:]))
print("client random data:", get_client_random(data[11:]), len(get_client_random(data[11:])))
print("session_id:", get_session_info(data[44:]))
