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
`[1:]

//go:embed day08.txt
var live string

// We have a set of 25x6 grids.

const GRID = 25*6

func part1( data string ) int {
    min0 := 99999
	best := 0
	for i := 0; i < len(data)-2; i += GRID {
		ln := data[i:i+GRID]
        i0 := strings.Count(ln, "0")
        i1 := strings.Count(ln, "1")
        i2 := strings.Count(ln, "2")
        ccc := ""
        if i0 < min0  {
            ccc = "***"
            best = i1*i2
            min0 = i0
		}

        if DEBUG {
            fmt.Println( i0, i1, i2, i1*i2, ccc )
		}
	}
	return best
}

func part2( data string ) string {
	s := []byte(strings.Repeat("2", GRID))
	for i := 0; i < len(data); i += GRID {
		ln := data[i:i+GRID]
		for j := range GRID {
            if s[j] == '2' {
                s[j] = ln[j]
			}
		}
	}

    out := []string{}
	for i := 0; i < 150; i += 25 {
		out = append( out, strings.ReplaceAll(string(s[i:i+25]),"0"," "))
	}
		
    return strings.Join( out, "\n" )
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	input = strings.TrimSpace(input)

    if TEST {
		fmt.Println( "TEST not supported.")
		return
	}

	fmt.Println("Part 1:", part1(input))
	fmt.Println("Part 2:")
	fmt.Println(part2(input))
}


