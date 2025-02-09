package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test string = `
1
10
100
2024`[1:]

var test2 []int = []int{1, 2, 3, 2024}

//go:embed day22.txt
var live string

/*
# Sequence: x64, mix, prune?
# /32, mix, prune
# *2024, mix, prune
#
# Mix = bitwise xor
# Prune = mod 16777216
*/

func gen(secret int) int {
	secret = (secret ^ (secret << 6)) & 0xFFFFFF
	secret = (secret ^ (secret >> 5)) & 0xFFFFFF
	secret = (secret ^ (secret << 11)) & 0xFFFFFF
	return secret
}

func part1(data []int) int {
	sum := 0
	for _, secret := range data {
		for i := 0; i < 2000; i++ {
			secret = gen(secret)
		}
		sum += secret
	}
	return sum
}

// Generate the part2 prices and deltas from a given secret.

func sequence(data []int, secret int) ([]int, []int) {
	prices := []int{secret % 10}
	deltas := []int{0}
	for i := 0; i < 2000; i++ {
		news := gen(secret)
		prices = append(prices, news%10)
		deltas = append(deltas, news%10-secret%10)
		secret = news
	}
	return prices, deltas
}

type Quad struct {
	a, b, c, d int
}

func makequad(a []int) Quad {
	return Quad{a[0], a[1], a[2], a[3]}
}

// Generate all of the 4-tuples from the deltas and the price at the end.

func part2(data []int) int {
	fours := make(map[Quad]int)
	for _, secret := range data {
		prices, deltas := sequence(data, secret)
		seen := make(map[Quad]bool)
		for i := 0; i < len(prices)-4; i++ {
			key := makequad(deltas[i : i+4])
			if !seen[key] {
				fours[key] += prices[i+3]
				seen[key] = true
			}
		}
	}
	maxx := 0
	for _, v := range fours {
		maxx = max(maxx, v)
	}
	return maxx
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	var data []int
	for _, line := range strings.Split(input, "\n") {
		data = append(data, tools.StrToInt(line))
	}

	fmt.Println("Part 1:", part1(data))
	if TEST {
		data = test2
	}
	fmt.Println("Part 2:", part2(data))
}
