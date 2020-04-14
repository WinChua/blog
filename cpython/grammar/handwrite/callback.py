import tokenize
import hand_grammar_ast

def p_atom(token, lastNode = None):
    if lastNode is None:
        ATOM_TYPE = hand_grammar_ast.Atom.STRING if token.type == tokenize.STRING else hand_grammar_ast.Atom.NAME
        return hand_grammar_ast.Atom(ATOM_TYPE, token.string)
    else:
        return hand_grammar_ast.Atom(hand_grammar_ast.Atom.RHS, lastNode)

def p_item(token, lastNode = None):
    if token.type == tokenize.OP and token.string == "[":
        return hand_grammar_ast.Item(hand_grammar_ast.Item.RHS, lastNode)
    else:
        return hand_grammar_ast.Item(hand_grammar_ast.Item.ATOM, lastNode)


def p_items(token, lastNode = None):
    return lastNode

def p_rhs(token, lastNode = None):
    return lastNode
