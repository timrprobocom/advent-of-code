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

// 13312 ORE for 1 FUEL:

var test1 = `
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT`[1:]

// 180697 ORE for 1 FUEL:

var test2 = `
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF`[1:]

// 2210736 ORE for 1 FUEL:

var test3 = `
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX`[1:]

var test = test3

//go:embed day14.txt
var live string


// Topological sort.

type Graph struct {
	graph map[string][]string
	nodes map[string]bool
}

func makeGraph() Graph {
	return Graph{
		make(map[string][]string),
		make(map[string]bool),
	}
}

func (self Graph) addEdge(u, v string) {
	self.nodes[u] = true
	self.nodes[v] = true
	self.graph[u] = append(self.graph[u], v )
}

func (self Graph) topoSortUtil( v string, visited map[string]bool, stack []string) []string {
	visited[v] = true
	for _,i := range self.graph[v] {
		if ! visited[i] {
			stack = self.topoSortUtil(i, visited, stack )
		}
	}
	stack = append( stack, v )
	return stack
}

func (self Graph) topoSort() []string {
	// Mark all vertices not visited.
	visited := make(map[string]bool)
	stack := []string{}

	for i,_ := range self.nodes {
		if ! visited[i] {
			stack = self.topoSortUtil( i, visited, stack )
		}
	}

    slices.Reverse(stack)
	return stack
}


type Mix struct {
	sym	string
	qty	int
	needs map[string]int
}

func (self Mix) __repr__() string {
	s := fmt.Sprintf("<Mix %s x %d from ", self.sym, self.qty)
	for k,v := range self.needs {
		s += fmt.Sprintf( " + %s %d", k, v )
	}
	s += ">"
	return s
}


func parse( data []string ) (map[string]Mix, []string) {
    tree := make(map[string]Mix)
    graph := makeGraph()
	for _,line := range data {
        lll,rrr,_ := strings.Cut(line, " => ")
        q,sym,_ := strings.Cut(rrr, " ")
        chem := Mix{sym,tools.StrToInt(q), map[string]int{}}
        tree[sym] = chem

		for _,part := range strings.Split(lll, ", ") {
            q,sym,_ := strings.Cut(part, " ")
            graph.addEdge( chem.sym, sym )
            chem.needs[sym] = tools.StrToInt(q)
		}
	}
    return tree, graph.topoSort()
}

func processloop( tree map[string]Mix, amts map[string]int, chem string ) {
    qty := amts[chem]
    amts[chem] = 0
    if DEBUG {
        fmt.Println( qty, "of", chem, "needs:" )
	}
    mix := tree[chem]
    qty = (qty+mix.qty-1) / mix.qty
    if DEBUG {
        print( "   ", qty, " units" )
	}
    for a,b := range mix.needs {
        if DEBUG {
            print( "   ", b+qty, " of ", a )
		}
        amts[a] += b*qty
	}
	if DEBUG {
		print("\n")
	}
}


// Part 1

func part1( s []string, target int ) int {
    tree, order := parse(s)
    if DEBUG {
        fmt.Println( order )
		fmt.Println( tree )
	}
    amts := make(map[string]int)
    amts["FUEL"] = target
    amts["ORE"] = 0

	for _,i := range order {
        if i == "ORE" {
            break
		}
        processloop(tree, amts, i )
        if DEBUG {
			fmt.Print( "Stores: " )
            for _,k := range order {
				fmt.Print( k, ":", amts[k] )
			}
            fmt.Println()
		}
	}
    return amts["ORE"]
}


// Part 2.

func part2( data []string ) int {
    ore := 1000000000000
    guess := 1

    // Times 10 until we go over.

    for true {
        got := part1( data, guess )
        if DEBUG {
			fmt.Println(guess, "got", got)
		}
        if got > ore {
            break
		}
        guess *= 10
	}

    // Back down and do one digit at a time.

    guess /= 10
    incr := guess

    for incr > 0 {
        guess += incr
        got := part1( data, guess )
        if DEBUG {
            fmt.Println(guess, "got", got)
		}
        if got > ore {
            guess -= incr
            incr /= 10
		}
	}
    return guess
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test,live)
	data := strings.Split(strings.TrimSpace(input), "\n")

	fmt.Println( "Part 1:", part1(data, 1))
	fmt.Println( "Part 2:", part2(data))
}
