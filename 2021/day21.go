package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = []int{4,8}
var live = []int{9,10}



type Dice struct {
	val int
}

func (d *Dice) next() int {
	val := d.val
	d.val = (d.val + 1) % 100
	return val
}


func part1( a, b int ) int {
	data := []int{a,b}
	dice := Dice{1}
    score := []int{0,0}
    count := 0
	p := 0
    for true {
        p = count & 1
        turn := dice.next() + dice.next() + dice.next()
        count += 3
        data[p] = (data[p] + turn - 1) % 10 + 1
        score[p] += data[p]
        if score[p] >= 1000 {
            break
		}
	}
    if DEBUG {
        fmt.Println(count, data, score)
	}
    return count * score[1-p]
}

type State struct {
	score0	int
	pos0	int
	score1	int
	pos1	int
	turn	int
}

func part2( a, b int ) int {
    // There are 7 possible outcomes of three dice, in a Gaussian curve.

    data := []int{a,b}
    dice := make([]int, 10)
	poss := []int{1,2,3}
	for _,i := range poss {
		for _,j := range poss {
			for _,k := range poss {
				dice[i+j+k] ++
			}
		}
	}

    // Score, position, score, position, next player.
	universes := make(map[State]int)
	universes[State{0, data[0], 0, data[1], 0}] = 1
    wins := make([]int,2)

    // It takes 9 or 10 rolls to win.  The key trick is that, at each roll, there are 
    // only a few distinct states (at most about 11,000).  Many universes share the same 
    // state.  We need to track those counts.

    for len(universes) > 0 {
        newu := make(map[State]int)
        // For each state (and many universes share the same state, that's the key):
		for state, cnt := range universes {
            if DEBUG {
                fmt.Println(state,cnt)
			}

            //  The current player is always first.

            for val,prob := range dice {
				if prob == 0 {
					continue
				}
				p := (state.pos0 + val - 1) % 10 + 1
                s := state.score0 + p
                if s >= 21 {
                    wins[state.turn] += cnt * prob
                    continue
				}

                // Swap positions for the next turn.
                newu[State{state.score1,state.pos1,s,p,1-state.turn}] += cnt * prob
			}
		}

        universes = newu
	}
	if DEBUG {
		fmt.Println(wins)
	}
    return tools.Max(wins)
}


func main() {
	var input []int
	TEST, DEBUG, input = tools.Setup(test, live)

	fmt.Println( "Part 1:", part1(input[0], input[1]))
	fmt.Println( "Part 2:", part2(input[0], input[1]))
}

