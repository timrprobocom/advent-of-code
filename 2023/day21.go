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
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........`[1:]

//go:embed day21.txt
var live string


type Point = tools.Point

var N Point = Point{0, -1}
var E Point = Point{1, 0}
var S Point = Point{0, 1}
var W Point = Point{-1, 0}

var WIDTH = -1
var HEIGHT = -1

var origin Point
            
func printgrid( s map[Point]bool, d Point ) int {
	sum := 0
	var grid [][]byte
	for range HEIGHT {
		grid = append(grid, tools.Repeat(byte('.'), WIDTH))
	}

    for pt := range s {
		npt := pt.Sub(d)
		if npt.InRange(WIDTH, HEIGHT) {
			sum++
            grid[npt.Y][npt.X] = 'O'
		}
	}
	for _,row := range grid {
		fmt.Println( string(row) )
    }
    fmt.Println(sum)
    return sum
}
            
func countgrid( s map[Point]bool, d Point ) int {
    sum := 0
	for pt := range s {
		npt := pt.Sub(d)
		if npt.InRange(WIDTH, HEIGHT) {
            sum++
		}
	}
    return sum
}

func part1(rocks map[Point]bool) int {
	steps := 64
	if TEST {
		steps = 6
	}
	queue := make(map[Point]bool)
	queue[origin] = true
	for range steps {
		newq := make(map[Point]bool)
		for pt := range queue {
			for _, delta := range []Point{N,E,W,S} {
				npt := pt.Add(delta)
				if npt.InRange(WIDTH, HEIGHT) && !rocks[npt] {
					newq[npt] = true
				}
			}
		}
        queue = newq
	}
    return len(queue)
}


// Once we get past an initial start up time, The number of cells at
// each multiple of the grid width, is quadratic.  If the 2nd derivative
// is N, then the first derivative is k
//  f''(x) = N
//  f'(x)  = Nx + b
//  f(x)   = (N/2)x**2 + bx + c
//
// If you look up how to derive a quadratic from differences, you'll find
//  a = d2[0]/2
//  b = d1[0] - 3a
//  c = d0[0] - a - b
// Oddly, this starts counting with 1, so we have to compensate for that.
//
// We gather the counts where (step % width) == (steps % width), so we're
// always at the same point in the cycle.  Note that the offset is where
// the S is, so we're sampling just as we reach the edge of a grid.
//
// It takes about 45 seconds to compute enough differences to ensure
// we know the second differences have stabilized.

func part2( rocks map[Point]bool ) int {
    steps := 26501365
	if TEST {
		steps = 5000
	}
    offset := steps % WIDTH

    queue := make(map[Point]bool)
	queue[origin] = true
    var nums  []int
    var diff1  []int
    var diff2  []int

    for i := range steps {
        if i % WIDTH == offset {
			nums = append( nums, len(queue) )
            if len(nums) > 1 {
				diff1 = append( diff1, nums[len(nums)-1] - nums[len(nums)-2] )
			}
            if len(diff1) > 1 {
				diff2 = append( diff2, diff1[len(diff1)-1] - diff1[len(diff1)-2] )
			}
            if DEBUG {
                fmt.Println(i,nums,diff1,diff2)
			}
            if len(diff2) > 1 && diff2[len(diff2)-1] == diff2[len(diff2)-2] {
                break
			}
		}
        newq := make(map[Point]bool)
        for pt := range queue {
			for _, delta := range []Point{N,E,W,S} {
				npt := pt.Add(delta)
				nptm := Point{ tools.Mod(npt.X, WIDTH), tools.Mod(npt.Y, HEIGHT)}
				if !rocks[nptm] {
					newq[npt] = true
				}
			}
		}
        queue = newq
	}
    
    // Use the first and second differences to find the quadratic
    // coefficients.

    skips := len(nums) - 4
    a := diff2[skips] / 2
    b := diff1[skips] - 3 * a
    c := nums[skips] - a - b
    n := steps/WIDTH-skips+1
    if DEBUG {
		printgrid(rocks, Point{0,0})
		printgrid(queue, Point{0,0})
        fmt.Println(skips,a,b,c,n)
	}
    return (a * n + b) * n + c
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := strings.Split(input, "\n")
	WIDTH = len(data[0])
	HEIGHT = len(data)

    rocks := make(map[Point]bool)
	for y,row := range data {
		for x,c := range row {
			if c == 'S' {
				origin = Point{x,y}
			} else if c == '#' {
				rocks[Point{x,y}] = true
			}
		}
	}

	// 40 rocks in test
	// 2290 rocks in real
	if DEBUG {
		fmt.Println(len(rocks),"rocks")
	}

	fmt.Println("Part 1:", part1(rocks))
	fmt.Println("Part 2:", part2(rocks))
}

