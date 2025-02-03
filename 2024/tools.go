package main

func absInt(x int) int {
	return absDiffInt(x, 0)
}

func absDiffInt(x, y int) int {
	if x < y {
		return y - x
	}
	return x - y
}

// golang shock #1:  "append" modifies its parameters.

func remove( row []int, index int ) []int {
    clone := append( row[:0:0], row...)
    return append( clone[0:index], clone[index+1:]... )
}

func setup() string {
    for _, arg := range os.Args {
        if arg == "debug" {
            DEBUG = true
        }
        if arg == "test" {
            TEST = true
        }
    }

    if TEST {
        return test
    } else {
        return live
    }
}

// Produce a matrix of ints from the input.

func parse( input string ) [][]int {
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
            print("Unexpected ", c)
        }
        last = c
    }
    if len(row) > 0 {
        result = append( result, append( row, sign*accum ) )
    }
    return result
}
