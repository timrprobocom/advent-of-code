package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed test19.txt
var test string

//go:embed day19.txt
var live string


type Point3d struct {
	x int
	y int
	z int
}

func sub( pta, ptb Point3d ) Point3d {
    return Point3d{pta.x-ptb.x, pta.y-ptb.y, pta.z-ptb.z}
}

func add( pta, ptb Point3d ) Point3d {
    return Point3d{pta.x+ptb.x, pta.y+ptb.y, pta.z+ptb.z}
}

func mandist( pta, ptb Point3d ) int {
	return  tools.AbsInt(pta.x - ptb.x) + 
			tools.AbsInt(pta.y - ptb.y) + 
			tools.AbsInt(pta.z - ptb.z)
}

func rotatex(pt Point3d) Point3d {
	return Point3d{pt.x, pt.z, -pt.y}
}

func rotatey(pt Point3d) Point3d {
	return Point3d{pt.z, pt.y, -pt.x}
}

func rotatez(pt Point3d) Point3d {
	return Point3d{-pt.y, pt.x, pt.z}
}

// This returns a vector of the 24 possible rotations of this point.
// Move the "facing" direction through all 6 points, then rotate around
// that axis four times.

func (point Point3d) allrotate() []Point3d {
	out := []Point3d{}
	for _,direction := range []func(Point3d)Point3d{
        rotatex, rotatex, rotatex, rotatez, // now pointing up / down
        rotatey, rotatey, rotatey, rotatex, // now pointing back / front
        rotatez, rotatez, rotatez, rotatey, // now pointing left / right
        rotatex, rotatex, rotatex, rotatez, // now pointing up / down
        rotatey, rotatey, rotatey, rotatex, // now pointing back / front
        rotatez, rotatez, rotatez, rotatey, // now pointing left / right
	} {
		out = append(out, point)
		point = direction(point)
	}

	return out
}



func makeScanners( data []string ) [][]Point3d {
	scanners := [][]Point3d{}
	row := []Point3d{}
	for _,ln := range data {
		if len(ln) > 0 {
			if ln[:3] == "---" {
				if len(row) > 0 {
					scanners = append( scanners, row )
				}
				row = []Point3d{}
			} else {
				parts := strings.Split(ln, ",")
				pt := Point3d{
					tools.StrToInt(parts[0]),
					tools.StrToInt(parts[1]),
					tools.StrToInt(parts[2]),
				}
				row = append( row, pt )
			}
		}
	}
	return append( scanners, row )
}


// This function answers the musical question, for each pair of points
// in the two scan lists, if they lined up, how many other points would
// line up?

func find_matches( scan1, scan2 []Point3d ) (bool, Point3d) {
	set1 := make(map[Point3d]bool)
	for _,pt1 := range scan1 {
		set1[pt1] = true
	}

    for _,pt1 := range scan1 {
        for _,pt2 := range scan2 {
            delta := sub(pt2,pt1)

			inter := 0
			for _,pt2x := range scan2 {
				if set1[sub(pt2x,delta)] {
					inter ++
				}
			}
			if inter >= 12 {
				if DEBUG {
					fmt.Println( "delta", delta, "results in",inter)
				}
				return true, delta
			}
		}
	}
	return false, Point3d{}
}


type Placement struct {
	rot   int
	point Point3d
}

func process( scanners [][]Point3d ) (map[Point3d]bool, map[int]Placement) {
    // Make all rotations of all scanner readings.
    // This is an Nx24x25 array (N scanners, 25/26 readings, 24 rotations).

    rotations := [][][]Point3d{}
	for _,scanner := range scanners {
		perrotate := make([][]Point3d, 24)
		for i := range len(perrotate) {
			perrotate[i] = make([]Point3d, len(scanner))
		}

		for i,pt := range scanner {
			for j,rot := range pt.allrotate() {
				perrotate[j][i] = rot
			}
		}

		rotations = append(rotations, perrotate)
	}

    // This is the set of known beacons.

	beacons := make(map[Point3d]bool)
	for _,pt := range rotations[0][0] {
		beacons[pt] = true
	}

	placed := make(map[int]Placement)
	placed[0] = Placement{}

    for len(placed) < len(rotations) {
		// For each scanner except 0...
        for i, scan1 := range rotations {
			_, ok := placed[i]
			if ok {
				continue
			}
            escape := false

            // scan1 is our candidate scanner.

            for j, placement := range placed {
				rot2 := placement.rot
				pt2 := placement.point

                scan2 := rotations[j][rot2]

                // scan2 is a scanner whose position and rotation is now known.

                for possrot := range 24 {

                    // Does this rotation of scan1 line up with scan2?

                    ok, result := find_matches( scan2, scan1[possrot] )
                    if ! ok {
                        continue
					}
                    if DEBUG {
                        fmt.Println( "Matched", i, "rot", possrot, "vs", j )
					}

                    // We have a winner.  Add this to the set of knowns.
                    // We shift scan1 to match the coords of scan2, then
                    // shift that to our master coords.

					for _,pt := range scan1[possrot] {
						px := sub(sub(pt,result),pt2)
						beacons[px] = true
					}

                    placed[i] = Placement{ possrot, add(result, pt2) }
                    escape = true
                    break
				}

                if escape {
                    break
				}
			}
		}
	}

    return beacons, placed
}


func part1( beacons map[Point3d]bool ) int {
    return len(beacons)
}


func part2( placed map[int]Placement) int {
    places := tools.Values(placed)
    // Find the largest distance between any two scanners (not beacons).
    maxx := 0
    for _,pt0 := range places {
        for _,pt1 := range places {
            maxx = max( maxx, mandist(pt0.point,pt1.point) )
		}
	}
    return maxx
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	scanners := makeScanners(data)
	beacons, placed := process(scanners)

	fmt.Println( "Part 1:", part1(beacons) )
	fmt.Println( "Part 2:", part2(placed) )
}

