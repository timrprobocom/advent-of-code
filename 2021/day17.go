package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

// test = "target area: x=20..30, y=-10..-5"
var test = []int{20,30,-10,-5}

// live = "target area: x=156..202, y=-110..-69"
var live = []int{156,202,-110,-69}

type Point = tools.Point


func sgn(x int) int {
	if x < 0 {
		return -1
	} else if x > 0 {
		return 1
	}
	return 0
}


// At each step
//x velocity step by 1 towards 0
//y velocity decreases by 1

func launch( data []int, vel Point ) int {
	pos := Point{0,0}
    maxy := 0
    for true {
		pos = pos.Add(vel)
        if DEBUG {
            fmt.Println(pos)
		}
		if tools.Between(data[0], pos.X, data[1]+1) && tools.Between(data[2], pos.Y, data[3]+1) {
            return maxy
		}
		if pos.X > data[1] || pos.Y < data[2] {
            break
		}
        maxy = max(maxy, pos.Y)
		vel.X -= sgn(vel.X)
		vel.Y -- 
	}
	return -1
}


func part1( data []int ) (int,int) {

	// What's the minimum X velocity?

	minx := 0
	mustx := data[0]
	for mustx > 0 {
		minx += 1
		mustx -= minx
	}

    maxdata := 0
    count := 0
	for vy := data[2]; vy < -data[2]; vy++ {
		for vx := minx; vx < data[1]+1; vx++ {
            vel := Point{vx,vy}
            if DEBUG {
                fmt.Println("*****", vel )
			}
            mx := launch( data, vel )
            if mx >= 0 {
                count ++
                if mx > maxdata {
                    if DEBUG {
                        fmt.Println(vel, mx)
					}
                    maxdata = mx
				}
			}
		}
	}
    return maxdata, count
}

func main() {
	var input []int
	TEST, DEBUG, input = tools.Setup(test, live)

	// Part 1 with math.  When aiming up, you will always come back to y=0
	// with vy = -vy0, and the max will hit the bottom of the zone at the
	// next step.  So, if bottom of the box is -10, you need initial
	// velocity 9, and the highest is sum(1..9), which is y1(y1+1)/2.

	fmt.Println( "Math 1:", input[2]*(input[2]+1)/2)

	p1, p2 := part1(input)
	fmt.Println( "Part 1:", p1 )
	fmt.Println( "Part 2:", p2 )

}

