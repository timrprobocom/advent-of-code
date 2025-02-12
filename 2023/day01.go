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
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet`[1:]

var test2 = `
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen`[1:]

//go:embed day01.txt
var live string

var nums = [...]string{
    "***",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
}

func part1(data []string) int {
	sum := 0
	for _, line := range data {
		d1, d2 := -1, -1
		for _, c := range line {
			if tools.Isdigit(byte(c)) {
				d2 = int(c) - '0'
				if d1 < 0 {
					d1 = d2
				}
			}
		}
		sum += d1 * 10 + d2
	}
	return sum
}

func part2(data []string) int {
	sum := 0
	for _, line := range data {
        d1, d2 := -1, -1
		for i := 0; i < len(line); i++ {
            if tools.Isdigit(line[i]) {
                d2 = int(line[i]) - '0'
            } else {
				for j, num := range nums {
                    l := len(num)
                    if (i + l <= len(line)) && line[i:i+l] == num {
                        d2 = j
                        i += l - 2
                        break
                    }
                }
            }
			if d2 >= 0 && d1 < 0 {
				d1 = d2
			}
        }
        sum += d1 * 10 + d2
    }
    return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input,"\n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}



/*
int part2( istringstream & data )
*/
