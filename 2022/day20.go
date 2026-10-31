package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day20.txt
var live string


var test = `
1
2
-3
3
-2
0
4`[1:]


type Grove struct {
	Pos   int
	Value int
}

// Either new is <, ==, > than old.
// If equal, no change.
// If less, everybody from new to old --
// if more, everybody from old to new --

func move( data []Grove, n int ) {
    posn := data[n].Pos
	delta := data[n].Value
	if delta < 0 {
		delta += len(data) - 1
	}
	newpos := tools.Mod( posn+delta, len(data)-1 )
	if posn < newpos {
		for i := 0; i < len(data); i++ {
			if posn < data[i].Pos && data[i].Pos <= newpos {
				data[i].Pos--
			}
		}
	} else if posn > newpos {
		for i := 0; i < len(data); i++ {
			if newpos <= data[i].Pos && data[i].Pos < posn {
				data[i].Pos++
			}
		}
	}
	data[n].Pos = newpos
}

func decode( data []Grove ) []int {
	var decoded = make([]int, len(data))
	for _,g := range data {
		decoded[g.Pos] = g.Value
	}
	return decoded
}
	

func mix(data []Grove) {
	for i := range len(data) {
        move(data, i)
	}
}


func result(data []Grove) int {
	// Find the value 0.
	zero := 0
	for _,g := range data {
		if g.Value == 0 {
			zero = g.Pos
			break
		}
	}

	sum := 0
	f1 := (zero + 1000) % len(data)
	f2 := (zero + 2000) % len(data)
	f3 := (zero + 3000) % len(data)
	for _,g := range data {
		if g.Pos == f1 || g.Pos == f2 || g.Pos == f3 {
			sum += g.Value
		}
	}

	return sum
}

func part1( data []Grove ) int {
    mix(data)
    return result(data)
}


func part2( data []Grove ) int {
    key := 811589153
	for i := 0; i < len(data); i++ {
		data[i].Value *= key
	}
    for _ = range 10 {
        mix(data)
	}
    return result(data)
}

func parse(input string) []Grove {
    data := []Grove{}
	for _,line := range strings.Split(input,"\n") {
		data = append( data, Grove{len(data), tools.StrToInt(line)})
	}
	return data
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	fmt.Println("Part 1:", part1(parse(input)) )
	fmt.Println("Part 2:", part2(parse(input)) )
}
