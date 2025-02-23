package tools

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Number interface {
	int | int8 | int16 | int32 | int64
}

func AbsInt[T Number](x T) T {
	return AbsDiffInt(x, 0)
}

func AbsDiffInt[T Number](x, y T) T {
	if x < y {
		return y - x
	}
	return x - y
}

// golang shock #1:  "append" modifies its parameters.
// This returns a new slice without that member.

func Remove(row []int, index int) []int {
	clone := append(row[:0:0], row...)
	return append(clone[0:index], clone[index+1:]...)
}

var DEBUG bool = false
var TEST bool = false

func Setup(test string, live string) (bool, bool, string) {
	for _, arg := range os.Args {
		if arg == "debug" {
			DEBUG = true
		}
		if arg == "test" {
			TEST = true
		}
	}

	var input string
	if TEST {
		input = test
	} else {
		input = live
	}
	return TEST, DEBUG, input
}

func Count(haystack []int, needle int) int {
	count := 0
	for _, i := range haystack {
		if i == needle {
			count += 1
		}
	}
	return count
}

func CountIf[T any](haystack []T, criteria func(T)bool) int {
	count := 0
	for _, p := range haystack {
		if criteria(p) {
			count++
		}
	}
	return count
}


// Produce a matrix of ints from the input.

func GetNumbers[T Number](input string) [][]T {
	result := make([][]T, 0)
	var row []T
	var accum T
	var sign T = 1
	last := '?'
	for _, c := range input {
		switch c {
		case '\n':
			row = append(row, sign*accum)
			result = append(result, row)
			row = make([]T, 0)
			accum = 0
			sign = 1
		case ' ', ',':
			if last != ' ' {
				row = append(row, sign*accum)
				accum = 0
				sign = 1
			}
		case '+':
			sign = 1
		case '-':
			sign = -1
		case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
			accum = accum*10 + T(c) - '0'
		default:
			if DEBUG {
				fmt.Println("Unexpected ", rune(c))
			}
		}
		last = c
	}
	if len(row) > 0 {
		result = append(result, append(row, sign*accum))
	}
	return result
}

// How does the language not already have this

func Isdigit(s byte) bool {
	return s >= '0' && s <= '9'
}

// Is val within [lo,hi)?  Uses Python concept.

func Between[T Number](lo T, val T, hi T) bool {
	return (lo <= val) && (val < hi)
}

func Repeat[T any](val T, count int) []T {
	result := make([]T, count, count)
	for i := 0; i < count; i++ {
		result[i] = val
	}
	return result
}

// Convert digits until we get a non-number.

func StrToInt(s string) int {
	accum := 0
	sign := 1
	for _, c := range s {
		if c == '+' {
			sign = 1
		} else if c == '-' {
			sign = -1
		} else if Isdigit(byte(c)) {
			accum = accum*10 + int(c) - '0'
		} else {
			break
		}
	}
	return sign * accum
}

// Convert a set of numbers to a slice.

func SplitInt(s string) []int {
	var res []int
	for _, w := range strings.Split(s, " ") {
		if len(w) == 0 || !Isdigit(byte(w[0])) {
			continue
		} else {
			res = append(res, StrToInt(w))
		}
	}
	return res
}

func SplitInt64(s string) []int64 {
	var res []int64
	for _, w := range strings.Split(s, " ") {
		if len(w) == 0 || !Isdigit(byte(w[0])) {
			continue
		} else {
			n, _ := strconv.ParseInt(w, 10, 64)
			res = append(res, n)
		}
	}
	return res
}

func Sum[T ~int](set []T) T {
	var sum T
	for _, n := range set {
		sum += n
	}
	return sum
}

// Set intersection.

func Intersect[T comparable](m1 map[T]bool, m2 map[T]bool) map[T]bool {
	newx := make(map[T]bool)
	for k := range m1 {
		if m2[k] {
			newx[k] = true
		}
	}
	return newx
}

// Python map tools.

/*
type Pair struct {
	K any
	V any
}

func Items[K comparable, V any]( m map[K]V ) []Pair {
	res := []Pair{}
	for k,v := range m {
		res = append( res, Pair{k,v} )
	}
	return res
}
*/

func Keys[K comparable, V any]( m map[K]V ) []K {
	res := []K{}
	for k,_ := range m {
		res = append( res, k )
	}
	return res
}

func Values[K comparable, V any]( m map[K]V ) []V {
	res := []V{}
	for _,v := range m {
		res = append( res, v )
	}
	return res
}

// Recursively finds and returns the greatest common divisor of a given integer.

func Gcd(a, b int64) int64 {
	if b == 0 {
		return a
	}
	return Gcd(b, a%b)
}

// Lcm returns the lcm of two numbers using the fact that lcm(a,b) * gcd(a,b) = | a * b |

func Lcm(a, b int64) int64 {
	return AbsInt(a * b / Gcd(a,b))
}



type Point struct {
	X int
	Y int
}

func (pt Point) Add(p2 Point) Point {
	return Point{pt.X + p2.X, pt.Y + p2.Y}
}

func (pt Point) Addi(dx int, dy int) Point {
	return Point{pt.X + dx, pt.Y + dy}
}

func (pt Point) Sub(p2 Point) Point {
	return Point{pt.X - p2.X, pt.Y - p2.Y}
}

func (pt Point) Left() Point {
	return Point{pt.Y, -pt.X}
}

func (pt Point) Right() Point {
	return Point{-pt.Y, pt.X}
}

func (pt Point) Back() Point {
	return Point{-pt.X, -pt.Y}
}

func Mandist( pt1, pt2 Point ) int {
	return AbsInt(pt1.X-pt2.X) + AbsInt(pt1.Y-pt2.Y)
}

func (pt Point) InRange(width int, height int) bool {
	return Between(0, pt.X, width) && Between(0, pt.Y, height)
}
