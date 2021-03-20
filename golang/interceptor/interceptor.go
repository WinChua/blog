package main

import ()

type Handler func()
type Interceptor func(h Handler) Handler

type Accelerator []Interceptor

func (a *Accelerator) Register(i Interceptor) {
	*a = append(*a, i)
}

// reduce(a, reducer, h) => result_func
func (a Accelerator) Wrap(h Handler) Handler {
	for idx := range a {
		h = reducer(h, a[len(a)-idx-1])
	}
	return h
}

func reducer(h Handler, i Interceptor) Handler {
	return i(h)
}

func (a Accelerator) AnotherWrap(h Handler) Handler {
	var cur = -1
	var nextHandler Handler
	nextHandler = func() {
		if cur == len(a)-1 {
			h()
			return
		}
		cur++
		a[cur](nextHandler)()
	}
	return nextHandler
}
