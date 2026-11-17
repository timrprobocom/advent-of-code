package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)


var DEBUG bool = false
var TEST bool = false
var dprint = tools.Absorb

var test = "389125467"

var live = "215694783"

    
type Node struct {
	value	int
	fwd		*Node
}

func printStack( node []*Node ) {
	cur := node[0]
	for range(9) {
		fmt.Print( cur.value )
		cur = cur.fwd
	}
	fmt.Println()
}

func process( vals []int, reps int ) *Node {
    nvals := len(vals)

    dprint( "Build a list of nodes." )
	nodes := make([]*Node, nvals)
	for i,n := range vals {
		nodes[i] = &Node{n,nil}
	}
	for i,n := range nodes {
		n.fwd = nodes[(i+1) % nvals]
	}

    // This is the key -- lookup by cup value.

    dprint( "Build lookup by number." )
	lookup := make(map[int]*Node)
	for _,n := range nodes {
		lookup[n.value] = n
	}

    dprint( "Start rounds." )
    cur := nodes[0]
    for range reps {

        // Grab the three cups after the first.

		if DEBUG {
			printStack(nodes)
		}
        three := []*Node{ cur.fwd, cur.fwd.fwd, cur.fwd.fwd.fwd }

        // Remove those three cups.

        cur.fwd = three[2].fwd

		// Insert them into position.

        n := cur.value - 1
        if n == 0 {
            n = nvals
		}

		for three[0].value == n || three[1].value == n || three[2].value == n {
            n--
            if n == 0 {
                n = nvals
			}
		}

        // Find up the destination cup.

        dest := lookup[n]

        // Move the three cups after the dest,
        // Point the last of the three where dest used to point,
        // Scoot current forward.

        three[2].fwd = dest.fwd
        dest.fwd = three[0]
        cur = cur.fwd
	}

    return lookup[1]
}



func part1(data []int) int {
    nbr1 := process( data, 100 )
	mk := 0
	for link := nbr1.fwd; link.value > 1; link = link.fwd {
		mk = mk * 10 + link.value
	}
    return mk
}


func part2(data []int) int {
	vals := data
	for i := 10; i <= 1000000; i++ {
		vals = append(vals, i)
	}
    nbr1 := process( vals, 10000000 )
    return nbr1.fwd.value * nbr1.fwd.fwd.value
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	if DEBUG {
		dprint = fmt.Println
	}
	data := []int{}
	for i := range len(input) {
		data = append(data, int(input[i]-'0'))
	}

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
