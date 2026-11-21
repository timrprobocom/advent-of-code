package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>`[1:]

var test2 = `
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>`[1:]

//go:embed day12.txt
var live string

var abs = tools.AbsInt[int]

// moon position (x,y,z)
// First apply gravity to update velocity
// Then update position by applying velocity
// First/second derivatives.
//
// Gravity:
//   Each velocity bumps by +1/-1
// 

type Point3 struct {
	x	int
	y	int
	z	int
}

func (self *Point3) add( other *Point3 ) {
	self.x += other.x
	self.y += other.y
	self.z += other.z
}

func (self *Point3) axis( i int ) int {
	switch i {
		case 0:
			return self.x
		case 1:
			return self.y
		case 2:
			return self.z
	}
	return -1
}


func (self *Point3) repr() string {
	return fmt.Sprintf("%d,%d,%d", self.x, self.y, self.z )
}

type Moon struct {
	pos		*Point3
	vel		*Point3
}

func (self Moon) applyVelocity() {
	self.pos.add( self.vel )
}

func (self Moon) pot() int {
	return abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)
}

func (self Moon) kin() int {
	return abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)
}

func (self Moon) Print() {
	fmt.Printf( "pos(%s) vel(%s)\n", self.pos.repr(), self.vel.repr() )
}

func cmp( a, b int ) int {
	if a < b {
		return -1
	} else if a > b {
		return 1
	}
	return 0
}

func compare( a, b *Point3 ) *Point3 {
	return &Point3 {
		cmp(a.x, b.x),
		cmp(a.y, b.y),
		cmp(a.z, b.z),
	}
}

func makemoons( text string ) []Moon {
	moons := []Moon{}
	for _,row := range tools.GetNumbers[int](text) {
		moons = append( moons, Moon{ &Point3{row[0],row[1],row[2]}, &Point3{0,0,0} } )
	}
	return moons
}

// Part 1

func energy( system []Moon ) int {
	sum := 0
	for _,m := range system {
		sum += m.pot() * m.kin()
	}
	return sum
}

func step( system []Moon ) {
    // Apply gravity.
	for i := range len(system) {
		for j := i+1; j < len(system); j++ {
			m1 := system[i]
			m2 := system[j]
			m1.vel.add( compare(m2.pos, m1.pos) )
			m2.vel.add( compare(m1.pos, m2.pos) )
		}
	}
    // Apply velocity.
	for _,m1 := range system {
		m1.applyVelocity()
	}
}

func part1( system []Moon, n int ) int {
    if DEBUG {
        for _,m1 := range system {
			m1.Print()
		}
	}
    for range n {
        step( system )
	}
    return energy( system )
}


// Part 2.

// We answer the musical question, are all of the velocities
// zero in this one axis?

func isAxisZero(system []Moon, axis int) bool {
	for _,m := range system {
		if m.vel.axis(axis) != 0 {
			return false
		}
	}
	return true
}

func lcm( x,y int ) int {
    return x * y / tools.Gcd(x,y)
}

func lcm3( x,y,z int ) int {
    return lcm(lcm(x,y),z)
}

// This is my third algorithm.  The velocities all reach zero at
// the halfway point, so we can look for that without tracking the
// previous positions.  This is 60% faster.

func findrepeat( system []Moon ) Point3 {
    found := Point3{0,0,0}
    step(system)
    nstep := 1
	for found.x == 0 || found.y == 0 || found.z == 0 {
        for axis := range 3 {
            if found.axis(axis) == 0 && isAxisZero(system,axis) {
                if DEBUG {
                    fmt.Println("Found",axis,"at",nstep)
				}
				switch axis {
					case 0:
					found.x = nstep*2
					case 1:
					found.y = nstep*2
					case 2:
					found.z = nstep*2
				}
			}
		}
        step(system)
        nstep += 1
	}

    return found
}

func part2( data []Moon ) int {
    cycles := findrepeat( data )
    if DEBUG {
        fmt.Println( cycles, lcm3(cycles.x, cycles.y, cycles.z) )
	}
    return lcm3(cycles.x, cycles.y, cycles.z)
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test,live)
	count := 1000
	if TEST {
		count = 10
	}
	fmt.Println( "Part 1:", part1(makemoons(input), count))
	fmt.Println( "Part 2:", part2(makemoons(input)))
}
