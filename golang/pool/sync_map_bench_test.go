package test

import (
	"sync"
	"testing"
)

func BenchmarkSyncMap(b *testing.B) {
	m := new(sync.Map)
}
