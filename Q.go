package main

import "fmt"
// import "math"
import "bufio"
import "os"
// import "sort"

type Pair struct {
    First int64
    Second int64
}

func main(){
    var n, k1, k2 int
    in := bufio.NewReader(os.Stdin)
    fmt.Fscan(in, &k1, &k2)
    fmt.Fscan(in, &n)
    xs := make ([]int64, n)
    ys := make ([]int64, n)
    for i := 0; i < n; i++{
        fmt.Fscan(in, &xs[i], &ys[i])
    }

    amount_of_xs := make (map[int64] int)
    amount_of_ys := make (map[int64] int)
    xy_pairs := make (map[Pair] int)
    for i := 0; i < n; i++{
        amount_of_xs[xs[i]] += 1
        amount_of_ys[ys[i]] += 1
        pair := Pair{xs[i], ys[i]}
        xy_pairs[pair] += 1
    }
    khi := 0.0
    var niconicodouga float64
    niconicodouga = float64(n)
    for key, value := range xy_pairs {
        var expected float64
        expected = float64(amount_of_xs[key.First]) * float64(amount_of_ys[key.Second]) / float64(n)
        niconicodouga -= expected
        khi += (float64(value) - expected) * (float64(xy_pairs[key]) - expected) / expected
    }
    fmt.Println(fmt.Sprintf("%.8f", (khi + niconicodouga)))
}