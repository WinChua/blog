// +build cgo

package main

import (
	"fmt"
	_ "unsafe"
)

// #include "lib.h"
// #cgo CFLAGS: -I ../clib
// #cgo LDFLAGS: -L ../clib/lib -lhello
import "C"

func TryCgo() {
	fmt.Println(C.hello(C.CString("winchua"), C.int(43)))
	fmt.Println(C.GoString(C.CString("Hello")))
	fmt.Println("build +cgo")
}
