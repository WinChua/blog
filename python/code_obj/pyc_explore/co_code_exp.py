import struct
import dis

def genIns(code):
    return dis._get_instructions_bytes(code.co_code, code.co_varnames, code.co_names, code.co_consts, code.co_cellvars)
