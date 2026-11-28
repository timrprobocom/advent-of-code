package main

import (
	"fmt"
	"slices"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test =`
dabAcCaCBAcCcaDA`[1:]

//go:embed day05.txt
var live string


func analyze(data string) int {
	old := []byte(data)
    new := []byte{}
    for len(old) > 0 {
        if len(old) > 1 && (old[0] ^ old[1]) == 0x20 {
			old = old[1:]
            if len(new) > 0 {
                old[0] = new[len(new)-1]
				new = new[:len(new)-1]
            } else {
                old = old[1:]
			}
        } else {
			new = append( new, old[0] )
			old = old[1:]
		}
        if DEBUG {
			fmt.Print( len(old), "\r")
		}
	}
    return len(new)
}


// Part 1

func part1( data string ) int {
	return analyze(data)
}

// Part 2

func part2( data string ) int {
    track := []int{}
    for i := range 26 {
        uc := string('A'+byte(i))
		lc := string('a'+byte(i))

        knt := analyze( strings.ReplaceAll(strings.ReplaceAll(data, uc,  ""), lc, "") )
        if DEBUG {
            fmt.Println( "\n", uc, lc, knt)
		}
		track = append( track, knt )
	}
    mn := slices.Min(track)
    if DEBUG {
        fmt.Println( track,mn, slices.Index(track, mn) )
	}
    return int(mn)
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, strings.TrimSpace(live))

	fmt.Println("Part 1:", part1(input))
	fmt.Println("Part 2:", part2(input))
}

