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
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green`[1:]

//go:embed day02.txt
var live string

var check []int = []int{12,13,14}

// Might try this as a state machine, word by word.

func reformat( data []string ) [][][]int {
	var record [][][]int
	for _,line := range data {
		parts := strings.Split(line, ": ")
		var game [][]int
		for _, g := range strings.Split(parts[1], "; ") {
            c := map[string]int{"red":0, "green":0, "blue":0}
            for _, p := range strings.Split( g, ", " ) {
				ab := strings.Split( p, " " )
                c[ab[1]] = tools.StrToInt( ab[0] )
			}
            game = append( game, []int{c["red"],c["green"],c["blue"]} )
		}
		record = append( record, game )
	}
    return record
}

func part1(record [][][]int) int {
    sum := 0
	for game, data := range record {
		bad := false
		for _,row := range data {
			for i := range 3 {
				bad = bad || row[i] > check[i]
			}
		}
        if !bad {
            sum += game + 1
		}
	}
    return sum
}

func part2(record [][][]int) int {
    sum := 0
	for _, data := range record {
        cnt := []int{0,0,0}
		for _, row := range data {
			for i := range 3 {
				cnt[i] = max(cnt[i], row[i])
			}
		}
        sum += cnt[0]*cnt[1]*cnt[2]
	}
    return sum
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := reformat( strings.Split(input,"\n") )

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}

