package tools

import (
	"fmt"
	"slices"
)

// The IntCode computer.

var TRACE = false
var count = 0

type Program struct {
	id	int
	pgm	[]int
	pc  int
	input  chan int
	output chan int
	rbase int
	die   bool
	modes int
	final int
}

// How do we shut down the channels?

func makeProgram( program []int, inputs []int) *Program {
	pgm := Program{}
	pgm.id = count
	count++
	pgm.pgm = slices.Clone( program )
	pgm.input = make(chan int)
	pgm.output = make(chan int)
	for _,k := range inputs {
		pgm.input <- k
	}
	return &pgm
}

func (self *Program) close() {
	close(self.input)
	close(self.output)
	self.die = true
}

func (self *Program) clone() *Program {
	return makeProgram(self.pgm, []int{})
}

func (self *Program) push( val int) {
	self.input <- val
}

func (self *Program) read_input() int {
	return <- self.input
}

func (self *Program) send_output( p int ) {
	self.output <- p
}

func (self *Program) pop() int {
	return <- self.output
}

func (self *Program) dump() []int {
	out := []int{}
	for val := range self.output {
		out = append( out, val )
	}
	return out
}

func (self *Program) opcode() int {
	opc := self.pgm[self.pc]
	self.modes = opc/100
	if TRACE {
		fmt.Printf( "%d: At %d: %d\n", self.id, self.pc, opc )
	}
	self.pc ++
	return opc % 100
}

func (self *Program) nextmode() int {
	p := self.modes % 10
	self.modes /= 10
	return p
}

func (self *Program) verify(loc int) {
	if loc >= len(self.pgm) {
		if TRACE {
			fmt.Println( "Extending memory to", loc )
		}
		self.pgm = append( self.pgm, Repeat( 0, loc-len(self.pgm)+1)... )
	}
}

func (self *Program) fetch() int {
	mode := self.nextmode()
	operand := self.pgm[self.pc]
	self.pc ++
	val := 0
	if mode == 0 {
		self.verify(operand)
		val = self.pgm[operand]
	} else if mode == 1 {
		val = operand
	} else if mode == 2 {
		self.verify(operand+self.rbase)
		val = self.pgm[operand+self.rbase]
	}
	if TRACE {
		fmt.Printf("%d fetch[%d] %d = %d\n", self.id, mode, operand, val)
	}
	return val
}

func (self *Program) store(n int) {
	mode := self.nextmode()
	operand := self.pgm[self.pc]
	if TRACE {
		fmt.Printf( "%d store[%d] %d at %d\n", self.id, mode, n, operand )
	}
	self.pc ++
	if mode == 0 {
		self.verify(operand)
		self.pgm[operand] = n
	} else if mode == 2 {
		self.verify(operand+self.rbase)
		self.pgm[operand+self.rbase] = n
	}
}

func bool2int(b bool) int {
	if b {
		return 1
	}
	return 0
}

func (self *Program) run() *Program {
	for ! self.die {
		opcode := self.opcode()
		if opcode == 1 {
			self.store( self.fetch() + self.fetch() )
		} else if opcode == 2 {
			self.store( self.fetch() * self.fetch() )
		} else if opcode == 3 {
			 ip := self.read_input()
			 if TRACE {
				 fmt.Println( self.id, "input", ip )
			 }
			 self.store( ip )
		} else if opcode == 4 {
			p := self.fetch()
			self.final = p
			self.send_output( p )
			if TRACE {
				fmt.Println( self.id, "output", p )
			}
		} else if opcode == 5 { // JT
			if self.fetch() != 0 {
				self.pc = self.fetch()
			} else {
				self.pc ++
			}
		} else if opcode == 6 {  // JF
			if self.fetch() == 0 {
				self.pc = self.fetch()
			} else {
				self.pc ++
			}
		} else if opcode == 7 {  // JLT
			self.store( bool2int(self.fetch() < self.fetch()))
		} else if opcode == 8 {  // JE
			self.store( bool2int(self.fetch() == self.fetch()))
		} else if opcode == 9 {  // set rbase
			self.rbase += self.fetch()
		} else if opcode == 99 {
			break
		} else {
			fmt.Println( "Explode, pc=",self.pc,", pgm=",self.pgm )
			break
		}
	}
	self.close()   // is this right?
	return self
}
