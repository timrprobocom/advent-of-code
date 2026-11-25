package main

import (
	"fmt"
	"math/big"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false


var test =`
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1`[1:]

// Result: 9 2 5 8 1 4 7 0 3 6


//go:embed day22.txt
var live string

func pow(a, b, m int) int {
    result := new(big.Int).Exp(
        big.NewInt(int64(a)),
        big.NewInt(int64(b)),
        big.NewInt(int64(m)),
    )
    return int(result.Uint64())
}

// Find the multiplicative inverse in a modulus field.

// This is Euler's theorem.  This is slick, but it lively only works if
// mod is prime.  The first line computes the "totient" of the modulus,
// which is mod-1 if mod is prime, but requires prime factoring otherwise.
// The test case uses mod 10 which, of course, is not prime.  We hardcode 
// the totient for 10 to allow the test to work.

func invert_euler(n int, mod int) int {
	tot := mod - 1
	if mod == 10 {
		tot = 4
	}
    return pow(n, tot-1, mod)
}

// This is the Extended Euclidean Algorithm.  It does not care about the
// totient.  It does, however, fail if a is negative, so we compensate.
// It is basically doing a GCD.

func invert_euclid(a, n int) int {
    t := 0 
	newt := 1
    r := n
	newr := a
	if a < 0 {
		newr += n
	}

    for newr > 0 {
        q := r / newr

		tmp := t - q * newt
		t = newt
		newt = tmp

		tmp = r - q * newr
		r = newr
		newr = tmp
	}
    if r > 1 {
        fmt.Println( a, "is not invertable mod", n )
        return -1
	}
    if t < 0 {
        t += n
	}
    return t
}

var invert = invert_euclid

// A deck can be encoded as ax+b mod n.

type Deck struct {
	count int
	state0 int
	state1 int
}

func MakeDeck(k int) *Deck {
	return &Deck{k,0,1}
}

func (self *Deck) cut( n int ) {
	off := (self.state0 + self.state1 * n) % self.count
	self.state0 = off
}

func (self *Deck) reverse() {
	inc := -self.state1 
	self.state0 = tools.Mod((self.state0+inc+self.count), self.count)
	self.state1 = inc
}

func (self *Deck) increment(n int) {
	inc := tools.Mod(self.state1 * invert(n, self.count), self.count)
	self.state1 = inc
}

func (self *Deck) run( src []string ) {
	for _, ln := range src {
		ln = strings.TrimSpace(ln)
		if DEBUG {
			fmt.Println( ln )
		}
		words := strings.Fields(ln)
		if words[0] == "cut" {
			self.cut( tools.StrToInt(words[1]) )
		}
		if words[1] == "with" {
			self.increment( tools.StrToInt(words[3]) )
		}
		if words[1] == "into" {
			self.reverse()
		}
		if DEBUG {
			fmt.Println( *self )
		}
	}
}

// Do a part 1 test.  Should be 9 2 5 8 1 4 7 0 3 6, or 9+3x.

func part1test(data []string) string {
    COUNT := 10
    deck := MakeDeck(COUNT)
    deck.run( data )
    fmt.Println( *deck )
	b := deck.state0
	m := deck.state1
	out := []byte{}
    for x := range COUNT {
		out = append(out, '0'+byte(tools.Mod(m*x+b, COUNT)))
		out = append(out, ' ')
	}
    return string(out)
}

// Do part 1.  Should be 4775.

func part1(data []string) int {
    COUNT := 10007

    deck := MakeDeck(COUNT)
    deck.run( data )
    if DEBUG {
        fmt.Println( *deck )
	}
	b := deck.state0
	m := deck.state1

    for x := range COUNT {
        if (m*x+b) % COUNT == 2019 {
            return x
		}
	}
	return -1
}

// Do part 2.  Shouild be 37889219674304.

func part2(data []string) int {
    COUNT := 119315717514047

    deck := MakeDeck(COUNT)
    deck.run( data )
    if DEBUG {
        fmt.Println( *deck )
	}
	b := deck.state0
	m := deck.state1

// So, each cycle through will do
// bn = mn * b
// mn = m
// So it's a geometric series.  b x (1-m^cycles) / (1-m).
// The formula comes from Wikipedia.  There's magic to do
// exponentiation and inversion in a modulus field.

    cycles := 101741582076661
    finalm := pow( m, cycles, COUNT )
    finalb := tools.Mod((b * (1 - finalm) * invert(1 - m, COUNT)),  COUNT)
    if DEBUG {
        fmt.Println(finalm,finalb)
	}

    tgt := 2020
    return (finalm * tgt + finalb) % COUNT
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(strings.TrimSpace(input), "\n")

    if TEST {
		fmt.Println( "Part 1:", part1test(data))
		return
	}

	fmt.Println( "Part 1:", part1(data))
	fmt.Println( "Part 2:", part2(data))
}
