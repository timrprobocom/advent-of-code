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

var test string = `
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn`[1:]

//go:embed day23.txt
var live string




func part1( data []string ) int {
	connx := make(map[string]map[string]bool)

	for _,line := range data {
		a := line[0:2]
		b := line[3:]
		if connx[a] == nil {
			connx[a] = make(map[string]bool)
		}
		if connx[b] == nil {
			connx[b] = make(map[string]bool)
		}
        connx[a][b] = true
        connx[b][a] = true
	}
    
	uniq := make(map[string]bool)
	for k,v := range connx {
        for v1,_ := range v {
			for v2,_ := range v {
                if k[0] == 't' || v1[0] == 't' || v2[0] == 't' {
                    if v1 != v2 && connx[v2][k] && connx[v2][v1] {
						makeme := []string{k,v1,v2}
						slices.Sort(makeme)
						uniq[strings.Join(makeme,"-")] = true
					}
				}
			}
		}
	}
    return len(uniq)
}

func intersect( m1 map[string]bool, m2 map[string]bool ) map[string]bool {
	newx := make(map[string]bool)
	for k := range m1 {
		if m2[k] {
			newx[k] = true
		}
	}
	return newx
}

func part2( data []string ) string {
	connx := make(map[string]map[string]bool)

	for _,line := range data {
		a := line[0:2]
		b := line[3:]
		if connx[a] == nil {
			connx[a] = make(map[string]bool)
		}
		if connx[b] == nil {
			connx[b] = make(map[string]bool)
		}
        connx[a][a] = true
        connx[a][b] = true
        connx[b][a] = true
        connx[b][b] = true
	}
   
    // Make an intersection of all permutations.

	matches := []map[string]bool{}
	for _,a := range connx {
		for _,b := range connx {
			matches = append( matches, intersect(a, b) )
		}
	}

    // For all the players in those matches, find the intersection 
	// of all of its followers and count how many times each combo
	// appears.

    poss := make(map[string]int)
	for _,m := range matches {
		if len(m) < 3 {
			continue
		}

		base := m
		for n := range m {
			base = intersect( base, connx[n] )
		}

		if len(base) > 1 {
			names := []string{}
			for k := range base {
				names = append( names, k )
			}
			slices.Sort(names)
			poss[strings.Join(names, ",")] ++
		}
	}

    // Return the most common subset found.

    type SortHelper struct {
		count int
		name string
	}

    sortme := []SortHelper{}
	for k,v := range poss {
		sortme = append( sortme, SortHelper{v,k} )
	}
	slices.SortFunc(sortme, func(a, b SortHelper) int { return b.count - a.count })

    if DEBUG {
		for _,top := range sortme {
			fmt.Println(top)
		}
	}
    return sortme[0].name
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := strings.Split(input,"\n") 

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}

