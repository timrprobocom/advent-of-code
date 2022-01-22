# Understanding Advent 2021 Day 24

In day 24 of the 2021 Advent of Code, we were presented with a simple processor to emulate.  Each year usually finds at least one such emulation to handle.  This year's was a bit different, in that it was not actually necessary to build the emulator to solve the problem.  In fact, it could be solved on paper without an awful lot of trouble.

If you look at your source code, you'll see that it is divided into 14 nearly identical sections, each starting with an `inp w` statement.  There are, in fact, two different section, each repeated 7 times.  Section A looks like this:

```
inp w           # Digit 0
mul x 0
add x z    
mod x 26
div z 1			# 1
add x 14		# 2
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14		# 3
mul y x
add z y
```

Section B looks like this:

```
inp w           # Digit 5
mul x 0
add x z
mod x 26
div z 26		# 1
add x -12       # 2
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 5			# 3
mul y x
add z y
```

There are only three differences here.  If you follow section A, you'll see that by the 8th statement, x will always be 1, regardless of the input.  That means `z` is multiplied by 26, `y` becomes the input value + 14, and that gets added to `z`.  Stepping back a bit, what is happening here is that we are constructing a 14-digit number in base 26 in the `z` register.

Because of the one change in the line marked "# 1", section B is a different.  Here, we pop the low-order digit of that base 26 number into `x`, and shift `z` down by one digit.  So if the number had been [5,11,6,10], `x` gets 10 and `z` gets [5,11,6].  Then, starting with `# 2`, if that digit we popped, plus a constant, equals the digit that was input, `x` ends up as 0.  Notice what happens in that case: `y` becomes 1, `z` is multiplied by 1 instead of 26. and the new digit plus the constant at `# 3` gets canceled out.  So, if the `eql x w` matches, the net effect of this block is to pop the low order digit from `z`.  If the `eql x w` doesn't match, the net effect is just like section A: we add another digit into the base 26 number.

We can rewrite the sections in Python:

```
# Section A:
z = z * 26 + inp + const

# Section B:
z = z // 26
if z % 26 + const != inp:
    z = z * 26 + inp + const
```

Or, if we treat `z` as a list of digits instead of a single number:

```
# Section A:
z.append( inp + const )

# Section B:
if z.pop() + const != inp:
    z.append( inp + const )
```

Remember the goal here is to find inputs that cause `z` to end up at 0.  The only way that can happen is if we are able to pop all the digits we push.  That means that, in every section B, the low order digit must match the new input digit plus/minus the constants, which are unique for each input.  Your input is going to differ from mine in the distribution of the sections (although always 7 As and 7 Bs), and the constants in "# 2" and "# 3", but the philosophy is the same.

With my input, the Python equivalent of the whole program becomes this:

```
z = []
z.append( inp[0] + 14 )
z.append( inp[1] + 2 )
z.append( inp[2] + 1 )
z.append( inp[3] + 13 )
z.append( inp[4] + 5 )
if z.pop() - 12 != inp[5]:
    z.append( inp[5] + 5 )
if z.pop() - 12 != inp[6]:
    z.append( inp[6] + 5 )
z.append( inp[7] + 9 )
if z.pop() - 7 != inp[8]:
    z.append( inp[8] + 3 )
z.append( inp[9] + 13 )
if z.pop() - 8 != inp[10]:
    z.append( inp[10] + 2 )
if z.pop() - 5 != inp[11]:
    z.append( inp[11] + 1 )
if z.pop() - 10 != inp[12]:
    z.append( inp[12] + 11 )
if z.pop() - 7 != inp[13]:
    z.append( inp[13] + 8 )
```

Remember that the "section A vs section B" decision is based on the `div z 1` vs `div z 26` instruction.  The first constant comes from the final `add y` in each section labeled "# 3", and the second constant comes from the "# 2" instructions.

This is a nice pattern.  There are 7 section As (which push), and 7 section Bs (which can pop).  So, let's look at the sections for inputs 4 and 5:

```
z.append( inp[4] + 5 )
if z.pop() - 12 != inp[5]:
    z.append( inp[5] + 5 )
```

We want that `if` statement NOT to be taken.  `z.pop` is going to pop what we just appended in the previous statement, so this sequence is exactly equivalent to:

```
if inp[4] + 5 - 12 != inp[5]:
    z.append( inp[5] + 5 )
```

So, if our 5th input digit minus 7 is equal to our 6th input digit, then neither one of them get added to `z`, and it is as if that whole pair of sections didn't exist.  That's the key here.  We want to remove these canceled-out sections until none are left.  Similarly, if `inp[7] + 9 - 7 == inp[8]`, then those two sections are eliminated.  And, if `inp[9] + 13 - 8  == inp[10]`, those two sections are eliminated.  If we remove those, we are left with:

```
z = []
z.append( inp[0] + 14 )
z.append( inp[1] + 2 )
z.append( inp[2] + 1 )
z.append( inp[3] + 13 )
if z.pop() - 12 != inp[6]:
    z.append( inp[6] + 5 )
if z.pop() - 5 != inp[11]:
    z.append( inp[11] + 1 )
if z.pop() - 10 != inp[12]:
    z.append( inp[12] + 11 )
if z.pop() - 7 != inp[13]:
    z.append( inp[13] + 8 )
```

It should now be clear that we are just eliminating pairs from the inside out.  If `inp[3] + 13 - 12 == inp[6]`, those get eliminated.  If `inp[2] + 1 - 5 == inp[11]`, those get eliminated.  If `inp[1] + 2 - 10 == inp[12]` and `inp[0] + 14 - 7 == inp[13]`, then we eliminate all of our digits, `z` ends up with 0, and the model number qualifies.

That means the value of `inp[5]` is exactly determined by the value of `inp[4]`.  Instead of having 14 independent variables, we only have 7 independent variables.  It is certainly possible to enumerate all 10,000,000 possible values, but we don't even have to do that much.  Let's look at the equations we must satisfy:

```
inp[0] + 14 -  7 == inp[13]  (delta = +7)
inp[1] +  2 - 10 -= inp[12]  (delta = -8)
inp[2] +  1 -  5 == inp[11]  (delta = -4)
inp[3] + 13 - 12 == inp[6]   (delta = +1)
inp[4] +  5 - 12 == inp[5]   (delta = -7)
inp[7] +  9 -  7 == inp[8]   (delta = +2)
inp[9] + 13 -  8 == inp[10]  (delta = +5)
```

There's another factor to help us.  Each of those input numbers must be between 1 and 9.  In order to have two numbers in that set that have a difference of 7, the only possibility is that one of them is 1 and the other 8, or one is 2 and the other 9.  That significantly restricts the range of our numbers:

```
inp[0] + 14 -  7 == inp[13]  (delta = +7)  
    inp[0] in (1,2)
    inp[13] in (8,9)
inp[1] +  2 - 10 -= inp[12]  (delta = -8)
    inp[1] == 9
    inp[12] == 1
inp[2] +  1 -  5 == inp[11]  (delta = -4)
    inp[1] in (5 to 9)
    inp[11] in (1 to 5)
inp[3] + 13 - 12 == inp[6]   (delta = +1)
    inp[3] in (1 to 8)
    inp[6] in (2 to 9)
inp[4] +  5 - 12 == inp[5]   (delta = -7)
    inp[4] in (8,9)
    inp[5] in (1,2)
inp[7] +  9 -  7 == inp[8]   (delta = +2)
    inp[7] in (1 to 7)
    inp[8] in (3 to 9)
inp[9] + 13 -  8 == inp[10]  (delta = +5)
    inp[9] in (1 to 4)
    inp[10] in (5 to 9)
```

So, let's extract those ranges in order:

```
inp[0] in (1,2)
inp[1] == 9
inp[1] in (5 to 9)
inp[3] in (1 to 8)
inp[4] in (8,9)
inp[5] in (1,2)
inp[6] in (2 to 9)
inp[7] in (1 to 7)
inp[8] in (3 to 9)
inp[9] in (1 to 4)
inp[10] in (5 to 9)
inp[11] in (1 to 5)
inp[12] == 1
inp[13] in (8,9)
```

That's a much smaller set of possibles: 2 x 1 x 5 x 8 x 2 x 2 x 8 x 7 x 7 x 4 x 5 x 5 x 1 x 2 ends up being 4,880, and that is exactly how many possible solutions there are for my input.  We can easily and quickly run 7 nested loops with 4,880 possibilities, but is turns out we don't even have to go **that** far.  All we want is the largest (for part 1) and smallest (for part 2) key numbers, and we can read those right off of that list:

```
Largest:  2 9 9 8 9 2 9 7 9 4 9 5 1 9
Smallest: 1 9 5 1 8 1 2 1 3 1 5 1 1 8
```

And those, in fact, are the answers to my part 1 and part 2.
