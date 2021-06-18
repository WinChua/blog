package test

import (
	"bytes"
	"sync"
	"testing"
)

var bufPool = sync.Pool{
	New: func() interface{} {
		return new(bytes.Buffer)
	},
}

func BenchmarkPoolGet(b *testing.B) {
	for i := 0; i < b.N; i++ {
		buf := bufPool.Get().(*bytes.Buffer)
		buf.Reset()
		buf.Write([]byte("hello"))
		bufPool.Put(buf)
	}
}

func BenchmarkByteGet(b *testing.B) {
	for i := 0; i < b.N; i++ {
		buf := new(bytes.Buffer)
		buf.Write([]byte("hello"))
	}
}

func BenchmarkPoolGetEmpty(b *testing.B) {
	for i := 0; i < b.N; i++ {
		buf := bufPool.Get().(*bytes.Buffer)
		bufPool.Put(buf)
	}
}
