package main

import "fmt"
// import "math"
import "bufio"
import "os"
import "sort"


func Dist(array []int) int64 {
    sort.Ints(array)
    var summ int64
    var ans int64
    summ = 0
    ans = 0
    for i := 1; i < len(array) + 1; i++{
        summ += int64(array[i - 1])
        ans += int64(array[i - 1]) * int64(i) - summ
    }
    return 2 * ans
}


func main(){
    var n, k int
    in := bufio.NewReader(os.Stdin)
    fmt.Fscan(in, &k)
    fmt.Fscan(in, &n)
    xs := make ([]int, n)
    ys := make ([]int, n)
    for i := 0; i < n; i++{
        fmt.Fscan(in, &xs[i], &ys[i])
    }
    clusters := make (map[int] []int)

    for i := 0; i < n; i++{
        clusters[ys[i]] = append(clusters[ys[i]], xs[i])
    }
//     fmt.Println(clusters)

    var inner_summ int64
    inner_summ = 0
    for _, value := range clusters {
        inner_summ += Dist(value)
    }
    fmt.Println(inner_summ)
    all_dist := Dist(xs)
    outer_summ := all_dist - inner_summ
    fmt.Println(outer_summ)

}