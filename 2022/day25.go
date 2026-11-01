package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122`[1:]

//go:embed day25.txt
var live string

var codes = map[byte]int{
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}

var uncode = "012=-"

func encode(n int) string {
    s := ""
    for n > 0 {
        r := n % 5
        n = n / 5
		if r >= 3 {
			n++
		}
        s = string(uncode[r]) + s
	}
    return s
}

func part1(data []string) string {
    sumx := 0
	for _,line := range data {
        num := 0
		for i := range len(line) {
            num = num * 5 + codes[line[i]]
		}
        sumx += num
	}

    if DEBUG {
        print(sumx)
	}
    return encode(sumx)
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	fmt.Println("Part 1:", part1(data))
}


