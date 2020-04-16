import hand_nfa_state
import tokenize
from hand_grammar_ast import *
import callback
from hand_dot_draw import gen_dot
import hand_dot_draw

gram_file = "Grammar"

tokens = tokenize.generate_tokens(open(gram_file).readline)

cur_token = next(tokens)
while cur_token.type in (tokenize.COMMENT, tokenize.NL):
    cur_token = next(tokens)

def getNextToken(tokens):
    t = next(tokens)
    while t.type == tokenize.NL:
        t = next(tokens)

    return t

def parse_grammar(cur_token, tokens):
    rules = []
    if cur_token.type in (tokenize.NL, tokenize.COMMENT):
        rs, cur_token = parse_grammar(getNextToken(tokens), tokens)
        rules.extend(rs)
    elif cur_token.type == tokenize.NAME:
        rule, cur_token = parse_rule(cur_token, tokens)
        rules.append(rule)
    if cur_token.type == tokenize.ENDMARKER:
        return rules, cur_token
    else:
        rs, cur_token = parse_grammar(cur_token, tokens)
        rules.extend(rs)
        return rules, cur_token


def parse_rule(cur_token, tokens):
    if cur_token.type != tokenize.NAME:
        raise Exception("the token input into parse_rule is wrong for whose type is not tokenize.NAME")
    name = cur_token.string
    cur_token = getNextToken(tokens)
    if cur_token.type != tokenize.OP and cur_token.string != ":":
        raise Exception("the token after the tokenize.NAME must be ':'.",cur_token)

    
    rhs, cur_token = parse_rhs(getNextToken(tokens), tokens)
    if cur_token.type != tokenize.NEWLINE:
        raise Exception("NEWLINE must after rhs", cur_token)
    
    return Rule(name, rhs), getNextToken(tokens)


def parse_rhs(cur_token, tokens):
    itemss = []
    items, cur_token = parse_items(cur_token, tokens)
    itemss.append(items)
    while cur_token.type == tokenize.OP and cur_token.string == "|":
        items, cur_token = parse_items(getNextToken(tokens), tokens)
        itemss.append(items)

    itemss = callback.p_rhs(cur_token, itemss)
    return itemss, cur_token


def parse_items(cur_token, tokens):
    items = []
    item, cur_token = parse_item(cur_token, tokens)
    items.append(item)
    while (cur_token.type == tokenize.OP and cur_token.string in ('[', '(')) or (cur_token.type in (tokenize.NAME, tokenize.STRING)):
        item, cur_token = parse_item(cur_token, tokens)
        items.append(item)

    items = callback.p_items(cur_token, items)
    return items, cur_token


def parse_item(cur_token, tokens):
    token = cur_token
    if cur_token.type == tokenize.OP and cur_token.string == "[":
        rhs, cur_token = parse_rhs(getNextToken(tokens), tokens)
        if cur_token.type != tokenize.OP and cur_token.string != "]":
            raise Exception("rhs in item should end with ']'", cur_token)
        cur_token = getNextToken(tokens)
        #item = Item(Item.RHS, rhs)
        item = callback.p_item(token, rhs)
    else:
        atom, cur_token = parse_atom(cur_token, tokens)
        if cur_token.type == tokenize.OP and cur_token.string in ('+', '*'):
            atom.modifier = cur_token.string
            atom.extra["modifier"]= cur_token.string
            cur_token = getNextToken(tokens)

        item = callback.p_item(token, atom)
        #item = Item(Item.ATOM, atom)
    return item, cur_token


def parse_atom(cur_token, tokens):
    if cur_token.type == tokenize.OP and cur_token.string == '(':
        rhs, cur_token = parse_rhs(getNextToken(tokens), tokens)
        if cur_token.type == tokenize.OP and cur_token.string != ')':
            raise Exception("the token after rhs in atom should be ')'")
        atom = callback.p_atom(cur_token, rhs)
        #atom = Atom(Atom.RHS, rhs)
        return atom, getNextToken(tokens)
    elif cur_token.type == tokenize.NAME:
        atom = callback.p_atom(cur_token)
        #atom = Atom(Atom.NAME, cur_token.string)
        return atom, getNextToken(tokens)
    elif cur_token.type  == tokenize.STRING:
        atom = callback.p_atom(cur_token)
        #atom = Atom(Atom.STRING, cur_token.string)
        return atom, getNextToken(tokens)

    raise Exception("parse atom error", cur_token)
    

def genAllDfas(cur_token, tokens):
    rules, cur_token = parse_grammar(cur_token, tokens)
    rule_dfas = []
    for r in rules:
        rule_text = r.dumpRule()
        nfa = r.genNFA()
        dfa = hand_nfa_state.dfa_from_nfa(nfa[0], nfa[1])
        rule_dfas.append((r.name, (rule_text, nfa, dfa)))
        #rule_dfas[r.name] = [nfa, dfa]

    return rule_dfas

import click

@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    pass

@cli.command()
def draw_dot():
    rule_dfas = genAllDfas(cur_token, tokens)
    for i, (rule_name, (rule_text, nfa, dfa)) in enumerate(rule_dfas):
        dfaArcs = hand_nfa_state.searchByArc((dfa, ))
        nfaArcs = hand_nfa_state.searchByArc(nfa)
        hand_dot_draw.gen_dot_by_arcs(rule_name, rule_text,[(nfaArcs, "nfa"),(dfaArcs, "dfa")], f'nfa_dfas/{i}.{rule_name}.dot')

@cli.command()
def regen_rule():
    rules, _ = parse_grammar(cur_token, tokens)
    for r in rules:
        print(r.name + ":", r.dumpRule())

@cli.command()
@click.option("--no", default=0, type=click.INT, help="no. i rule to generate dot.")
def draw_no(no):
    rule_dfas = genAllDfas(cur_token, tokens)
    rule_name, (rule_text, nfa, dfa) = rule_dfas[no]
    nfaArcs = hand_nfa_state.searchByArc(nfa)
    dfaArcs = hand_nfa_state.searchByArc((dfa, ))
    hand_dot_draw.gen_dot_by_arcs(rule_name, rule_text, [(nfaArcs, "nfa"), (dfaArcs, "dfa")])



if __name__ == "__main__":
    cli()
