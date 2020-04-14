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


def gen_dot_by_arcs(rulename, arcs_type):
    # arcs_type  : [([arcs], "type"),...]
    print("digraph", rulename, "{")
    for arcs, t in arcs_type:
        gen_dot_by_arcs_type(rulename, arcs, t)
    print("}")

def gen_dot_by_arcs_type(rulename, allArcs, t="nfa"):
    print(" subgraph", rulename+"_"+t, "{")
    state_id = dict()
    for arc in allArcs:
        print("  ", end="")
        s, e, a = arc
        sid = state_id.setdefault(s, len(state_id))
        eid = state_id.setdefault(e, len(state_id))
        a = a if a else "epsilon"
        if t == "dfa":
            print(f'{t}_{sid}->{t}_{eid}[label={a}{",color=red" if e.isfinal else ""}]')
        else:
            print(f'{t}_{sid}->{t}_{eid}[label={a}]')


    print("  }")

