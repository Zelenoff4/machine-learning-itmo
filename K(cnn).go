package main

import (
	"bufio"
	"fmt"
	"os"
)

type Matrix struct {
	matrix [][][]float64
}

type Pool struct {
	s int
	n int
	d int
	matrix Matrix
	derivatives Matrix
}

func poolForward (node Pool) Pool {
	for k := 0; k < node.d; k++{
		for i := 0; i < node.n; i++{
			for j := 0; j < node.n; j++{

			}
		}
	}
}


func main() {
	var n, d int
	in := bufio.NewReader(os.Stdin)
	fmt.Fscan(in, &n)
	fmt.Fscan(in, &d)

}
