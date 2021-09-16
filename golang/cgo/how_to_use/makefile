all:
	go test -bench=. -benchmem -count 2 -gcflags -l > with_cgo.out
	CGO_ENABLED=0 go test -bench=. -benchmem -count 2 -gcflags -l > without_cgo.out
	benchstat with_cgo.out without_cgo.out
