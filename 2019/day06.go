package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false


var test = `
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L`[1:]

//go:embed day06.txt
var live string

type Node struct {
	me		string
	parent 	string
	child 	[]string
	depth 	int
}

type Tree = map[string]*Node

func makeNode( me string ) *Node {
	return &Node{ me, "", []string{}, 0}
}

func addToTree( tree Tree, name string ) {
	a,b,_ := strings.Cut(name, ")")
	_,ok := tree[a]
	if !ok {
		tree[a] = makeNode(a)
	}
	_,ok = tree[b]
	if !ok {
		tree[b] = makeNode(b)
	}
	tree[a].child = append( tree[a].child, b )
	tree[b].parent = a
}


func makeTree( data []string ) Tree {
	tree := make(Tree)
	for _,ln := range data {
		addToTree( tree, ln )
	}
	return tree
}


var xsum int

//  Part 1

func count( tree Tree, st string, depth int ) int {
    e := tree[st]
    e.depth = depth
    for _,i := range e.child {
        count(tree, i,depth+1)
        if DEBUG {
            fmt.Println( st, ": After", i, " now ", depth )
		}
        xsum += depth + 1
	}
    return xsum
}
    

func part1( tree Tree  ) int {
    return count(tree, "COM", 0)
}

// Part 2.

func getpath( tree Tree, el string, path []string ) []string {
    cell := tree[el]
    if len(cell.parent) > 0 {
        return getpath( tree, cell.parent, append( path, cell.parent) )
	}
    return path
}

func part2( tree Tree ) int {
	if DEBUG {
		for k,v := range tree {
			fmt.Println(k, *v)
		}
	}
	you := make(map[string]bool)
	for _,s := range getpath(tree, "YOU", []string{}) {
		you[s] = true
	}
	santa := make(map[string]bool)
	equal := make(map[string]bool)
	for _,s := range  getpath(tree, "SAN", []string{}) {
		santa[s] = true
		if you[s] {
			equal[s] = true
		}
	}

    if DEBUG {
        fmt.Println( "Part 2: " )
        fmt.Println( "YOU", len(you) )
        fmt.Println( "SANTA:", len(santa) )
        fmt.Println( "COMMON:", len(equal) )
	}

	// How many steps on the two branches that are not in common:

    return  len(you)-len(equal) + len(santa)-len(equal)
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")
	tree := makeTree(data)

	fmt.Println("Part 1:", part1(tree))
	if TEST {
        addToTree( tree, "K)YOU" );
        addToTree( tree, "I)SAN" );
	}
	fmt.Println("Part 2:", part2(tree))
}

