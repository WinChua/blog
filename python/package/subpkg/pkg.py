from .. import sub1
from . import pkg
print(__file__)
print(__name__)
import sys
print("equal:", sys.modules["__main__"] == sys.modules["package.subpkg.pkg"])

print("sub1 is", sub1)
