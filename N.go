package main

import "fmt"
import "math"
import "bufio"
import "os"
import "sort"


type KolenkaMap struct {
    Element int
    Ind int
}

type ByElement []KolenkaMap

func (a ByElement) Len() int            { return len(a) }
func (a ByElement) Less(i, j int) bool  { return a[i].Element <= a[j].Element }
func (a ByElement) Swap(i, j int)       { a[i], a[j] = a[j], a[i] }


func RoundDown(input float64, places int) (newVal float64) {
 	var round float64
 	pow := math.Pow(10, float64(places))
 	digit := pow * input
 	round = math.Floor(digit)
 	newVal = round / pow
 	return
 }


func main(){


    var n int
    in := bufio.NewReader(os.Stdin)
    fmt.Fscan(in, &n)
    xs := make ([]int, n)
    ys := make ([]int, n)
    xxs := make ([]int, n)
    yys := make ([]int, n)
    for i := 0; i < n; i++ {
        tmp1 := 0
        tmp2 := 0
        fmt.Fscan(in, &tmp1, &tmp2)
        xs[i] = tmp1
        xxs[i] = tmp1
        ys[i] = tmp2
        yys[i] = tmp2
    }
    sort.Ints(xs)
    sort.Ints(ys)
    ranks_xs := make (map[int] int)
    ranks_ys := make (map[int] int)
    for i := 0; i < n; i++ {
        ranks_xs[xs[i]] = i
        ranks_ys[ys[i]] = i
    }
    var numerator int64
    numerator = 0
    for i := 0; i < n; i++{
        numerator += (int64(ranks_xs[xxs[i]]) - int64(ranks_ys[yys[i]])) * (int64(ranks_xs[xxs[i]]) - int64(ranks_ys[yys[i]]))
    }
    numerator = 6 * numerator
    denominator := int64(n) * (int64(n) - 1) * (int64(n) + 1)
//     fmt.Println(numerator)
//     fmt.Println(denominator)
    coeff := 1.0 - float64(numerator) / float64(denominator)
    if n == 1 {
        fmt.Println(0)
    } else {
        fmt.Println(fmt.Sprintf("%.12f", coeff))
    }
//     xs := make ([]KolenkaMap, n)
//     ys := make ([]KolenkaMap, n)
//     yys := make ([]KolenkaMap, n)
//     xxs := make ([]KolenkaMap, n)
//     for i := 0; i < n; i++ {
//         fmt.Fscan(in, &xs[i].Element, &ys[i].Element)
//         xs[i].Ind = i
//         ys[i].Ind = i
//         xxs[i].Element = xs[i].Element
//         xxs[i].Ind = i
//         yys[i].Element = ys[i].Element
//         yys[i].Ind = i
//
//     }
//
//     sort.Sort(ByElement(xs))
//     sort.Sort(ByElement(ys))
//
// //     ranks_xs := make ([]int, n)
// //     ranks_ys := make ([]int, n)
//     ranks_xs := make (map[int] int)
//     ranks_ys := make (map[int] int)
//     for i := 0; i < n; i++ {
// //         ranks_xs[xs[i].Ind] = i
// //         ranks_ys[ys[i].Ind] = i
//             ranks_xs[xs[i].Element] = i
//             ranks_ys[ys[i].Element] = i
//     }
//
// //     fmt.Println(xs)
// //     fmt.Println(ys)
// //     fmt.Println(ranks_xs)
// //     fmt.Println(ranks_ys)
// //     fmt.Println(xxs)
// //     fmt.Println(yys)
//     ans := 0
//     for i := 0; i < n; i++ {
//         ans += (ranks_xs[xxs[i].Element] - ranks_ys[yys[i].Element]) * (ranks_xs[xxs[i].Element] - ranks_ys[yys[i].Element])
// //         ans += (xxs[i].Ind - yys[i].Ind) * (xxs[i].Ind - yys[i].Ind)
//     }
// //     fmt.Println(ans)
//     numerator := 6 * ans
//     denominator := n * n * n - n
// //     fmt.Println(numerator, denominator)
//     var coeff float64 = 1.0 - float64(numerator) / float64(denominator)
//
//     if n == 1 {
//         fmt.Println(0)
//     } else {
//         fmt.Println(fmt.Sprintf("%.12f", coeff))
//     }


}
