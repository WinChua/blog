a: all s t

all:
	for i in `seq 0 91`; do python hand_write_parse_Grammar.py $${i} > nfa_dfas/nfa_dfa$${i}.dot; done 

t:
	tar cvzf nfa_dfas.tgz nfa_dfas

s:
	sed -i "s/'/\"/g" nfa_dfas/*

