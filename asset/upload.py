#! python

import os
import sys

base_path = os.path.dirname(sys.argv[0])
repo = "https://github.com/WinChua/blog/blob/master/asset/"

def move(i):
    basename = os.path.basename(i)
    os.system(f"cp {i} {base_path}")
    os.system(f"cd {base_path} && git add . ")
    os.system(f"cd {base_path} && git commit -m 'add pic'")
    os.system(f"cd {base_path} && git push origin master")
    print(os.path.join(repo, basename))

print("Upload Success:")
for i in sys.argv[1:]:
    move(i)
