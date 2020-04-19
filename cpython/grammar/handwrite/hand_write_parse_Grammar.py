#! /usr/bin/env python

import hand_nfa_state
from collections import defaultdict
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
        start_dfa, all_dfa = hand_nfa_state.dfa_from_nfa(nfa[0], nfa[1])
        minimize_dfaset = minimize_dfa(all_dfa)

        arcs = build_arc(minimize_dfaset, start_dfa)
        rule_dfas.append((r.name, (rule_text, nfa, start_dfa, arcs)))

    return rule_dfas

import click

@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    pass


@cli.command()
def draw_dot():
    rule_dfas = genAllDfas(cur_token, tokens)
    for i, (rule_name, (rule_text, nfa, dfa, marcs)) in enumerate(rule_dfas):
        dfaArcs = hand_nfa_state.searchByArc((dfa, ))
        nfaArcs = hand_nfa_state.searchByArc(nfa)
        hand_dot_draw.gen_dot_by_arcs(rule_name, rule_text,[(nfaArcs, "nfa"),(dfaArcs, "dfa"), (marcs, "m_dfa")], f'nfa_dfas/{i}.{rule_name}.dot')


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

from pprint import pprint

@cli.command()
@click.option("--no", type=click.INT, default=30, help="no rule to show")
def explore(no):
    rules, _ = parse_grammar(cur_token, tokens)
    r = rules[no]
    rule_text = r.dumpRule()
    nfa = r.genNFA()
    start_dfa, all_dfa = hand_nfa_state.dfa_from_nfa(nfa[0], nfa[1])
    #print("no is", no, "len(all_dfa) is", len(all_dfa))
    minimize_dfaset = minimize_dfa(all_dfa)

    arcs = build_arc(minimize_dfaset, start_dfa)
    hand_dot_draw.gen_dot_by_arcs("abc", "abc", [(arcs, "dfa")])
    #for d in minimize_dfa(all_dfa):
    #    for dd in d:
    #        print(",", end="")
    #        pprint(dd)

def build_arc(minimize_dfaset, start_dfa):
    start_dfa_set = None
    for d in minimize_dfaset:
        if start_dfa in d:
            start_dfa_set = d

    for d_i in minimize_dfaset:
        #for j in range(0, len(minimize_dfaset)):
        #    d_j = minimize_dfaset[j]
        for d_j in minimize_dfaset:
            for dfastate in d_i:
                for targetstate, arc in dfastate.arcs:
                    if targetstate in d_j:
                        d_i.add_arc(arc, d_j)
    arcs = hand_nfa_state.searchByArc((start_dfa_set,))
    return arcs

class DFASet:
    __hash__ = object.__hash__
    def __init__(self, dfa_set):
        # dfa_set: {DFAState, DFAState}
        self.dfa_set = dfa_set
        self.isfinal = False
        for i in dfa_set:
            if i.isfinal:
                self.isfinal = True
        
        self.arcs = []

    def add_arc(self, arc, target):
        for t, a in self.arcs:
            if arc == a:
                assert(target is t)
                return 
        self.arcs.append((target, arc))

    def __repr__(self):
        arcs = ":".join([",".join([a for _, a in s.arcs]) for s in self.dfa_set])
        return f'''<DSet {len(self.dfa_set)},f[{self.isfinal}],dfaid:[{','.join([str(id(s)) for s in self.dfa_set])}], [{arcs}]>'''
    def __iter__(self):
        return iter(self.dfa_set)

    def __contains__(self, dfa):
        return dfa in self.dfa_set

    def __eq__(self, other):
        return other.dfa_set == self.dfa_set

    def equal_with_last(self, state_i, state_j, last_merge):
        # use to judge the two DFAState is jump equal in the last_merge
        if len(state_i.arcs) != len(state_j.arcs):
            return False
        d_arc_state_i = {arc: t_state for t_state, arc in state_i.arcs}
        d_arc_state_j = {arc: t_state for t_state, arc in state_j.arcs}
        arc_states = defaultdict(list)
        for arc, t_state_i in d_arc_state_i.items():
            t_state_j = d_arc_state_j.get(arc, None)
            if t_state_j is None:
                return False
            arc_states[arc].append(t_state_i)
            arc_states[arc].append(t_state_j)

        for arc, t_state_list in arc_states.items():
            for dfa_set in last_merge:
                all_state_in_dfa_set = [state in dfa_set for state in t_state_list]
                if all(all_state_in_dfa_set):
                    continue
                if any(all_state_in_dfa_set) == False:
                    continue
                return False

        return True
    def split(self, last_merge):
        # self DFASet, return list of DFASet
        # last_merge: list of DFASet
        list_of_dfa = list(self.dfa_set)
        same_state = {}
        if_j_dealed = set()
        for i, state_i in enumerate(list_of_dfa):
            if i in if_j_dealed:
                continue
            if_j_dealed.add(i)
            same_state[i] = [state_i]
            for j in range(i+1, len(list_of_dfa)):
                state_j = list_of_dfa[j]
                if self.equal_with_last(state_i, state_j, last_merge):
                    same_state[i].append(state_j)
                    if_j_dealed.add(j)

        next_merge = []
        for v in same_state.values():
            next_merge.append(DFASet(set(v)))

        return next_merge, len(next_merge) > 1


def minimize_dfa(all_dfa):
    end_set, non_end_set = set(), set()
    for dfa_state in all_dfa:
        if dfa_state.isfinal:
            end_set.add(dfa_state)
        else:   
            non_end_set.add(dfa_state)

    last_merge = [DFASet(end_set), DFASet(non_end_set)]
    next_merge = []
    change = True
    i = 0
    while change:
        #print("loop", i)
        all_dfa_set_change = []
        for dfaset in last_merge:
            l, set_change = dfaset.split(last_merge)
            all_dfa_set_change.append(set_change)
            next_merge.extend(l)

        # if there is no change during all the split of dfaset, we need to break the loop
        if not any(all_dfa_set_change):
            change = False
        else:
            last_merge, next_merge = next_merge, []

        #for m in last_merge:
        #    print(m)
        #print(len(last_merge))
        i = i + 1

    return last_merge
    #return last_merge[0].split(), last_merge[1].split()
    
def change_equal(next_merge, last_merge, i):
    #print(sorted(next_merge))
    #print(set(next_merge) == set(last_merge))
    return i > 3

if __name__ == "__main__":
    cli()
