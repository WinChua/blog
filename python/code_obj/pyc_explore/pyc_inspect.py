import sys
sys.path.insert(0, "../")
import utils
import marshal
import inspect
import struct

with open(sys.argv[1], "rb") as f:
    data = f.read()

headers = {}
headers["magic"] = data[:4]
headers["version"] = data[4:8]
headers["timestamp"] = data[8:12]
headers["source_filesize"] = data[12:16]

for k, v in headers.items():
    headers[k] = struct.unpack("I", v)
    v = headers[k][0]
    print(f"{k} is {v}")

code_obj = marshal.loads(data[16:])
print(code_obj)
utils.show_code(code_obj)
