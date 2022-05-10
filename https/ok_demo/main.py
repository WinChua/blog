import sys
from flask import Flask

app = Flask(__name__)

app.run(ssl_context=(sys.argv[1], sys.argv[2]))
