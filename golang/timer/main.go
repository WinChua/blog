package main

import (
	"fmt"
	"time"
)

func main() {
	<-time.After(time.Second)
	fmt.Println("hello")
}
