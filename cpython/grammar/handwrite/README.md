## visualization of python's grammar

recently, the beautiful of python's grammar drive me dived into it.
While, when i was learning the parsing of the grammar, i found that
it's hard to understand the parsing of the Grammar file. So, I pick
some snippet of code in pgen, and visualize every production rule in
the Grammar file.

Take this production rule as an example:

```
exprlist: (expr|star_expr) (',' (expr|star_expr))* [',']
```

it generate the picture like this.

[exprlist](https://github.com/WinChua/blog/blob/master/cpython/grammar/handwrite/nfa_dfas/nfa_dfa75.dot.png)

the red edge specify that whose end node is the final state of the dfa.
