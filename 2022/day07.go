package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day07.txt
var live string

var test = `
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k`[1:]

type Node struct {
	Name     string
	Children map[string]*Node
	Size     int64
	Allsize  int64
}

func makeNode(name string) *Node {
	return &Node{
		Name:     name,
		Children: make(map[string]*Node),
		Size:     0,
		Allsize:  0,
	}
}

func (s Node) Print() {
	if DEBUG {
		fmt.Println("<Node", s.Name, "has", len(s.Children), "children, size", s.Size, ", allsize", s.Allsize, ">")
	}
}

func (s *Node) Find(path []string) *Node {
	for _, c := range path {
		s = s.Children[c]
	}
	return s
}

func part1(data []string) (int64, int64) {
	root := makeNode("/")
	leaf := root
	cd := []string{}

	// Build the tree.

	for _, line := range data {
		if DEBUG {
			fmt.Print("Leaf: ")
			fmt.Println("Command:", line)
			leaf.Print()
		}
		parts := strings.Split(line, " ")
		if parts[0] == "$" {
			if parts[1] == "cd" {
				if parts[2] == "/" {
					cd = []string{}
					leaf = root
				} else if parts[2] == ".." {
					cd = cd[:len(cd)-1]
					leaf = root.Find(cd)
				} else {
					cd = append(cd, parts[2])
					leaf = leaf.Children[parts[2]]
				}
			}
		} else if parts[0] == "dir" {
			leaf.Children[parts[1]] = makeNode(parts[1])
		} else {
			leaf.Size += tools.StrToInt64(parts[0])
		}
	}

	// Make a list in depth order.

	q := []*Node{root}
	for i := 0; i < len(q); i++ {
		q = append(q, tools.Values(q[i].Children)...)
	}

	if DEBUG {
		for _, qq := range q {
			qq.Print()
		}
	}

	// Unroll that, accumulating the sizes, summing those below 100000.

	var qsum int64 = 0
	for len(q) > 0 {
		node := q[len(q)-1]
		q = q[:len(q)-1]
		node.Allsize = node.Size
		if len(node.Children) > 0 {
			for _, v := range node.Children {
				node.Allsize += v.Allsize
			}
		}
		if node.Allsize <= 100000 {
			qsum += node.Allsize
		}
	}

	need := root.Allsize - 40000000

	// Now do a top-down, remembering all sizes larger than "need".

	q = []*Node{root}
	var poss []int64

	for len(q) > 0 {
		node := q[len(q)-1]
		q = q[:len(q)-1]
		if node.Allsize >= need {
			poss = append(poss, node.Allsize)
		}
		q = append(q, tools.Values(node.Children)...)
	}
	if DEBUG {
		fmt.Println(poss)
	}

	return qsum, tools.Min(poss)
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	p1, p2 := part1(data)
	fmt.Println("Part 1:", p1)
	fmt.Println("Part 2:", p2)
}
