import inspect
import sys
import opcode
import dis

v = sys.version_info
PY_VER = f'{v.major}.{v.minor}.{v.micro}'

co_flag = [i for i in dir(inspect) if i.startswith("CO_")]

def show_flag(code):
    if hasattr(code, "__code__"):
        code = code.__code__
    return ",".join(f for f in co_flag if getattr(inspect, f) & code.co_flags)

def show_code(code_obj):
    if hasattr(code_obj, "__code__"):
        code_obj = code_obj.__code__
    for i in dir(code_obj):
        if i.startswith("co_"):
            print(i, getattr(code_obj, i))


# CO_NEWLOCALS
def with_newlocals(a):
    def hello(b):
        return a + b
    return hello


def with_kw(**kwargs):
    pass

def with_va(*args):
    pass

with_nested = with_newlocals(42)

def with_generator(a):
    for i in range(a):
        yield i

def with_kwonly(a,*, abc=23):
    print(abc)

HAVE_ARGUMENT = opcode.HAVE_ARGUMENT
EXTENDED_ARG = opcode.EXTENDED_ARG

def unpack_opargs(code):
    extended_arg = 0
    for i in range(0, len(code), 2):
        op = code[i]
        if op >= HAVE_ARGUMENT:
            arg = code[i+1] | extended_arg
            extended_arg = (arg << 8) if op == EXTENDED_ARG else 0
        else:
            arg = None
        yield (i, op, arg)

if PY_VER >= "3.8":
    with_argonly = '''def with_argonly(a,b,/,c,d,*,e,f):
    pass
'''
else:
    with_argonly = '''def with_argonly(a, b, c):
    pass
'''

exec(with_argonly)

keys = list(locals().keys())

for k in keys:
    if isinstance(locals()[k], type(with_newlocals)):
        f = locals()[k]
        print(k)
        print(show_flag(f))

#show_code(with_argonly)

def with_jump(a):
    if a > 42:
        return False
    else:
        return True

uo = list(unpack_opargs(unpack_opargs.__code__.co_code))
code = unpack_opargs.__code__
gi = list(dis._get_instructions_bytes(code.co_code, code.co_varnames, code.co_names, code.co_consts, code.co_cellvars))
for a in uo:
    print(a)

print(len(uo))
print(len(gi))
for a in gi:
    print(a._disassemble())
print('hello')
dis.dis(unpack_opargs)
