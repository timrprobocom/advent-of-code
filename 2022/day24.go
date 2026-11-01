package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day24.txt
var live string


var test = `
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#`[1:]

type Info struct {
	WID 	int
	HGT 	int
	IN 		Point
	OUT 	Point
	CYCLE 	int
}

type Point = tools.Point

type OurMap = map[Point]string

var info Info

var dircodes = map[byte]Point {
    '>': Point{1,0},
    'v': Point{0,1},
    '<': Point{-1,0},
    '^': Point{0,-1},
}

var directions = []Point {
	Point{1,0},
	Point{0,1},
	Point{-1,0},
	Point{0,-1},
	Point{0,0},
}

var patterns []OurMap


func parse( data [] string ) OurMap {
	res := make(OurMap)
    for y,row := range data[1:len(data)-1] {
        for x,col := range row[1:len(row)-1] {
            if col == '#' {
                fmt.Println("Found a wall", x, y)
			}
            if col != '.' {
                res[Point{x,y}] += string(col)
			}
		}
	}
    return res
}


func shift( mymap OurMap ) OurMap {
	res := make(OurMap)
	for pt,storms := range mymap {
		for i := range(len(storms)) {
			v := storms[i]
            dxy := dircodes[v]
			xy0 := pt.Add(dxy)
			xy0.X = tools.Mod(xy0.X, info.WID)
			xy0.Y = tools.Mod(xy0.Y, info.HGT)
			res[xy0] += string(v)
		}
	}
    return res
}


func plot( grid OurMap ) {
	plt := make([][]byte, info.HGT)
	for i := range info.HGT {
		plt[i] = tools.Repeat( "."[0], info.WID )
	}

    for pt,v := range grid {
        if len(v) > 1 {
            plt[pt.Y][pt.X] = "123456789"[len(v)]
        } else {
            plt[pt.Y][pt.X] = v[0]
		}
	}
	print(strings.Repeat("#",info.WID+2))
	print("\n")
    for _,row := range plt {
        print("#"+string(row)+"#\n" )
	}
	print(strings.Repeat("#",info.WID+2))
	print("\n")
}


type Queue struct {
	Pt 	 Point
	Time int
}


func solve( startpt Point, endpt Point, t int ) int {
	q := tools.Stack[Queue]{}
	q.Push(Queue{startpt, t})
    seen := []map[Point]bool{}
    for !q.IsEmpty() {
		item,_ := q.PopFront()
		xy := item.Pt
		t := item.Time

        if DEBUG {
            fmt.Println(item)
		}

        t += 1
		for len(seen) <= t {
			seen = append( seen, make(map[Point]bool) )
		}
        grid := patterns[t % info.CYCLE]

        for _,dxy := range directions {
			xy0 := xy.Add(dxy)
            if xy0 == endpt {
                return t
			}
			if tools.Between(0,xy0.X,info.WID) &&
				tools.Between(0,xy0.Y,info.HGT) &&
				len(grid[xy0]) == 0 && !seen[t][xy0] {

                seen[t][xy0] = true
                q.Push( Queue{xy0,t} )
			}
		}
        
        // As a last resort, stay at home.

        if xy == startpt {
            q.Push( Queue{xy,t} )
		}
	}

    fmt.Println("fail at",t)
    return -1
}


func part1( result chan int ) {
	defer close(result)

    t := solve( info.IN, info.OUT, 0 )
    result <- t

    t = solve( info.OUT, Point{0,0}, t-1 )
    t = solve( info.IN, info.OUT, t-1 )
    result <- t
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input,"\n") 
	mymap := parse(data)

	info.WID = len(data[0])-2
	info.HGT = len(data)-2
	info.IN = Point{0,-1}
	info.OUT = Point{info.WID-1,info.HGT}
	info.CYCLE = tools.Lcm(info.WID,info.HGT)

	for _ = range info.CYCLE {
		patterns = append(patterns, mymap)
		mymap = shift(mymap)
	}

    channel := make(chan int)
	go part1(channel)

    part := 0
	for res := range channel {
		part ++
		fmt.Printf("Part %d: %d\n", part, res)
	}
}
