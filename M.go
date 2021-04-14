package main

import "fmt"
import "math"
import "bufio"
import "os"
import "sort"

func RoundDown(input float64, places int) (newVal float64) {
 	var round float64
 	pow := math.Pow(10, float64(places))
 	digit := pow * input
 	round = math.Floor(digit)
 	newVal = round / pow
 	return
 }


func main(){


    type KolenkaMap struct {
        Element int
        Ind int
    }

    type ByElement stru

    var n int
    in := bufio.NewReader(os.Stdin)
    fmt.Fscan(in, &n)
    xs := make ([]int, n)
    ys := make ([]int, n)
    for i := 0; i < n; i++ {
        fmt.Fscan(in, &xs[i], &ys[i])
    }

    sort.Ints(xs)
    sort.Ints(ys)


}