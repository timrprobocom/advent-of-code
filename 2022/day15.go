package main

import (
	"os"
	"fmt"
	"runtime/pprof"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day15.txt
var live string

var test = `
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3`[1:]

type Point = tools.Point

type Sensor struct {
	S 		Point
	B 		Point
	Reach 	int
}

func makeSensor( coords []int ) *Sensor {
	sensor := Point{coords[0],coords[1]}
	beacon := Point{coords[2],coords[3]}
	return &Sensor{
		S: sensor,
		B: beacon,
		Reach: tools.Mandist( sensor, beacon ),
	}
}

func (s Sensor) Within( pt Point ) bool {
	return tools.Mandist( pt, s.S ) <= s.Reach
}

func part1( data []*Sensor, target int) int {

	// There's only one beacon at the target Y.  We don't need to count them.

	rangelo := target;
	rangehi := target;

    for _,s := range data {
        fromtgt := tools.AbsInt (target-s.S.Y)

        // So, from 8,7 to 2,10 distance is 9
        //   7:-1 to 17  19
        //   8: 0 to 16  17
        //   9: 1 to 15  15
        //  10: 2 to 14  13
        //  11: 3 to 13  11
        //  12: 4 to 12  9

        if s.Reach < fromtgt {
            continue
		}
        
        x00 := s.S.X - s.Reach + fromtgt
        x99 := s.S.X + s.Reach - fromtgt
        if DEBUG {
            fmt.Println(s.S.X,s.S.X,s.B.X,s.B.Y,s.Reach,x00,x99)
		}
		// Turns out this doesn't matter.
		if DEBUG && (x99 < rangelo  ||  x00 > rangehi) {
			fmt.Println( x00, x99, "discontiguous" )
		} 
		rangelo = min(x00,rangelo)
		rangehi = max(x99,rangehi)
	}
	return rangehi - rangelo
}

func part2( data []*Sensor, target int) int64 {

// This one runs instantaneously.  If we draw a line parallel to each
// surface of the diamonds but one pixel out, then the unseen beacon 
// will be at an intersection of four of those lines.  Handling these
// lines is easy, because the slope is either +1 or -1.

    type Line struct {
		Slope int
		Yint int
	}

    lines := make(map[Line]int)
    for _,s := range data {

        // The values here are m and b for y=mx+b.

        nw := Line{ 1, s.S.Y - s.Reach - 1 - s.S.X }
        ne := Line{-1, s.S.Y - s.Reach - 1 + s.S.X }
        se := Line{ 1, s.S.Y + s.Reach + 1 - s.S.X }
        sw := Line{-1, s.S.Y + s.Reach + 1 + s.S.X }

		lines[nw]++
		lines[ne]++
		lines[sw]++
		lines[se]++
	}

    // To be the spot, we need 4 lines to intersect.  Thus, there
    // will be two with +1 slope and two with -1 slope.  So, only keep
    // the duplicates.

    slopes := map[int][]int { 1: []int{}, -1: []int{} }
    for line,count := range lines {
        if count > 1 {
            slopes[line.Slope] = append(slopes[line.Slope], line.Yint)
		}
	}

    // All the lines have slope of 1 or -1 so intersection is easy.
    // +x + b0 == -x + b1 so 2x = b1 - b0.

    for _,up := range slopes[1] {
        for _,dn := range slopes[-1] {
            x := (dn - up) / 2
            y := x + up
			if !tools.Between( 0, x, target+target) ||
				!tools.Between( 0, y, target+target) {
				continue
			}

			// Pick this one if there is no sensor that can
			// reach this point.

			winner := false
			for _,s := range data {
				winner = winner || s.Within(Point{x,y})
			}
			if !winner {
                return int64(x) * 4000000 + int64(y)
 		    }
		}
	}

    return -1
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := []*Sensor{}
	for _,row := range tools.GetNumbers[int](input) {
		data = append(data, makeSensor(row))
	}

	target := 2000000
	if TEST {
		target = 10
	}
	if false {
		f,_ := os.Create("cpu.pprof")
		defer f.Close()
		pprof.StartCPUProfile(f)
		defer pprof.StopCPUProfile()
	}

	fmt.Println("Part 1:", part1(data,target))
	fmt.Println("Part 2:", part2(data,target))
}

