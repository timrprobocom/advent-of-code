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
1721
979
366
299
675
1456`[1:]

//go:embed day01.txt
var live string


func part1(data []int) int {
    for i := range len(data)  {
		for j := i+1; j < len(data); j++ {
            if data[i]+data[j] == 2020 {
                return data[i]*data[j]
			}
		}
	}
	return 0
}

func part2(data []int) int {
    for i := range len(data) {
		for j := i+1; j < len(data); j++ {
			for k := j+1; k < len(data); k++ {
                if data[i]+data[j]+data[k] == 2020 {
                    return data[i]*data[j]*data[k]
				}
			}
		}
	}
	return 0
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := []int{}
	for _,row := range strings.Fields(input) {
		data = append(data, tools.StrToInt(row))
	}

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
