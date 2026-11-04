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
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc`[1:]

var test1 = `
start-A
start-b
A-c
A-b
b-d
A-end
b-end`[1:]

//go:embed day12.txt
var live string

type Caves map[string][]string

func makecaves(data []string) Caves {
    caves := make(Caves)
    for _,line := range data {
		i := strings.Index(line,"-")
		left := line[:i]
		right := line[i+1:]
        if right != "start" {
            caves[left] = append(caves[left], right)
		}
        if left != "start" {
            caves[right] = append(caves[right], left)
		}
	}
    return caves
}


type Stackable struct {
	node string
	path string
	twice bool
}

func islower(s string) bool {
	return s[0] >= 'a'
}

func part1( part int, caves Caves ) int {
    paths := 0

    // Node we are considering, path we've taken so far, True if we've 
    // been to a lower-case cave twice.

    untried := tools.Stack[Stackable]{}
	untried.Push( Stackable{"start", "start", part==1} )

    for !untried.IsEmpty() {
		s,_ := untried.PopFront()

        for _,n := range caves[s.node] {
            if n == "end" {
                if DEBUG {
                    fmt.Println(s.path,n)
				}
                paths += 1
			} else if islower(n) && strings.Contains( s.path, n ) {
                if ! s.twice {
                    untried.Push( Stackable{n, s.path + " " + n, true} )
				}
			} else {
                untried.Push( Stackable{n, s.path + " " +  n, s.twice} )
			}
		}
	}

    return paths
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	caves := makecaves(strings.Split(input,"\n"))

	fmt.Println("Part 1:", part1(1,caves))
	fmt.Println("Part 2:", part1(2,caves))
}
