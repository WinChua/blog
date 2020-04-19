import sys

def gen_dot(rulename, states):
    # rulename: name of rule
    # states: [state0, arc0, state1, arc1,...,staten]
    # if epsilon then arcx will be None
    print("digraph", rulename, "{")
    for state in states:
        print("  ", end="")
        print("subgraph {")
        for s, arc, e in zip(state[0::2], state[1::2], state[2::2]):
            if arc is None:
                arc = "epsilon"
            print(f"    {s}->{e}[label={arc}]")
        print("  }")

    print("}")


def gen_dot_by_arcs(rulename, rule_text,  arcs_type, file=None):
    need_close = False
    if isinstance(file, str):
        file = open(file, "w")
        need_close = True
    if file is None:
        file = sys.stdout
    # arcs_type  : [([arcs], "type"),...]
    print("digraph", rulename, "{", file=file)
    print(' graph[label="' + rulename + ":" + rule_text + '"]', file=file)
    for arcs, t in arcs_type:
        gen_dot_by_arcs_type(rulename, arcs, t, file)
    print("}", file=file)
    if need_close:
        file.close()

def gen_dot_by_arcs_type(rulename, allArcs, t="nfa", file=None):
    print(" subgraph", rulename+"_"+t, "{", file=file)
    state_id = dict()
    final_state = set()
    for arc in allArcs:
        print("  ", end="", file=file)
        s, e, a = arc
        sid = state_id.setdefault(s, len(state_id))
        eid = state_id.setdefault(e, len(state_id))
        a = a if a else "epsilon"
        if t == "dfa" or t == "m_dfa":
            print(f'{t}_{sid}->{t}_{eid}[label="{a}"{",color=red" if e.isfinal else ""}]',file=file)
            if e.isfinal:
                final_state.add(eid)
        else:
            print(f'{t}_{sid}->{t}_{eid}[label="{a}"]', file=file)

    for e in final_state:
        print(f'  {t}_{e}[shape=doublecircle]', file=file)

    print("  }", file=file)
