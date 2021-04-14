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
    var n, k int
    in := bufio.NewReader(os.Stdin)
    fmt.Fscan(in, &k)
    fmt.Fscan(in, &n)
    xs := make ([]int64, n)
    ys := make ([]int64, n)
    for i := 0; i < n; i++{
        fmt.Fscan(in, &xs[i], &ys[i])
    }
    amount_of_xs := make (map[int64] int)
    xy_pairs := make (map[Pair] int)
    for i := 0; i < n; i++{
        amount_of_xs[xs[i]] += 1
        pair := Pair{xs[i], ys[i]}
        xy_pairs[pair] += 1
    }
//     fmt.Println(xy_pairs)
//     fmt.Println(amount_of_xs)


    E_x := make (map[int64] float64)
    E_sq := make (map [int64] float64)
    for key, value := range xy_pairs {
        var probability float64
        probability = float64(value) / float64(amount_of_xs[key.First])
//         fmt.Println(probability, value, amount_of_xs[key.First], key.First, key.Second)
        E_x[key.First] += float64(key.Second) * probability
        E_sq[key.First] += float64(key.Second) * float64(key.Second) * probability
    }
//     fmt.Println(E_x)
//     fmt.Println(E_sq)
    var dispersion float64
    dispersion = 0.0
    for key, _ := range E_x {
        dispersion += (float64(amount_of_xs[key]) / float64(n)) * (E_sq[key] - E_x[key] * E_x[key])
    }

    fmt.Println(fmt.Sprintf("%.12f", dispersion))

}