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
var dprint = tools.Absorb

var test = `
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10`[1:]

//go:embed day22.txt
var live string

func parse(decks []string) ([]int, []int) {
	out := [][]int{}
	for _,d := range decks {
		row := []int{}
		deck := strings.Split(d,"\n")
		for _,line := range deck[1:] {
			row = append( row, tools.StrToInt(line) )
		}
		out = append( out, row )
	}
	return out[0],out[1]
}

func score(deck1 []int, deck2 []int) int {
	d := []int{}
	d = append( d, deck1... )
	d = append( d, deck2... )
	sum := 0
	for i,v := range d {
		sum += (len(d)-i) * v
	}
	return sum
}



func part1(data []string) int {
    deck1,deck2 := parse(data)
	for len(deck1) > 0 && len(deck2) > 0 {
        dprint( deck1, deck2 )
		d1 := deck1[0]
		d2 := deck2[0]
		deck1 = deck1[1:]
		deck2 = deck2[1:]
        if d1 > d2 {
			deck1 = append(deck1, d1)
			deck1 = append(deck1, d2)
        } else {
			deck2 = append(deck2, d2)
			deck2 = append(deck2, d1)
		}
	}

    return score(deck1,deck2)
}

// This enables memoization.
func encode(d1,d2 []int) string {
	out := []byte{}
	for _,d := range d1 {
		out = append(out, byte(d+32))
	}
	out = append(out, '/')
	for _,d := range d2 {
		out = append(out, byte(d+32))
	}
	return string(out)
}

func whoWins( deck1, deck2 []int ) int {
	if len(deck1) > len(deck2 ) {
		return 0
	}
	return 1
}

func rounds( deck1, deck2 []int, depth int) (int,int) {
	tab := strings.Repeat(" ", depth*2)
    dprint( tab, depth, "Recurse...", deck1, deck2 )
    remember := make(map[string]bool)
	for len(deck1) > 0 && len(deck2) > 0 {
        dprint( tab, deck1, deck2 )
        e := encode(deck1,deck2)
        if remember[e] {
            dprint( tab, "Player 1 wins by dup")
            return 0,0
		}

        remember[e] = true

		d1 := deck1[0]
		d2 := deck2[0]
		deck1 = deck1[1:]
		deck2 = deck2[1:]

		winner := 0
        if d1 > len(deck1) || d2 > len(deck2) {
			if d2 > d1 {
				winner = 1
            }
        } else {
            winner,_ = rounds( slices.Clone(deck1[:d1]), slices.Clone(deck2[:d2]), depth+1 )
		}
        
        if winner == 0 {
            dprint( tab, "Player 1 wins" )
			deck1 = append(deck1, d1)
			deck1 = append(deck1, d2)
        } else {
            dprint( tab, "Player 2 wins" )
			deck2 = append(deck2, d2)
			deck2 = append(deck2, d1)
		}
	}
	dprint(deck1,"   ",deck2)
	if depth == 0 {
		dprint( tab, "Game over" )
		return whoWins(deck1,deck2),score(deck1,deck2)
	} else {
		dprint( tab, "Round over" )
		return whoWins(deck1,deck2),0
	}
}


func part2(data []string) int {
    deck1,deck2 := parse(data)
	_, score := rounds( deck1, deck2, 0 )
	return score
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	if DEBUG {
		dprint = fmt.Println
	}
	data := strings.Split(strings.TrimSpace(input), "\n\n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
