// +build !cgo

package main

import (
	"fmt"
)

func TryCgo() {
	fmt.Println("build -cgo")
}

func Add(a, b int) int32 {
	return int32(a + b)
}
