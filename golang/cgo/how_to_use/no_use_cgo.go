// +build !cgo

package main

import (
	"fmt"
)

func TryCgo() {
	fmt.Println("build -cgo")
}
