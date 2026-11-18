package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = []int{
	3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0,  // 365210
}

var live = []int{
3,8,1001,8,10,8,105,1,0,0,21,38,55,80,97,118,199,280,361,442,99999,3,9,101,2,9,9,1002,9,5,9,1001,9,4,9,4,9,99,3,9,101,5,9,9,102,2,9,9,1001,9,5,9,4,9,99,3,9,1001,9,4,9,102,5,9,9,101,4,9,9,102,4,9,9,1001,9,4,9,4,9,99,3,9,1001,9,3,9,1002,9,2,9,101,3,9,9,4,9,99,3,9,101,5,9,9,1002,9,2,9,101,3,9,9,1002,9,5,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99,
}


func part1( program []int ) int {
    maxval := 0
	perms := make(chan []int)
    go  tools.Permutations(perms, []int{0,1,2,3,4})
    for inputset := range perms {
		if DEBUG {
			fmt.Println( inputset )
		}
        lastval := 0
        for _,ip := range inputset {
            lastval = tools.MakeProgram(program, []int{ip, lastval}).Run().Dump()[0]
			if DEBUG {
				fmt.Println( lastval )
			}
		}
        maxval = max(maxval,lastval)
	}
    return maxval
}

func part2( program []int ) int {
    maxval := 0
	perms := make(chan []int)
    go tools.Permutations(perms, []int{5,6,7,8,9})
	empty := []int{}
    for ip := range perms {
        amps := []*tools.Program{
            tools.MakeProgram(program,empty),
            tools.MakeProgram(program,empty),
            tools.MakeProgram(program,empty),
            tools.MakeProgram(program,empty),
            tools.MakeProgram(program,empty),
        }

		// The output from 0 sends to the input of 1.

		tools.Connect( amps[0], amps[1] )
		tools.Connect( amps[1], amps[2] )
		tools.Connect( amps[2], amps[3] )
		tools.Connect( amps[3], amps[4] )
		tools.Connect( amps[4], amps[0] )

		// Set the initial phase input for each amp.

        for i := range 5 {
			amps[i].Push( ip[i] )
		}

		// Set the first signal into amp 0.

        amps[0].Push( 0 )

		// Go.

        for _,amp := range amps {
			go amp.Run()
		}

		// Wait for the chain to exit.

        amps[4].Wait()

		// The answer is waiting in amp 4's output queue.

        maxval = max( maxval, amps[4].Final )
	}

    return maxval
}

func main() {
	var input []int
	TEST, DEBUG, input = tools.Setup(test, live)

	fmt.Println("Part 1:", part1(input))
	fmt.Println("Part 2:", part2(input))
}
