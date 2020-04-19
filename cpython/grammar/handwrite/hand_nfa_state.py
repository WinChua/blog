from collections import defaultdict
from copy import deepcopy
import hand_dot_draw

class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class NFAState:
    def __init__(self):
        self.arcs = []

    def add_arc(self, nextState, arc = None):
        self.arcs.append((nextState, arc))

    def __repr__(self):
        return f'''<NFAState {id(self)} with {[a[1] for a in self.arcs]}>'''


def searchByArc(nfa):
    # nfa: (start, end)
    arcs = []
    node = set()
    def p(start):
        if start in node:
            return
        node.add(start)
        for arc in start.arcs:
            # a = (start, end, arc_label)
            a = (start, arc[0], arc[1])
            arcs.append(a)
            p(arc[0])
    p(nfa[0])
    return arcs


def genNFAStateByEpsilon(nfaState, endState):
    node = set()
    nfas = {nfaState}
    def dealSingleNode(nfaState):
        if nfaState in node:
            return
        node.add(nfaState)
        for arc in nfaState.arcs:
            if arc[1] is None:
                nfas.add(arc[0])
                dealSingleNode(arc[0])
    dealSingleNode(nfaState)
    return nfas


class DFAState:
    def __init__(self, nfas):
        self.nfas = nfas
        self.arcs = []
        self.isfinal = False

    def add_arc(self, dfa, arc):
        self.arcs.append((dfa, arc))

    # equal could not be __eq__ for the reason that the definition of __eq__ in Class will
    # make Class.__hash__ to be None, which could not be hash
    def equal(self, other, endnfa=None):
        # ## two dfa contains the end nfa state may not equal for the reason that they may consume different arc and jump to different state.
        # ## if we would like to simply the dfas, may should add another condition:
        # ##    the arcs of self and other is equal.
        #if endnfa in self.nfas and endnfa in other.nfas:
        #    return True
        return self.nfas == other.nfas

    @classmethod
    def from_nfa(cls, nfa, endnfa):
        nfas = genNFAStateByEpsilon(nfa, endnfa)
        s = cls(nfas)
        if endnfa in nfas:
            s.isfinal = True
        return s

    def direct_dfas(self, endnfa):
        # self is the first dfa
        dfas = set()
        dfas.add(self)
        #enddfa = DFAState({endnfa})
        #enddfa.isfinal = True
        #dfas.add(enddfa)
        def direct_dfa(parent_dfa):
            arc_nfas = defaultdict(set)
            ## find the nfa state that parent_dfa could reach by consume a non-None arc
            for nfa in parent_dfa.nfas:
                for arc in nfa.arcs:
                    if arc[1] is not None:
                        ## record all the nfa states to which parent_dfa jump by consume a arc[1]
                        arc_nfas[arc[1]].add(arc[0])

            ## generate all dfa from the nfa state to which parent_dfa jump by consume a arc
            arc_dfas = {}
            for arc, nfas in arc_nfas.items():
                arc_dfa = DFAState(set())
                for nfa in nfas:
                    a_dfa = DFAState.from_nfa(nfa, endnfa)
                    arc_dfa = arc_dfa.merge(a_dfa)

                arc_dfas[arc] = arc_dfa

            ## two dfa is equal if the nfa state they containe is equal
            ## figure out the dfa which have been explore, take the old one as the next dfa state.
            for arc, dfa in arc_dfas.items():
                next_dfa = dfa
                need_explore = True
                for ed in dfas:
                    if ed.equal(dfa):
                        next_dfa = ed
                        ## if the dfa state is a new one, we should explore it later.
                        need_explore = False

                parent_dfa.add_arc(next_dfa, arc)
                dfas.add(next_dfa)
                if need_explore:
                    ## explore the next_dfa, put all the next_dfas of next_dfa into dfas
                    direct_dfa(next_dfa)

            #return arc_dfas

        direct_dfa(self)
        return dfas

    def merge(self, other):
        ## two dfa state could merge if only they transform from the same dfa state with the same label
        d = DFAState(self.nfas.union(other.nfas))
        d.isfinal = self.isfinal or other.isfinal
        return d

    def __repr__(self):
        return f"<DFAState, {len(self.nfas)} nfas isfinale[{self.isfinal}] id[{id(self)}]>"

def dfa_from_nfa(nfastart, nfaend):
    start_dfa = DFAState.from_nfa(nfastart, nfaend)
    all_dfas = start_dfa.direct_dfas(nfaend)
    return start_dfa, all_dfas

