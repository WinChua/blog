import pdb
import tokenize
import sys
from io import StringIO
sys.path.insert(0, "/home/winchua/cpython")
GRAMMAR_FILE = "/home/winchua/cpython/Grammar/Grammar"


from Parser.pgen.metaparser import GrammarParser


def makeGrammar():
    with open(GRAMMAR_FILE) as f:
        grammarFile = StringIO(f.read())

    t = tokenize.generate_tokens(grammarFile.readline)
    return t

def getNextTup(t):
    tup = next(t)
    while tup.type in (tokenize.COMMENT, tokenize.NL):
        tup = next(t)
    return tup

def getAllTup():
    g = makeGrammar()
    tups = []
    tup = getNextTup(g)
    while tup.type != tokenize.ENDMARKER:
        while tup.type in (tokenize.COMMENT, tokenize.NL):
            tup = getNextTup(g)

        tups.append(tup)
        tup = getNextTup(g)

    return tups

tups = getAllTup()

def getAllNFA(filename):
    data = open(filename).read()
    parser = GrammarParser(data)
    nfa = parser.parse()
    return list(nfa)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        filename = GRAMMAR_FILE
    else:
        filename = sys.argv[1]

    #pdb.set_trace()
    nfas = getAllNFA(filename)
    print(nfas)
