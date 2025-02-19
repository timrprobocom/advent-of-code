package main

import (
	"fmt"
	"strings"
	"slices"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9`[1:]

//go:embed day22.txt
var live string


type Point struct {
	x int
	y int
}

func (pt Point) add(p2 Point) Point {
	return Point{pt.x + p2.x, pt.y + p2.y}
}

func (pt Point) addi(dx int, dy int) Point {
	return Point{pt.x + dx, pt.y + dy}
}

func (pt Point) sub(p2 Point) Point {
	return Point{pt.x - p2.x, pt.y - p2.y}
}

func (pt Point) left() Point {
	return Point{pt.y, -pt.x}
}

func (pt Point) right() Point {
	return Point{-pt.y, pt.x}
}

func (pt Point) backward() Point {
	return Point{-pt.x, -pt.y}
}

func manhattan(pt1, pt2 Point) int {
	return tools.AbsInt(pt2.x-pt1.x) + tools.AbsInt(pt2.y-pt1.y)
}


type Brick struct {
	x0, y0, z0 int
	x1, y1, z1 int
}

func makebrick(s string) Brick {
	var nums []int
	accum := 0
	for _,c := range s {
		if tools.Isdigit(byte(c)) {
			accum = accum * 10 + int(c) - '0';
		} else {
			nums = append( nums, accum )
			accum = 0
		}
	}
	return Brick{nums[0],nums[1],nums[2],nums[3],nums[4],accum}
}

var WIDTH = -1
var HEIGHT = -1


// How far can this brick drop?  Find the tallest brick
// below us.

type Tops map[Point]int

func how_much_drop( top Tops, brick Brick ) int {
    peak := 0
    for  x := brick.x0; x <= brick.x1; x++ {
        for y := brick.y0; y <= brick.y1; y++ {
            peak = max(peak, top[Point{x,y}]);
		}
	}
    return brick.z0-peak-1
}

// Drop all the bricks that can be dropped.  We remember the
// highest brick for each x,y in `top`.  We sorted the bricks
// by z, so we're always building from bottom to top.

func countdrops( bricks []Brick, except int ) int {
    dropped := 0;
    top := make(Tops)
	for i, brick := range bricks {
        if i == except {
            continue
		}

        dz := how_much_drop(top,brick)
        if dz > 0 {
            dropped++
		}

        z1 := brick.z1 - dz

        // Register the new peak.

		for  x := brick.x0; x <= brick.x1; x++ {
			for y := brick.y0; y <= brick.y1; y++ {
				top[Point{x,y}] = z1
			}
		}
    }
    return dropped
}
            

func drop(bricks []Brick) {
    top := make(Tops)
	for i := range bricks {

        // If it can be dropped, drop it.

        dz := how_much_drop(top,bricks[i])
        bricks[i].z0 -= dz
        bricks[i].z1 -= dz

        // Register the new peak.

		brick := bricks[i]
		for  x := brick.x0; x <= brick.x1; x++ {
			for y := brick.y0; y <= brick.y1; y++ {
				top[Point{x,y}] = brick.z1
			}
		}
    }
}



func part1(bricks []Brick) (int,int) {
    sum1 := 0
    sum2 := 0

    // Eliminate all the gaps.

    drop(bricks)

    // For each brick, if we remove the brick, how many will fall?

    for i := range bricks {
        dropped := countdrops(bricks,i);
		if dropped > 0 {
			sum2 += dropped
		} else {
			sum1++
		}
    }
    return sum1, sum2
}



func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	bricks := []Brick{}
	for _,line := range strings.Split(input, "\n") {
		bricks = append( bricks, makebrick(line) )
	}

    slices.SortFunc( bricks, func( a, b Brick ) int { return a.z0 - b.z0 } )

	p1, p2 := part1(bricks)
	fmt.Println("Part 1:", p1)
	fmt.Println("Part 2:", p2)
}

