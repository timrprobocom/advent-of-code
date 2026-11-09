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
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]`[1:]

var test1 = `
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]`[1:]

//go:embed day18.txt
var live string

// Philosophy TED talk.
//
// In the Python code, we convert the whole thing to a list.  Because Python 
// allows embedded lists of varying sizes and varying types, this works. It
// doesn't work in Go.
//
// So, I convert each string to another string (essentially an array of bytes).
// Brackets and commas get values way up high.  Numbers get their own numerical
// values.

var LBR byte = '\xfa'
var RBR byte = '\xfb'
var CMA byte = '\xfc'
var LBRS string = "\xfa"
var RBRS string = "\xfb"
var CMAS string = "\xfc"

var mapchar = map[byte]byte{
	'[': LBR,
	']': RBR,
	',': CMA,
	'0': 0,
	'1': 1,
	'2': 2,
	'3': 3,
	'4': 4,
	'5': 5,
	'6': 6,
	'7': 7,
	'8': 8,
	'9': 9,
}

func encode(s string) string {
	t := make([]byte,len(s))
	for i := range len(s) {
		t[i] = mapchar[s[i]]
	}
	return string(t)
}

func decode(s string) string {
    t := ""
	for i := range len(s) {
		if s[i] == LBR {
			t = t+"["
		} else if s[i] == RBR {
			t = t+"]"
		} else if s[i] == CMA {
			t = t+","
		} else {
			t = t + fmt.Sprintf("%d", s[i] )
		}
	}
	return t
}

// Add two structures.

func add( a, b string ) string {
	if a == "" {
		return b
	}
	return LBRS+a+CMAS+b+RBRS
}

/*
func atoi(a byte) byte {
	return a-'0'
}

func itoa(a byte) byte {
	return a+'0'
}
*/


// Split the over 9 value val.

func split( txt string, n int ) string {
	if DEBUG {
		fmt.Println("splitting")
		fmt.Println(decode(txt))
		fmt.Println(strings.Repeat(" ", n-1),"^")
	}
	val := txt[n]
	sub := []byte{LBR,val/2,CMA,(val+1)/2, RBR}
	return txt[:n]+string(sub)+txt[n+1:]
}


func add_to( half string, loc int, adder byte) string {
	newx := adder + half[loc]
	sub := string(newx)
	return half[:loc]+sub+half[loc+1:]
}


// Explode the pair starting at n.
// n points to the starting bracket.

func explode( a string, n int ) string {
    if DEBUG {
		fmt.Println("exploding at", n)
		fmt.Println(decode(a))
		fmt.Println(strings.Repeat(" ", n-1),"^")
	}

	// These are bytes.

    left := a[:n]
    lval := a[n+1]
	rval := a[n+3]
	right := a[n+5:]

    // Search backwards for a digit.

    for nn := n-1; nn >= 0; nn-- {
		c := left[nn]
		if c < LBR {
			if DEBUG {
				fmt.Printf( "l adding %d to %d\n", lval, left[nn] )
			}
			left = add_to( left, nn, lval )
			break
		}
	}

    // Search forwards for a digit.

    for nn := range len(right) {
		c := right[nn]
		if c < LBR {
			if DEBUG {
				fmt.Printf( "r adding %d to %d\n", rval, right[nn] )
			}
			right = add_to( right, nn, rval )
			break
		}
	}

    // Remove the pair.

    return left + "\x00" + right
}

func testexplode() {
    testdata := []string{
        "[[[[[9,8],1],2],3],4]",
        "[7,[6,[5,[4,[3,2]]]]]",
        "[[6,[5,[4,[3,2]]]],1]",
        "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
        "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
    }
	testexpl := []int{4,12,10,10,24}

	for i := range len(testdata) {
        fmt.Println(testdata[i], "==>", decode(explode(encode(testdata[i]),testexpl[i])))
	}
}


// Take all actions.  Not sure it's documented, but we must do all
// explodes before we do a split. 

func actions( a string ) string {
    changed := true
    for changed {
        changed = false

        // Find an item of depth 4.

        depth := 0
		if DEBUG {
			fmt.Println( "start", decode(a) )
		}
        for i := range len(a) {
			c := a[i]
            if byte(c) == RBR {
                depth --
            } else if byte(c) == LBR {
                depth ++
                if depth == 5 {
                    a = explode( a, i )
                    changed = true
                    break
				}
			}
		}
		
        if changed {
            continue
		}

        // Find a number bigger than 9.

		for i := range len(a) {
			if a[i] > 9 && a[i] < LBR {
                a = split( a, i )
                changed = true
                break
			}
		}
		
		/*
        if changed {
			fmt.Println( " then", a )
		}
		*/
	}
    return a
}

func testactions() {
    s1 := encode("[[[[4,3],4],4],[7,[[8,4],9]]]")
    s2 := encode("[1,1]")
    s3 := add(s1,s2)
	fmt.Println("add:", decode(s3))
    s3 = actions( s3 )
	fmt.Println("act:", decode(s3))
}

// Return the magnitude of a structure.

func magnitude(a string) int {
	// Convert to an int array?
	
	cvt := make([]int,len(a))
	for i := range len(a) {
		if a[i] >= 250 {
			cvt[i] = -1
		} else {
			cvt[i] = int(a[i])
		}
	}

	if DEBUG {
		fmt.Println(cvt)
	}
	for len(cvt) > 1 {
		for i := range len(cvt) {
			if cvt[i] >= 0 && cvt[i+2] >= 0 {
				cvt[i-1] = cvt[i]*3 + cvt[i+2]*2
				if len(cvt) > 5 {
					cvt = append( cvt[:i], cvt[i+4:]... )
				} else {
					cvt = cvt[:i]
				}
				break
			}
		}
	}

    return cvt[0]
}


func testmagnitude() {
    testmag := []string {
        "[[1,2],[[3,4],5]]",
        "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",
        "[[[[1,1],[2,2]],[3,3]],[4,4]]",
        "[[[[3,0],[5,3]],[4,4]],[5,5]]",
        "[[[[5,0],[7,4]],[5,5]],[6,6]]",
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
	}
	testexpl := []int{ 143, 1384, 445, 791, 1137, 3488 }
	for i,a := range testmag {
        chk := magnitude(encode(a))
		b := testexpl[i]
        fmt.Println(a, chk, b)
		if chk != b {
			print("FAILURE\n")
        }
	}
}

func testing() {
    testexplode()
    testactions()
    testmagnitude()
}


func part1( data []string ) int {
    base := ""
	for _,expr := range data {
        base = add( base, encode(expr) )
		if DEBUG {
			fmt.Println("after add", decode(base))
		}
        base = actions( base )
		if DEBUG {
			fmt.Println("after reduce", decode(base))
		}
	}
    return magnitude(base)
}


// Find the best combo.
// I think we have to do this exhaustively.

func part2( data []string ) int {
    maxval := 0
    for _,a := range data {
        for _,b := range data {
            if a == b {
                continue
			}
            val := magnitude( actions( add( encode(a), encode(b) ) ) )
            if val > maxval {
                if DEBUG {
                    print(val,"\n")
				}
                maxval = val
			}
		}
	}
    return maxval

}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test1, live)
	data := strings.Split(input, "\n")

	fmt.Println( "Part 1:", part1(data) )
	fmt.Println( "Part 2:", part2(data) )
}

