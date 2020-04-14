import hand_nfa_state as nfa


class gAST:
    def __init__(self, type, value, **kwargs):
        self.type = type
        self.value = value
        self.extra = kwargs
        self.tabsize = 0
    def dump(self, tabsize):
        self.tabsize = tabsize
        s = repr(self).split("\n")
        s = [tabsize * " " + line for line in s]
        return "\n".join(s) + "\n"

    def dumpType(self):
        return repr(self.type)

    def dumpValue(self):
        return repr(self.value)

    def genNFA(self):
        raise NotImplemented

    def __repr__(self):
        return f"""<{self.__class__.__name__}:{self.dumpType()}:{self.value}:{','.join(k+"="+v for k, v in self.extra.items() if v)}>"""
#    def __repr__(self):
#        return f'''<{self.__class__.__name__}
#        type: {self.dumpType()}
#        value: {self.value}
#>'''
#    def __repr__(self):
#        #if isinstance(self.value, list):
#        #    vStr = ""
#        #    for v in self.value:
#        #        if isinstance(v, list):
#        #            vStr += "\n".join([vv.dump(self.tabsize+2) for vv in v]) + "\n"
#        #        else:
#        #            vStr += v.dump(self.tabsize+1) + "\n"
#        #else:
#        #    vStr = self.value.dump(self.tabsize+1)
#        return f'''<{self.__class__.__name__} 
#    type: [{self.dumpType()}]
#    value: [{chr(10)+self.dumpValue()}]
#'''    

class String(gAST):
    def __init__(self, string):
        super().__init__(0, string)

class Atom(gAST):
    RHS, NAME, STRING = list(range(3))
    def __init__(self, type, value, modifier=None):
        super().__init__(type, value, modifier=modifier)
        self.modifier = modifier

    def dumpType(self):
        return {Atom.RHS:"RHS", Atom.NAME:"NAME", Atom.STRING:"STRING"}[self.type]
    def dumpValue(self):
        if isinstance(self.value, str):
            return self.value
        elif isinstance(self.value, list):
            return "\n".join(["\n".join([v.dump(self.tabsize+1) for v in vv]) for vv in self.value])
        else:
            return self.value.dump(self.tabsize+1)

    def genNFA(self):
        if self.type in (Atom.NAME, Atom.STRING):
            start, end = nfa.NFAState(), nfa.NFAState()
            start.add_arc(end, self.value)
        else:
            #start, end = self.value.genNFA()
            start, end = Rule.genNFA(self)
        
        if self.modifier is None:
            return start, end
        elif self.modifier == "*":
            end.add_arc(start)
            return start, start
        elif self.modifier == "+":
            end.add_arc(start)
            return start, end
        else:
            raise Exception("nfa gen for atom err")

#    def __repr__(self):
#        return f'''<Atom type:[{self.type}] 
#    value[{self.value}] 
#    modifier[{self.modifier}]>'''


class Item(gAST):
    RHS, ATOM = list(range(2))
    def __init__(self, type, value):
        super().__init__(type, value)

    def dumpType(self):
        return {Item.RHS:"RHS", Item.ATOM:"ATOM"}[self.type]

    def dumpValue(self):
        return self.value.dump(self.tabsize+1)

    def genNFA(self):
        if self.type == Item.RHS:
            ##start, end = self.value.genNFA()
            start, end = Rule.genNFA(self)
            start.add_arc(end)
            return  start, end
        elif self.type == Item.ATOM:
            start, end = self.value.genNFA()
            return start, end
#    def __repr__(self):
#        return f"<Item type:[{self.type}] value[{self.value}]>"

class Rule:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def genNFA(self):
        ss, ee = nfa.NFAState(), nfa.NFAState()
        for items in self.value:
            start, end = None, None
            for item in items:
                s, e = item.genNFA()
                if start is None:
                    start = s
                else:
                    end.add_arc(s)
                end = e
            ss.add_arc(start)
            end.add_arc(ee)
        #nfa.search_nfaState([ss,ee], nfa.dealState, nfa.dealArc)
        return ss, ee
#    def __repr__(self):
#        return f"<Rule name:[{self.name}] value[{self.value}]>"
#

def rule2nfa(rule):
    return rule.genNFA()
