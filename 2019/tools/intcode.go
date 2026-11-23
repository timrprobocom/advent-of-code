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
	finish chan int
	input  chan int
	output chan int
	rbase int
	die   bool
	modes int
	Final int
}

// How do we shut down the channels?

func MakeProgram(program []int) *Program {
	pgm := Program{}
	pgm.id = count
	count++
	pgm.pgm = slices.Clone( program )
	pgm.finish = make(chan int, 10)
	pgm.input = make(chan int, 100)
	pgm.output = make(chan int, 50)
	return &pgm
}


func (self *Program) Close() {
	close(self.output)
	self.die = true
}

func Connect( producer *Program, consumer *Program ) {
	consumer.input = producer.output
}

func (self *Program) Clone() *Program {
	return MakeProgram(self.pgm)
}

func (self *Program) IsAlive() bool {
	return ! self.die
}

func (self *Program) Push( val int) {
	self.input <- val
}

func (self *Program) Pop() int {
	return <- self.output
}

func (self *Program) Read_input() int {
	return <- self.input
}

func (self *Program) Send_output( p int ) {
	self.output <- p
}

func (self *Program) Dump() []int {
	out := []int{}
	for val := range self.output {
		out = append( out, val )
	}
	return out
}

func (self *Program) Opcode() int {
	opc := self.pgm[self.pc]
	self.modes = opc/100
	if TRACE {
		fmt.Printf( "%d: At %d: %d\n", self.id, self.pc, opc )
	}
	self.pc ++
	return opc % 100
}

func (self *Program) Nextmode() int {
	p := self.modes % 10
	self.modes /= 10
	return p
}

func (self *Program) Verify(loc int) {
	if loc >= len(self.pgm) {
		if TRACE {
			fmt.Println( "Extending memory to", loc )
		}
		self.pgm = append( self.pgm, Repeat( 0, loc-len(self.pgm)+1)... )
	}
}

func (self *Program) Fetch() int {
	mode := self.Nextmode()
	operand := self.pgm[self.pc]
	self.pc ++
	val := 0
	if mode == 0 {
		self.Verify(operand)
		val = self.pgm[operand]
	} else if mode == 1 {
		val = operand
	} else if mode == 2 {
		self.Verify(operand+self.rbase)
		val = self.pgm[operand+self.rbase]
	}
	if TRACE {
		fmt.Printf("%d Fetch[%d] %d = %d\n", self.id, mode, operand, val)
	}
	return val
}

func (self *Program) Store(n int) {
	mode := self.Nextmode()
	operand := self.pgm[self.pc]
	if TRACE {
		fmt.Printf( "%d Store[%d] %d at %d\n", self.id, mode, n, operand )
	}
	self.pc ++
	if mode == 0 {
		self.Verify(operand)
		self.pgm[operand] = n
	} else if mode == 2 {
		self.Verify(operand+self.rbase)
		self.pgm[operand+self.rbase] = n
	}
}

func bool2int(b bool) int {
	if b {
		return 1
	}
	return 0
}

func (self *Program) Run() *Program {
	for ! self.die {
		opcode := self.Opcode()
		if opcode == 1 {
			self.Store( self.Fetch() + self.Fetch() )
		} else if opcode == 2 {
			self.Store( self.Fetch() * self.Fetch() )
		} else if opcode == 3 {
			 ip := self.Read_input()
			 if TRACE {
				 fmt.Println( self.id, "input", ip )
			 }
			 self.Store( ip )
		} else if opcode == 4 {
			p := self.Fetch()
			self.Final = p
			self.Send_output( p )
			if TRACE {
				fmt.Println( self.id, "output", p )
			}
		} else if opcode == 5 { // JT
			if self.Fetch() != 0 {
				self.pc = self.Fetch()
			} else {
				self.pc ++
			}
		} else if opcode == 6 {  // JF
			if self.Fetch() == 0 {
				self.pc = self.Fetch()
			} else {
				self.pc ++
			}
		} else if opcode == 7 {  // JLT
			self.Store( bool2int(self.Fetch() < self.Fetch()))
		} else if opcode == 8 {  // JE
			self.Store( bool2int(self.Fetch() == self.Fetch()))
		} else if opcode == 9 {  // set rbase
			self.rbase += self.Fetch()
		} else if opcode == 99 {
			break
		} else {
			fmt.Println( "Explode, pc=",self.pc,", pgm=",self.pgm )
			break
		}
	}
	self.finish <- 0
	self.Close()
	return self
}

func (self *Program) Wait() {
	<-self.finish
}
