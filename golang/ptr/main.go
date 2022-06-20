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

	// unsafe.Pointer, uintptr 的4种操作:
	// * unsafe.Pointer => pointer of any type
	// * pointer of any type => unsafe.Pointer
	// * uintptr => unsafe.Pointer
	// * unsafe.Pointer => uintptr

	/* 以下几种使用模式是可以的:
	 * Convert *T1 => *T2
	 1. func Float64ToInt64(f float64) int64 {
		 return *(*int64)(unsafe.Pointer(&f))
	 }
	 // 只要目标类型的内存大小小于源类型就行
	 2. unsafe.Pointer => uintptr , 但不能把uintptr转回unsafe.Pointer
	 3. unsafe.Pointer => uintptr, 然后进行指针运算马上转回unsafe.Pointer, 必须在同一个expression中, 防止移动gc
	 4. unsafe.Pointer => uintptr, 作为syscall.Syscall的参数, 这些实现的内部会将uintptr转会pointer, unsafe.Pointer 
	    到uintptr的转化只能放在函数参数中
	 */
}

type a unsafe.Pointer
