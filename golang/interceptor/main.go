package main

import (
	"fmt"
)

func handler() {
	fmt.Println("handler")
}

func i2(h Handler) Handler {
	return func() {
		fmt.Println("i2 before")
		h()
		fmt.Println("i2 after")
	}
}
func i1(h Handler) Handler {
	return func() {
		fmt.Println("i1 before")
		h()
		fmt.Println("i1 after")
	}
}
func main() {
	a := &Accelerator{}
	a.Register(i1)
	a.Register(i2)
	a.Wrap(handler)()
	a.AnotherWrap(handler)()
}
