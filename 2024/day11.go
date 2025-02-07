package main

import (
	"fmt"
	"strconv"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

const test string = "125 17"
const live string = "4189 413 82070 61 655813 7478611 0 8"

// //go:embed day10.txt
// var live string

/*
# The key here is recognizing that the stones are independent.  A given
# stone will always follow the same path.  So, we can cache the results
# without actually remembering all of the stones.
*/

type pair struct {
	one interface{}
	two interface{}
}

var cache map[pair]int64

func blink(s int64, n int) int64 {
	key := pair{s, n}
	if cache[key] > 0 {
		return cache[key]
	}
	if n == 0 {
		return 1
	}
	if s == 0 {
		cache[key] = blink(1, n-1)
		return cache[key]
	}

	ss := strconv.FormatInt(s, 10)
	if len(ss)%2 == 0 {
		a, _ := strconv.ParseInt(ss[0:len(ss)/2], 10, 0)
		b, _ := strconv.ParseInt(ss[len(ss)/2:], 10, 0)
		cache[key] = blink(a, n-1) + blink(b, n-1)
		return cache[key]
	}
	return blink(s*2024, n-1)
}

func part1(data []int, N int) int64 {
	var sum int64
	for _, i := range data {
		sum += blink(int64(i), N)
	}
	return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := tools.Parse[int](input)[0]
	cache = make(map[pair]int64)

	fmt.Println("Part 1:", part1(data, 25))
	fmt.Println("Part 2:", part1(data, 75))
}
