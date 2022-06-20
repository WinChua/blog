package main

import (
	"fmt"
	"unsafe"
)

type s struct {
	a int
	b string
}

func main() {
	ss := s{a: 5, b: "string"}
	p := unsafe.Pointer(uintptr(unsafe.Pointer(&ss)) + unsafe.Offsetof(ss.b)) // 这个语句对于gc来说是原子的
	*(*string)(p) = "Hello"
	fmt.Println(ss)

	// tmp := uintptr(unsafe.Pointer(&ss)) + unsafe.Offsetof(ss.b)
	// pb := (*string)(unsafe.Pointer(tmp))
	// *pb = "Hello" // 这个对于gc来说不是原子的, golang的gc是移动gc, 在gc过程中为了防止内存碎片化, 可能会一定一些内存
	// 在内存移动之后, 对应指向这些内存的指针需要被移动, 由于 tmp 是一个value, 假如某次gc过程中, ss被移动了, 而由于tmp
	// 是值, 不会被gc修改, 那么在后面计算p的时候, 可能指向了一个悬空的地址了

	// 另外unsafe.Pointer(不能进行算数运算, 需要通过转化成uintptr进行指针运算
}

type a unsafe.Pointer
