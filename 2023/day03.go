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
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..`[1:]

//go:embed day03.txt
var live string

type Point struct {
	x int
	y int
}

type Number struct {
	x int
	y int
	length int
	value int
}


// Convert grid to list of numbers and symbols.

func convert( data []string ) ( []Number, []Point ) {
    var numbers []Number
	var symbols []Point
    for y,line := range data {
        num := false
        for x,c := range line {
            if tools.Isdigit(byte(c)) {
                if !num {
					numbers = append( numbers, Number{x,y,0,0} )
                    num = true
				}
                numbers[len(numbers)-1].length++
            } else {
                num = false
                if c != '.' {
                    symbols = append( symbols, Point{x,y} )
				}
			}
		}
	}
	for i,num := range numbers {
		numbers[i].value = tools.StrToInt(data[num.y,][num.x:num.x+num.length])
	}
    return numbers,symbols
}


func part2( part int, numbers []Number, symbols []Point ) int {
    sum := 0
	for _, spt := range symbols {
		var nums []int
		for _, num := range numbers {
			if num.y-1 <= spt.y && spt.y <= num.y+1 &&
				num.x-1 <= spt.x && spt.x <= num.x+num.length {
				nums = append( nums, num.value )
			}
		}
		if part == 1 {
			sum += tools.Sum(nums)
		} else if len(nums) == 2 {
			sum += nums[0] * nums[1]
		}
	}
    return sum
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input,"\n")

	numbers, symbols := convert(data)

	fmt.Println("Part 1:", part2(1, numbers, symbols)) // 514969
	fmt.Println("Part 2:", part2(2, numbers, symbols)) // 78915902
}

