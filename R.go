package main

import "fmt"
import "math"
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
    entropy := 0.0
    for key, value := range xy_pairs {
        var prob float64
        prob = float64(value) / float64(amount_of_xs[key.First])
        entropy += prob * math.Log(1.0 / prob) * float64(amount_of_xs[key.First]) / float64(n)
    }
    fmt.Println(fmt.Sprintf("%.8f", entropy))
}