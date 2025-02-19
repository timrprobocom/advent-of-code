package main

import (
	"fmt"
	"math"
	"strings"
	"gonum.org/v1/gonum/mat"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3`[1:]

//go:embed day24.txt
var live string

type Point3D struct {
	x int64
	y int64
	z int64
}


type Vector struct {
	pos Point3D
	dt Point3D
}

func makeVector( line string ) Vector {
	acc := tools.SplitInt64(line)
	return Vector{
		Point3D{acc[0], acc[1], acc[2]},
		Point3D{acc[3], acc[4], acc[5]},
	}
}

func (pt Point3D) add(p2 Point3D) Point3D {
	return Point3D{pt.x + p2.x, pt.y + p2.y, pt.z + p2.z}
}

func (pt Point3D) sub(p2 Point3D) Point3D {
	return Point3D{pt.x - p2.x, pt.y - p2.y, pt.z - p2.z}
}

func (pt Point3D) addi(dx int64, dy int64, dz int64) Point3D {
	return Point3D{pt.x + dx, pt.y + dy, pt.z + dz}
}

func (pt Point3D) times(f int64) Point3D {
	return Point3D{pt.x*f, pt.y*f, pt.z*f}
}

func (pt Point3D) asSlice() []int64 {
	return []int64{pt.x,pt.y,pt.z}
}

func (pt Point3D) asFloatSlice() []float64 {
	return []float64{float64(pt.x), float64(pt.y), float64(pt.z)}
}

func (pt Point3D) asVector() mat.Vector {
	return mat.NewVecDense( 3, pt.asFloatSlice() )
}

func (r Vector) at( t int64 ) Point3D {
//	return r.pos.add(r.dt.times(t))
    return Point3D{
		r.pos.x + r.dt.x * t,
		r.pos.y + r.dt.y * t,
		r.pos.z + r.dt.z * t,
	}
}

func (r Vector) clone() Vector {
	return Vector{
		Point3D{ r.pos.x, r.pos.y, r.pos.y },
		Point3D{ r.dt.x, r.dt.y, r.dt.z },
	}
}

func (v Vector) find_mbx() (float64, float64) {
	return find_mbx(v.pos.x,v.pos.y,v.dt.x,v.dt.y)
}

func (r Vector) __repr__() string {
	return fmt.Sprint("<P3D", r.pos, "delta=", r.dt, ">")
}

var WIDTH = -1
var HEIGHT = -1



// This finds a line equation for a vector.

func find_mbx( x0, y0, dx, dy int64) (float64, float64) {
    m := float64(dy)/float64(dx)
    b := float64(y0) - m * float64(x0)
    return m,b
}

// This finds the intersection of two 3D lines in mx+b form.

func intersect2d( p1m, p1b, p2m, p2b float64) (int64,int64) {
    // Are the lines parallel?
    if p1m == p2m {
        return 0,0
	}
    x := int64(math.Round((p2b-p1b)/(p1m-p2m)))
    y := int64(math.Round(p1m*float64(x)+p1b))
    return x,y
}

// This asks, would this intersection happen in the future?

func in_the_future( pt1 Vector, x int64, y int64 ) bool {
    return (pt1.dt.x < 0) == (x < pt1.pos.x)
}




func part1( vectors []Vector ) int64 {
	var rmin int64 = 2E14
	var rmax int64 = 4E14
	if TEST {
		rmin, rmax = 7,20
	}
    var count int64 = 0
	for i,pt0 := range vectors {
        p1m,p1b := pt0.find_mbx()
		for _, pt1 := range vectors[i+1:] {
            p2m,p2b := pt1.find_mbx()
            x,y := intersect2d(p1m,p1b,p2m,p2b)
            if in_the_future(pt0,x,y) && in_the_future(pt1,x,y) {
				if tools.Between(rmin, x, rmax+1) && tools.Between(rmin, y, rmax+1) {
					count++
				}
			}
		}
	}
    return count
}

// Find the velocity of the rock.

// Here's an explanation, as best as I can.
//
// Call the rock's location r, and it's velocity dr.  For every hailstone s, 
// there must be a time t so that
//   r + dr*t = s * ds*t
// Which means
//   r = s + (ds-dr) * t
// That means if we shift our framework relative to the rock's velocity,
// every ray passes through that point r.  That makes for some nice triangles.
//
// That means that the vectors (s2-s1), (ds1-dr) and (ds2-dr) are all coplanar,
// in the plane of the triangle that contains s1, s2, and r.  (The two velocity
// vectors don't make up the other legs, but they are in the same direction.)
// This is where I went wrong with my first analysis -- I was using vectors
// that were not coplanar.
//
// By rearranging, it also means that (s2-s1), (ds1-ds2), and (ds2-dr) are 
// coplanar.  If we look up the Wikipedia definition of a "triple scalar
// product", we find definitions that let us construct a system of three
// linear equations that produce dr.
//
// Believe it or not.


// It's a shame the gonum is auch a piece of crap that I have to do these here.

func dotproduct( p1 Point3D, p2 Point3D ) int64 {
    return p1.x * p2.x + p1.y * p2.y + p1.z * p2.z
}

func crossproduct( p1 Point3D, p2 Point3D ) Point3D  {
	return Point3D{
		p1.y * p2.z - p1.z * p2.y,
		p1.z * p2.x - p1.x * p2.z,
		p1.x * p2.y - p1.y * p2.x,
	}
}

func find_rock_velocity( vectors []Vector ) Point3D {
    p1 := vectors[0]
    p2 := vectors[1]
    p3 := vectors[2]
	s1 := crossproduct(p1.pos.sub(p2.pos), p1.dt.sub(p2.dt) )
	s2 := crossproduct(p2.pos.sub(p3.pos), p2.dt.sub(p3.dt) )
	s3 := crossproduct(p3.pos.sub(p1.pos), p3.dt.sub(p1.dt) )
	e1 := float64(dotproduct( s1, p2.dt ))
	e2 := float64(dotproduct( s2, p3.dt ))
	e3 := float64(dotproduct( s3, p1.dt ))

	sys := mat.NewDense(3, 3, []float64{
		float64(s1.x), float64(s1.y), float64(s1.z),
		float64(s2.x), float64(s2.y), float64(s2.z),
		float64(s3.x), float64(s3.y), float64(s3.z),
	})

	equals := mat.NewDense(3, 1, []float64{e1, e2, e3})
    if DEBUG {
        fmt.Println(sys)
		fmt.Println(equals)
	}
	var res mat.Dense
	if res.Solve(sys, equals) != nil {
		panic( "Solution did not solve.")
	}
	a1 := int64(math.Round(res.At(0, 0)))
	a2 := int64(math.Round(res.At(1, 0)))
	a3 := int64(math.Round(res.At(2, 0)))
	return Point3D{a1,a2,a3}
}

// Given the velocity of the rock, find the initial position.

// As above, we warp space by shifting the reference frame so that the rock's 
// velocity is zero.  That way, all of the hailstones will pass through a 
// single point.  If we can find the point where two of the hailstones
// cross, since the rock's velocity is zero, that must be the point where
// the rock started.

// It's not easy to find the intersection of two 3D lines, but if the vectors
// intersect in 2D (and we know how to do that), it's pretty safe to assume 
// they cross in 3D.

func find_rock_posisition( vectors []Vector, drock Point3D ) Point3D {
    p1 := vectors[0]
    p2 := vectors[1]
    p1.dt = p1.dt.sub(drock)
    p2.dt = p2.dt.sub(drock)

    p1m,p1b := find_mbx(p1.pos.x, p1.pos.y, p1.dt.x, p1.dt.y)
    p2m,p2b := find_mbx(p2.pos.x, p2.pos.y, p2.dt.x, p2.dt.y)

    // So, hailstones 0 and 1 intersect in x, y here:
    x,y := intersect2d(p1m,p1b,p2m,p2b)

    // At these times:
    ta := int64((x - p1.pos.x) / p1.dt.x)
    tb := int64((x - p2.pos.x) / p2.dt.x)
	if DEBUG {
		fmt.Println("p1",p1,"p2",p2,"x,y",x,y,"ta,tb",ta,tb)
	}

    // And what is that location in 3D?
    return p1.at(ta)
}


func part2( vectors []Vector ) int64 {
    drock := find_rock_velocity(vectors)
    prock := find_rock_posisition(vectors, drock)
    return prock.x + prock.y + prock.z
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	var vectors []Vector
	for _, row := range strings.Split(input, "\n") {
		vectors = append(vectors, makeVector(row))
	}

	fmt.Println("Part 1:", part1(vectors))
	fmt.Println("Part 2:", part2(vectors))
}

