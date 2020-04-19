aa: n d t
	ft put -u yongcai -o nfa_dfas.tgz


a: all s d t

all:
	#for i in `seq 0 91`; do python hand_write_parse_Grammar.py $${i} > nfa_dfas/nfa_dfa$${i}.dot; done 
	./hand_write_parse_Grammar.py draw-dot

t:
	tar cvzf nfa_dfas.tgz nfa_dfas

s:
	sed -i "s/'/\"/g" nfa_dfas/*

d:
	for i in `ls nfa_dfas/*.dot`; do dot -Tpng $${i} -O; done

n:
	python hand_write_parse_Grammar.py draw-dot
