## the show is wrong for show the whole path of a nfa, for the reason that a nfa may have loop
def show(nfas):
    print("rule:", nfas.start.rule_name)
    stateId = set()
    def showNFAState(spacesize, state):
        if id(state) in stateId:
            print("|" * spacesize, id(state), "have printed.")
        else:
            stateId.add(id(state))
            for arc in state.arcs:
                print("|" * spacesize + repr(id(state)) + " --"+ str(arc.label) +  "--> " + repr(id(arc.target)))
                showNFAState(spacesize+1, arc.target)
    showNFAState(1, nfas.start)
