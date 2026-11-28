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

//go:embed day04test.txt
var test string

//go:embed day04.txt
var live string

//[1518-02-03 23:50] Guard #661 begins shift
//[1518-02-04 00:01] falls asleep
//[1518-02-04 00:57] wakes up


// Parsing.

func parse( ln string )(string, int, int, int) {
	guard := -1
    parts := strings.Fields(ln)
	hh := tools.StrToInt(parts[1][0:2])
	mm := tools.StrToInt(parts[1][3:5])
    verb := parts[2]
    if verb == "Guard" {
        guard = tools.StrToInt(parts[3][1:])
	}
    return verb,guard,hh,mm
}

type Track struct {
	guard	int
	doze	int
	when	[60]int
}

func (self *Track) print() {
	fmt.Println("(track#",self.guard,", doze=", self.doze, ", when=", self.when )
}

func makeSleep( data []string ) map[int]*Track {
	sleeptime := make(map[int]*Track)
	sleep := 0
	guard := -1
	for _,ln := range data {
		verb,g,_,mm := parse(ln)
		if g >= 0 {
			guard = g
		}
		if verb == "falls" {
			sleep = mm
		} else if verb == "wakes" {
			_,ok := sleeptime[guard]
			if !ok {
				sleeptime[guard] = &Track{guard, 0, [60]int{}}
			}
			sleeptime[guard].doze += mm - sleep
			for minute := sleep; minute < mm; minute ++ {
				sleeptime[guard].when[minute] ++
			}
		}
	}
	return sleeptime
}



// Part 1
//
// Find most asleep.

func part1( sleeptime map[int]*Track ) int {
	var maxo *Track = nil
    for _,v := range sleeptime {
        if maxo == nil || v.doze > maxo.doze {
            maxo = v
		}
	}

    maxn := -1
    maxp := 0
    for n,v := range maxo.when {
        if v > maxp {
            maxn = n
            maxp = v
		}
	}

    if DEBUG {
        fmt.Println(maxo.guard)
        fmt.Println(maxn)
        fmt.Println('=', maxo.guard * maxn)
        fmt.Println("----")
	}

    return maxo.guard * maxn
}



// Part 2
// Find most commonly asleep minute.

func part2( sleeptime map[int]*Track ) int {
	maxn := make([]int,60)
	maxz := make([]int,60)
    for k,v := range sleeptime {
        for mm,knt := range v.when {
            if knt > maxz[mm] {
                maxz[mm] = knt
                maxn[mm] = k
			}
		}
	}

    maxval := slices.Max(maxz) 
    indval := slices.Index(maxz, maxval)
    if DEBUG {
        fmt.Println( maxn[indval], indval, maxval, "=", maxn[indval] * indval)
	}
    return maxn[indval] * indval
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

    data := strings.Split(strings.TrimSpace(input), "\n")
    sleeptime := makeSleep( data )

	fmt.Println("Part 1:", part1(sleeptime))
	fmt.Println("Part 2:", part2(sleeptime))
}

