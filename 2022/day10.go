package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day10test.txt
var test string

//go:embed day10.txt
var live string

var w int = 40
var h int = 6

func part1(data []string) int {
    X := 1
    t := 1
    sumx := 0
	for _,row := range(data) {
        t += 1
        if t % 40 == 20 {
            if DEBUG {
                fmt.Println(t, X, t*X)
			}
            sumx += t * X
		}
        if tools.StartsWith( row, "addx") {
            X += tools.StrToInt(row[5:])
            t += 1
            if t % 40 == 20 {
                if DEBUG {
                    fmt.Println(t, X, t*X)
				}
                sumx += t * X
			}
		}
	}
    return sumx
}

func part2(data []string) string {
	screen := ""
    X := 1
	for _,row := range(data) {
        t := len(screen) % w
		if tools.AbsInt(X-t) <= 1 {
			screen += "#"
		} else {
			screen += " "
		}
        if tools.StartsWith(row, "addx") {
            t = len(screen) % w
			if tools.AbsInt(X-t) <= 1 {
				screen += "#"
			} else {
				screen += " "
			}
            X += tools.StrToInt(row[5:])
		}
	}
    result := ""
	for i := range h {
		result += screen[i*w:(i+1)*w] + "\n"
	}
    return result
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:")
	fmt.Println(part2(data))
}
