package tools

import "os"
import "fmt"

func AbsInt(x int) int {
    return AbsDiffInt(x, 0)
}

func AbsDiffInt(x, y int) int {
    if x < y {
        return y - x
    }
    return x - y
}

// golang shock #1:  "append" modifies its parameters.
// This returns a new slice without that member.

func Remove( row []int, index int ) []int {
    clone := append( row[:0:0], row...)
    return append( clone[0:index], clone[index+1:]... )
}

var DEBUG bool = false
var TEST bool = false

func Setup( test string, live string ) (bool,bool,string) {
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


// Produce a matrix of ints from the input.

func Parse( input string ) [][]int {
    result := make([][]int, 0)
    var row []int
    var accum int
    sign := 1
    last := '?'
    for _, c := range input {
        switch c {
        case '\n':
            row = append( row, sign*accum )
            result = append( result, row )
            row = make([]int, 0)
            accum = 0
            sign = 1
        case ' ':
            if last != ' ' {
                row = append( row, sign*accum )
                accum = 0
                sign = 1
            }
        case '-':
            sign = -1
        case '0','1','2','3','4','5','6','7','8','9':
            accum = accum * 10 + int(c) - '0';
        default:
            if DEBUG {
                fmt.Println("Unexpected ", rune(c))
            }
        }
        last = c
    }
    if len(row) > 0 {
        result = append( result, append( row, sign*accum ) )
    }
    return result
}

// How does the language not already have this?

func Isdigit(s byte) bool {
    return s >= '0' && s <= '9';
}

// Is val within [lo,hi)?  Uses Python concept.

func Between[T ~int] (lo T, val T, hi T) bool {
    return (lo <= val) && (val < hi)
}

