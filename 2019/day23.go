package main

import (
	"fmt"
	"time"

	"aoc/tools"
	_ "embed"
)

var DEBUG = false
var TEST = false
var IMAGE = false

var test = ""

//go:embed day23.txt
var live string

type Program = tools.Program


func run(program []int) (int,int) {
	thisnat := []int{0,0}
	lastnat := []int{0,0}
	part1 := 0
	part2 := 0
    progs := []*Program{}
	for i := range 50 {
		pgm := tools.MakeProgram(program)
		pgm.Push(i)
		progs = append( progs, pgm )
	}

	for _,pgm := range progs {
		go pgm.Run()
	}

	for part2 == 0 {
        idle := thisnat[0] > 0
		for i,pgm := range progs {
			for pgm.OutSize() >= 3 {
				idle = false
				a := pgm.Pop()
				x := pgm.Pop()
				y := pgm.Pop()
				if DEBUG {
					fmt.Println(i,"sent",x,y,"to",a)
				}
				if a == 255 {
					if part1 == 0 {
						if DEBUG {
							fmt.Println("Found part 1", y)
						}
						part1 = y
					}
					if DEBUG {
						fmt.Println("NAT info",y)
					}
					thisnat[0] = x
					thisnat[1] = y
				} else {
					progs[a].Push(x)
					progs[a].Push(y)
					time.Sleep( 5 * time.Millisecond )
				}
			}
			if pgm.Waiting {
				pgm.Push(-1)
			}
		}
		if idle {
			if DEBUG {
				fmt.Println("Idle restarting", thisnat[0], thisnat[1] )
			}
			if thisnat[1] == lastnat[1] {
				part2 = thisnat[1]
				break
			}
			progs[0].Push(thisnat[0])
			progs[0].Push(thisnat[1])
			lastnat = thisnat
			thisnat = []int{0,0}
		}
	}

    return part1, part2
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(live, live)

	program := tools.GetRowNumbers[int](input)

	// We start 50 programs running.

	part1,part2 := run(program)
	fmt.Println("Part 1:", part1 )
	fmt.Println("Part 2:", part2 )
}
