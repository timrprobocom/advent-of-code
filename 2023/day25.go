package main

import (
	"fmt"
	"strings"
	"slices"
	"math/rand"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr`[1:]

//go:embed day25.txt
var live string

type Graph map[string][]string


func make_graph( data string ) Graph {
    graph := make(map[string][]string)
    var base string
	for _, word := range strings.Fields(data) {
		if word[len(word)-1] == ':' {
            base = word[:len(word)-1]
        } else {
			graph[base] = append( graph[base], word )
			graph[word] = append( graph[word], base )
        }
    }
	return graph
}

func reachableNodes( graph Graph, start string ) map[string]bool {
	seen := make(map[string]bool)
	seen[start] = true
	queue := []string{start}
	for len(queue) > 0 {
		v := queue[0]
		queue = queue[1:]
        seen[v] = true
		for _, edge := range graph[v] {
            if !seen[edge] {
				queue = append( queue, edge )
			}
		}
    }
    return seen
}

func shortestPath( graph Graph, v1 string, v2 string ) string {
	queue := []string{v1}
	seen := make(map[string]bool)
	for len(queue) > 0 {
		path := queue[0]
		queue = queue[1:]
        v := path[len(path)-3:]
        if v == v2 {
            return path
		}
        seen[v] = true
		for _, n := range graph[v] {
            if !seen[n] {
				queue = append( queue, path+","+n )
			}
		}
    }
    return ""
}


// We repeatedly pick two random vertices and find the shortest path between them via BFS.
// Then pick the top k most travelled edges and remove these from the graph and
// check if we have succesfully made a k cut. If so return it, if not we continue
//
// noCrossings - How many crossings to collect statistics on per attempt.
// k - Stop when we find a k-cut.
// Returns the size of one of the partitions.

func minimumCut( graph Graph, noCrossings int, cut int ) int {
	var keys  []string
	for k := range graph {
		keys = append( keys, k )
	}

    for {
		crossingCounts := make(map[string]int)
		for range noCrossings {
			v1 := keys[rand.Intn(len(keys))]
			v2 := keys[rand.Intn(len(keys))]
			path := shortestPath(graph, v1, v2)

            for j := 4; j < len(path); j += 4 {
                p1 := path[j-4:j-1]
                p2 := path[j:j+3]
                crossingCounts[p1+p2] ++
            }
        }

        // Convert the crossing counters to something that can be sorted.

		type Pair struct {
			i int
			s string
		}

		cross2 := make([]Pair, len(crossingCounts))
		for k, v := range crossingCounts {
			cross2 = append( cross2, Pair{v,k} )
		}
		slices.SortFunc( cross2, func( a,b Pair ) int {
            return b.i - a.i
        })

        // Remove the 3 edges that we are guessing make the min cut.

        cross2 = cross2[:3]

        g2 := make(Graph)
		for k, v := range graph {
			g2[k] = slices.Clone(v)
		}

		for _, v := range cross2 {
			key0 := v.s[0:3]
			key1 := v.s[3:6]
			g2[key0] = slices.DeleteFunc( g2[key0], func(k string) bool { return k == key1 })
			g2[key1] = slices.DeleteFunc( g2[key1], func(k string) bool { return k == key0 })
        }

        canReach := reachableNodes(g2, keys[0])
		if len(canReach) < len(graph) {
            return len(canReach)
		}
    }

    return 0
}

func part1( graph Graph ) int {
    one := minimumCut( graph, 10, 3 );
    two := len(graph) - one;
    return one*two;
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

    graph := make_graph( input )

	fmt.Println("Part 1:", part1(graph)) // 485607
}

