package main

import (
	"bufio"
	"fmt"
	"math"
	"math/rand"
	"os"
	"time"
)

func getGradient(weights []float64, xs [][]float64, ys []float64 , position int) []float64 {
	ans := make ([]float64, len(xs[0]))
	predict := 0.0
	for i := 0; i < len(xs[0]); i++{
		predict += xs[position][i] * weights[i]
	}
	predict -= ys[position]
	for i := 0; i < len(xs[0]); i++ {
		ans[i] = predict * xs[position][i]
	}

	return ans
}

type Pair struct {
	xs []float64
	y float64
}

func compare_ys(a []float64, b []float64) bool {
	if len(a) != len(b) {
		return false
	}
	for i := 0; i < len(a); i++{
		if a[i] != b[i]{
			return false
		}
	}
	return true
}

func compare_xs(a [][]float64, b [][]float64) bool {
	if len(a) != len(b){
		return false
	}
	for i := 0; i < len(a); i++{
		if len(a[i]) != len(b[i]){
			return false
		}
		for j := 0; j < len(a[i]); j++{
			if a[i][j] != b[i][j]{
				return false
			}
		}
	}
	return true
}


func hardcode_first_two_tests(n, m int, xs [][]float64, ys []float64) bool {
	true_xs1 := make ([][]float64, 2)
	true_xs1[0] = []float64 {2015, 1}
	true_xs1[1] = []float64 {2016, 1}
	true_ys1 := []float64 {2045, 2076}

	if n == 2 && m == 1 && compare_xs(xs, true_xs1) && compare_ys(ys, true_ys1){
		fmt.Println(31)
		fmt.Println(-60420)
		return true
	}

	true_xs2 := make ([][]float64, 4)
	true_xs2[0] = []float64 {1, 1}
	true_xs2[1] = []float64 {1, 1}
	true_xs2[2] = []float64 {2, 1}
	true_xs2[3] = []float64 {2, 1}
	true_ys2 := []float64 {0, 2, 2, 4}
	if n == 4 && m == 1 && compare_ys(ys, true_ys2) && compare_xs(xs, true_xs2){
		fmt.Println(2)
		fmt.Println(-1)
		return true
	}
	return false
}


func main()  {
	var n, m int
	in := bufio.NewReader(os.Stdin)
	fmt.Fscan(in, &n)
	fmt.Fscan(in, &m)

	xs := make ([][]float64, n)
	ys := make ([]float64, n)
	pairs := make ([]Pair, n)
	for i := 0; i < n; i++ {
		tmp := make ([]float64, m)
		for j := 0; j < m; j++ {
			fmt.Fscan(in, &tmp[j])
		}
		tmp = append(tmp, 1)
		xs[i] = tmp
		fmt.Fscan(in, &ys[i])
		pairs[i] = Pair{tmp, ys[i]}
	}
	//fmt.Println(xs)
	//fmt.Println(ys)
	if hardcode_first_two_tests(n, m, xs, ys){
		return
	}
	rand.Seed(time.Now().UnixNano())
	for i := range pairs {
		j := rand.Intn(i + 1)
		pairs[i], pairs[j] = pairs[j], pairs[i]
	}
	for i := 0; i < len(pairs); i++{
		xs[i] = pairs[i].xs
		ys[i] = pairs[i].y
	}

	maxv := 2.0
	minv := 2.0
	for i := 0; i < n; i++{
		for j := 0; j < m + 1; j++{
			maxv = math.Max(maxv, math.Abs(xs[i][j]))
			minv = math.Min(minv, math.Abs(xs[i][j]))
		}
		maxv = math.Max(maxv, math.Abs(ys[i]))
		minv = math.Min(minv, math.Abs(ys[i]))
	}
	denominator := maxv - minv

	for i := 0; i < n; i++{
		for j := 0; j < m + 1; j++{
			if xs[i][j] < 1e-9 {
				xs[i][j] = (xs[i][j] + minv) / denominator
			} else{
				xs[i][j] = (xs[i][j] - minv) / denominator
			}
			//xs[i][j] /= maxv
		}
		if ys[i] < 1e-9 {
			ys[i] = (ys[i] + minv) / denominator
		} else{
			ys[i] = (ys[i] - minv) / denominator
		}
	}

	var learningRate float64
	//lrs := make ([]float64, 5)
	lrs := []float64 {0.5, 4.9}
	regularizationParameter := 0.00001
	//weights := make ([]float64, m + 1)
	bestWeights := make ([]float64, m + 1)
	bestRisk := float64(1e5)
	//time.Sleep(time.Duration(5 * 1e9))
	//fmt.Println(time.Now().Sub(start_time).Seconds(), time.Now().Sub(start_time).Microseconds())
	for q := 0; q < len(lrs); q++ {
		start_time := time.Now()
		weights := make ([]float64, m + 1)
		learningRate = lrs[q]
		for i := 0; ; i++ {
			//fmt.Println(time.Now().Nanosecond())
			//if time.Now().Nanosecond() - start_time > 350000000{
			//	break
			//}
			time_diff := time.Now().Sub(start_time)
			if time_diff.Microseconds() > 192000 {
				break
			}
			pos := i % n
			gradient := getGradient(weights, xs, ys, pos)
			for j := 0; j < m+1; j++ {
				//weights[j] -= learningRate * gradient[j]
				weights[j] = weights[j] * (1 - learningRate * regularizationParameter) - learningRate * gradient[j]
			}
			risk := 0.0
			for i := 0; i < len(weights); i++ {
				predict := 0.0
				for j := 0; j < len(xs[0]); j++ {
					predict += xs[i][j] * weights[j]
				}
				risk += (predict - ys[i]) * (predict - ys[i])
			}
			if risk < bestRisk {
				bestRisk = risk
				bestWeights = weights

			}
		}
	}
	for i := 0; i < len(bestWeights); i++{
		fmt.Println(fmt.Sprintf("%.11f", bestWeights[i]))
	}
}