package main

import (
	"fmt"
	_ "unsafe"
)

// 几点注意:
// #cgo CFLAGS: -I ${SRCDIR}/hello
// SRCDIR 在编译的时候会替换成为包含源文件的目录

// cgo在本机系统编译的时候是默认打开的, 在交叉编译的时候是默认关闭的,
// 可以使用 // +build !cgo 支持cgo的条件编译

// CGO_ENABLED=0 go build

import "C"

func main() {
	TryCgo()
	fmt.Printf("%T\n", C.malloc(C.ulong(12)))
}
