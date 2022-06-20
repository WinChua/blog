package main

import (
	"fmt"
)

type A struct {
	A int
}

func main() {
	f()
}

func f() *A{
	a := &A{A:42}
	fmt.Println(a) // 指针作为调用参数
	return a // 局部变量作为指针返回了, escape
}

// go build -gcflags='-m -l' main.go // -m 打印出逃逸分析情况; -l 阻止内联
