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
939
7,13,x,x,59,x,31,19`[1:]

//go:embed day13.txt
var live string

type Point = tools.Point


var deltas = map[byte]Point { 
    'N': Point{ 0,-1},
    'E': Point{ 1, 0},
    'S': Point{ 0, 1},
    'W': Point{-1, 0},
}

// N and W are negative.


func part1(stamp int, posns []int, buses []int) int {
    winline := 0
    wintime := 9999999999999
    for _,line := range buses {
        poss := (stamp + line - 1) / line * line
        if poss < wintime {
            winline = line
            wintime = poss
		}
	}
    if DEBUG {
        fmt.Println( winline, wintime )
	}

    return winline*(wintime-stamp)
}

// Keep trying multiples of the first that satisfy the second.
//
// There is a subtle problem here.  The code does not work if
// reverse the arrays or reverse the order of the paraneter pairs.
// This is the difference between (t+a) % n and (t % n == a).
// The 'a' in the posns array is the first type.  The 'a'
// we return here is the second type.  The 0 in 7,0 doesn't
// care, so it works either way.


func findcommon2( a1, n1, a2, n2 int) (int, int) {
    // This version returns a (t % n == a) answer, and
    // thus needs posns to be negated, but also works
    // with the arrays reversed.
    inc := n1
    t := inc - a1
    for (t+a2) % n2 > 0 {
        t += inc
	}
    return n1*n2 - t, n1*n2
}

func findcommon1( a1, n1, a2, n2 int) (int, int) {
    // This version returns a (t+a % n) answer.
    inc := n1
    t := inc + a1
    for (t+a2) % n2 > 0 {
        t += inc
	}
    return t, n1*n2
}

var findcommon = findcommon1

// Satisfy 2 at a time until we get them all.

func part2(stamp int, posns []int, buses []int) int {
    a0 := posns[0]
    n0 := buses[0]
	for i := 1; i < len(posns); i++ {
        if DEBUG {
            fmt.Println( a0, n0 )
		}
        a1 := posns[i]
        n1 := buses[i]
        a0, n0 = findcommon( a0, n0, a1, n1 )
// This also works.
//        a0, n0 = findcommon( n1-a1, n1, n0-a0, n0 )
// This works if we use the b-p list below.
//        a0, n0 = findcommon( a1, n1, n0-a0, n0 )
	}
	if DEBUG {
		fmt.Println(a0,n0)
	}
    return a0
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	p1,p2,_ := strings.Cut(strings.TrimSpace(input), "\n")
	stamp := tools.StrToInt(p1)

	posns := []int{}
	buses := []int{}

	for i,b := range strings.Split(p2,",") {
		if b != "x" {
			posns = append( posns, i )
			buses = append( buses, tools.StrToInt(b) )
		}
	}

	if DEBUG {
    	fmt.Println( posns, buses )
	}

	fmt.Println("Part 1:", part1(stamp, posns,buses))
	fmt.Println("Part 2:", part2(stamp, posns,buses))
}


// So they are all equal again at 1,131,189,818,632,523.
//
// 0 1 3 5 6     1068781
//
// 7 and 13 are off by 6 then 5 then 4 then 3 then 2 then 1 then 0
// 7 and 59 are off by 4 then 1 then 5 then 2 then 6 then 3 then 0
// 7 and 31 are off by 4 then 1 then 5 then 2 then 6 then 3 then 0
// 7 and 19 are off by 2 then 4 then 6 then 1 then 3 then 5 then 0
//
// so 7 and 13 line up at 77 mod 91
