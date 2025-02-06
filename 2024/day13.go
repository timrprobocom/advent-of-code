package main

import (
	"fmt"
	"strings"

  	"gonum.org/v1/gonum/mat"
	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test string = `
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279`[1:]

//go:embed day13.txt
var live string

// Convert until we can't no more.

func stol( s string ) int {
	sign := 1
	accum := 0
	for _,c := range s {
		switch c {
			case '-':
				sign = -1
			case '+':
				sign = +1
			case '0','1','2','3','4','5','6','7','8','9':
				accum = accum * 10 + int(byte(c)) - '0'
			default:
				return sign * accum
		}
	}
	return sign * accum
}

func part1(data [][]int) int64 {
	var sum int64 = 0
	for _, game := range data {
        ax := game[0]
        ay := game[1]
        bx := game[2]
        by := game[3]
        px := game[4]
        py := game[5]

        for a := 1; a < px/ax; a++ {
            if (px - a * ax) % bx == 0 {
                b := (px - a * ax) / bx;
                if ay*a + by*b == py {
                    sum += int64(a * 3 + b)
                    break
                }
            }
        }
    }
    return sum
}

func part2(data [][]int, offset int64) int64 {
	var sum int64 = 0
	for _, game := range data {
        ax := int64(game[0])
        ay := int64(game[1])
        bx := int64(game[2])
        by := int64(game[3])
        px := int64(game[4])+offset
        py := int64(game[5])+offset

        // We are setting up the equations:
        //   ax*x + bx*y = px
        //   ay*x + by*y = py

	    sys := mat.NewDense( 2, 2, []float64{
			float64(ax), float64(bx),
			float64(ay), float64(by),
		})

		equals := mat.NewDense( 2, 1, []float64{
			float64(px), float64(py),
		})

        // If the solution is not integral, there is no solution.

        var res mat.Dense
		if res.Solve( sys, equals ) == nil {
			a := int64( res.At(0,0) + 0.5 )
			b := int64( res.At(1,0) + 0.5 )
			if a*ax+b*bx == px && a*ay+b*by == py  {
				sum += a *3 + b;
			}
		}
    }
    return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	var data [][]int
	var row []int
	for _, line := range strings.Split(input, "\n") {
		if len(line) == 0 {
			data = append( data, row )
			row = nil
			continue
		}
		
		i := strings.Index( line, "X" )
		j := strings.Index( line, "Y" )
		if line[i+1] == '=' {
			i++
			j++
		}
		row = append( row, stol(line[i+1:]) )
		row = append( row, stol(line[j+1:]) )
	}
	data = append(data, row)

	if DEBUG {
		fmt.Println(data)
	}

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data,0))
	fmt.Println("Part 2:", part2(data,1e13))
}
