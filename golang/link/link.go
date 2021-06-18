package link

import (
	_ "unsafe"
)

//go:linkname hello1 hello
func hello1() {
}
