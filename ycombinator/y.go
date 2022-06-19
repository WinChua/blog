package main

import (
	"fmt"
)

type Func[T, U any] func(T)U

type TagFunc[T, U any] func(Func[T, U]) Func[T, U]

type C[T, U any] func(C[T, U]) Func[T, U]

func Y[T, U any](f TagFunc[T, U]) Func[T, U] {
	return func(self C[T, U]) Func[T, U] {
		return func(t T) U {
			return f(self(self))(t)
		}
	}(
		func(self C[T, U]) Func[T, U] {
			return func(t T) U {
				return f(self(self))(t)
			}
		},
	)
}

func main() {
	fmt.Println(Y(
		func(f Func[int, int]) Func[int, int] {
			return func(n int) int {
				switch n {
				case 0:
					return 1
				default:
					return n * f(n-1)
				}
			}
		},
	)(6))
	fmt.Println(Y(
		func(f Func[[]int, int]) Func[[]int, int] {
			return func(ns []int) int {
				switch len(ns) {
				case 0:
					return 1
				case 1:
					return ns[0]
				default:
					return f(ns[1:]) * ns[0]
				}
			}
		},
	)([]int{1,2,3,4,5,6}))
}
