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
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576`[1:]

//go:embed day09.txt
var live string

var preamble = 25


func part1(data []int) int {
	for i := preamble; i < len(data); i++ {
        found := false
		for j := i-preamble; j < i; j++ {
			for k := j+1; k < i; k++ {
                if DEBUG {
                    fmt.Println(i,j,k,data[i],data[j],data[i])
				}
                if data[i] == data[j] + data[k] {
                    found = true
					break
				}
			}
		}
        if ! found {
            return data[i]
		}
	}
    return -1
}


func part2(data []int, key int) int {
    // Start here.
    for i := range len(data) {
        // End here.
		for j := i; j < len(data); j++ {
			sub := data[i:j]
            trial := tools.Sum(sub)
            if trial == key {
                return tools.Min(sub)+tools.Max(sub)
			}
            if trial > key {
                break
			}
		}
	}
    return 0
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := []int{}
	for _,line := range strings.Split(strings.TrimSpace(input), "\n") {
		data = append(data, tools.StrToInt(line))
	}

    if TEST {
		preamble = 5
	}

	key := part1(data)
	fmt.Println("Part 1:", key)
	fmt.Println("Part 2:", part2(data,key))
}
