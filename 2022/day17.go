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

//go:embed day17.txt
var live string

var test = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

// We're making tetris!

type Point struct {
	X int64
	Y int64
}

type PointSet = map[Point]bool

type Rock = PointSet

var rocktypes = [][][]int{
    {{0,0},{1,0},{2,0},{3,0}},
    {{1,2},{0,1},{1,1},{2,1},{1,0}},
    {{2,2},{2,1},{0,0},{1,0},{2,0}},
    {{0,3},{0,2},{0,1},{0,0}},
    {{0,1},{1,1},{0,0},{1,0}},
}

// Left edge is 0, b0t edge is 0

func makerock( kind, x int, y int64) Rock {
	rock := make(Rock)
	for _,pt := range rocktypes[kind] {
		rock[Point{int64(pt[0]+x), int64(pt[1])+y}] = true
	}
	return rock
}

func left(rock Rock) Rock {
	pts := make(Rock)
	for p,_ := range rock {
		if p.X == 0 {
			return rock
		}
		pts[Point{p.X-1,p.Y}] = true
	}
	return pts
}

func right(rock Rock) Rock {
	pts := make(Rock)
	for p,_ := range rock {
		if p.X >= 6 {
			return rock
		}
		pts[Point{p.X+1,p.Y}] = true
	}
	return pts
}

func down(rock Rock) Rock {
	pts := make(Rock)
	for p,_ := range rock {
		if p.Y == 0 {
			return rock
		}
		pts[Point{p.X,p.Y-1}] = true
	}
	return pts
}

var BIG int64 = 1000000000000

/*
func up(rock Rock) Rock {
	pts := make(Rock)
	for p,_ := range rock {
		pts[Point{p.X,p.Y+1}] = true
	}
	return pts
}
*/

func top(rock Rock) int64 {
	var maxx int64 = 0
	for p,_ := range rock {
		maxx = max(maxx, p.Y)
	}
	return maxx
}

func bottom(rock Rock) int64 {
	var minx int64 = BIG
	for p,_ := range rock {
		minx = min(minx, p.Y)
	}
	return minx
}

func printRock(rock Rock) {
	fmt.Print( "<" )
	for pt,_ := range rock {
		fmt.Print( " ",pt.X,",",pt.Y )
	}
	fmt.Println(">")
}

func collision( rock Rock, rocks PointSet ) bool {
	for pt,_ := range rock {
		if rocks[pt] {
			return true
		}
	}
	return false
}

func toprow( rocks PointSet )  int64 {
	var maxx int64 = 0
	for pt,_ := range rocks {
		maxx = max(maxx, pt.Y)
	}
	return maxx
}

func plot(rocks PointSet) {
    ymax := toprow(rocks)
	chart := [][]byte{}
	for _ = range(ymax+2) {
		chart = append(chart, []byte("......."))
	}
	for pt,_ := range rocks {
		chart[ymax-pt.Y+1][pt.X] = '#'
	}
    for _,row := range chart {
		fmt.Println( "|"+string(row)+"|")
	}
    fmt.Println("|-------|")
}


func part1( moves string ) int64 {
    n := len(moves)
    rocks := make(PointSet)
    step := 0
	for i := range 2022 {
        if i > 0 && DEBUG {
            plot(rocks)
		}
		var y int64 = 3
		if len(rocks) > 0 {
			y = toprow(rocks) + 4
		}

        rock := makerock(i%len(rocktypes), 2, y )
		for true {

            // Go left/right.

            code := moves[step % n]
            step ++
			rock0 := Rock{}
            if code == '<' {
                rock0 = left(rock)
            } else {
                rock0 = right(rock)
			}
            if !collision(rock0,rocks) {
				rock = rock0
			}

            // Go down.

            if bottom(rock) == 0 {
				for pt,_ := range rock {
					rocks[pt] = true
				}
                break
			}
            rock0 = down(rock)
            if !collision(rock0,rocks) {
				rock = rock0
			} else {
				for pt,_ := range rock {
					rocks[pt] = true
				}
				break
			}
		}
	}

    return toprow(rocks)+1
}

func signature( step int, rocktype int, rocks PointSet ) string {
    maxy := toprow(rocks)
	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("|%d,%d", step, rocktype))

    deltas := []int{}
	for pt,_ := range rocks {
		dy := maxy-pt.Y
		if dy < 30 {
			deltas = append( deltas, int(dy*10+pt.X) )
		}
	}
	slices.Sort(deltas)

	for _,n := range deltas {
		sb.WriteString(fmt.Sprintf(";%d",n))
	}
    return sb.String()
}

func part2( moves string ) int64 {
    n := len(moves)
    rocks := make(PointSet)
    step := 0
	var layers int64 = 0
	seen := make(map[string]Point)

	var i int64 = 0
	for i <= BIG {
		if DEBUG {
			fmt.Print(i,"\r")
		}

		var y int64 = 3
		if len(rocks) > 0 {
			y = toprow(rocks) + 4
		}

        rt := int(i%int64(len(rocktypes)))
        rock := makerock(rt, 2, y )
		for true {

            // Go left/right.

            code := moves[step % n]
            step ++
			rock0 := Rock{}
            if code == '<' {
                rock0 = left(rock)
            } else {
                rock0 = right(rock)
			}
            if !collision(rock0,rocks) {
				rock = rock0
			}

            // Go down.

            if bottom(rock) == 0 {
				for pt,_ := range rock {
					rocks[pt] = true
				}
                break
			}
            rock0 = down(rock)
			if !collision(rock0, rocks) {
				rock = rock0
				continue
			}
			for pt,_ := range rock {
				rocks[pt] = true
			}

			top := toprow(rocks)
			sig := signature(step%len(moves), rt, rocks)
			if DEBUG {
				fmt.Println(sig)
			}
			oldty,ok := seen[sig]
			if layers == 0 && ok {
				dt := i - oldty.X
				dy := top - oldty.Y
				if DEBUG {
					fmt.Println("cycle:", i,y,oldty,dt,dy)
				}
				cycles := (BIG-i)/dt
				layers += cycles*dy
				i += cycles*dt
			}
			seen[sig] = Point{i,top}
			break
		}
		i++
	}

    return toprow(rocks)+layers
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	fmt.Println("Part 1:", part1(input) )
	fmt.Println("Part 2:", part2(input) )
}
