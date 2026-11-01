package main

import (
	"fmt"
//	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day19.txt
var live string

type State struct {
	ox int
	cl int
	ob int
	ge int
	r1 int
	r2 int
	r3 int
	r4 int
	t int
}


//  0     1   2    3   4    5     6  7     8   9    10    11   12  13   14   15       16    17   18 19 20   21 22     23   24    25    26   27  28 29 30
var test = `
Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian`[1:]

func solve( plan []int, T int ) int {
    // The state is ore inventory, robot inventory, time
    state := State{0, 0, 0, 0, 1, 0, 0, 0, T}
	q := tools.Stack[State]{}
	q.Push(state)
    seen := make(map[State]bool)
    core := max(plan[1],plan[2],plan[3],plan[5])
	best := 0
	for !q.IsEmpty() {
        state,_ := q.PopFront()

        best = max(best,state.ge)
        if state.t == 0 {
            continue
		}
		t := state.t

// What is this doing?  It produces the correct results without this, 
// but much slower.  It's saying we should never have more ore robots
// than the largest need.  Doesn't this discard bots we already bought?
// Does this just prune useless branches?

        r1 := min(state.r1, core)
        r2 := min(state.r2, plan[4])
        r3 := min(state.r3, plan[6])
		r4 := state.r4
        ox := min(state.ox, t*core    - r1*(t-1))
        cl := min(state.cl, t*plan[4] - r2*(t-1))
        ob := min(state.ob, t*plan[6] - r3*(t-1))
		ge := state.ge

		state = State{ox,cl,ob,ge,r1,r2,r3,r4,t}
        if seen[state] {
            continue
		}
        seen[state] = true

        if DEBUG && len(seen) % 1000000 == 0 {
            fmt.Println(t,best,len(seen))
		}

        q.Push(State{ox+r1,cl+r2,ob+r3,ge+r4,r1,r2,r3,r4,t-1})
        if ox >= plan[1] {
            q.Push(State{ox-plan[1]+r1, cl+r2,        ob+r3,         ge+r4, r1+1,r2,r3,r4,t-1})
		}
        if ox >= plan[2] {
            q.Push(State{ox-plan[2]+r1, cl+r2,        ob+r3,         ge+r4, r1,r2+1,r3,r4,t-1})
		}
        if ox >= plan[3] && cl >= plan[4] {
            q.Push(State{ox-plan[3]+r1, cl-plan[4]+r2,ob+r3,         ge+r4, r1,r2,r3+1,r4,t-1})
		}
        if ox >= plan[5] && ob >= plan[6] {
            q.Push(State{ox-plan[5]+r1, cl+r2,        ob-plan[6]+r3, ge+r4, r1,r2,r3,r4+1,t-1})
		}
	}
    return best
}

func part1( data [][]int ) int {
    result := 0
	for _,plan := range data {
        ans := solve(plan, 24)
        if DEBUG {
            fmt.Println("===",plan[0],ans)
		}
        result += plan[0] * ans
	}
    return result
}


func part2( data [][]int ) int {
	result := 1
    for _,plan := range data {
        ans := solve(plan, 32)
        if DEBUG {
            fmt.Println("===",plan[0],ans)
		}
        result *= ans
	}
    return result
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := tools.GetNumbers[int](input)

	fmt.Println("Part 1:", part1(data) )
	fmt.Println("Part 2:", part2(data[:min(len(data),3)]) )
}

