#include <fstream>
#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>

#define test "flqrgnkx"
#define live "nbysizxe"

// 128 bits is 16 bytes

const char extra[] = {17,31,73,47,23,0};

typedef std::vector<uint8_t> ByteVector;

ByteVector knothash( std::string inp )
{
    std::string val = inp + extra;
    ByteVector rope(256);
    std::iota( rope.begin(), rope.end(), 0 );

    int posn = 0;
    int skip = 0;
    for( int round = 0; round < 64; round++ )
    {
        for( auto c : val )
        {
            // Swap posn with posn+i-1
            for( int j = 0; j < c/2; j++ )
            {
                int left = (posn + j) % rope.size();
                int right = (posn + c - 1 - j) % rope.size();
                if( left == right )
                    continue;
                uint8_t temp = rope[left];
                rope[left] = rope[right];
                rope[right] = temp;
            }
            posn = (posn + c + skip) % rope.size();
            skip ++;
        }
    }

    // Compute hash.

    uint8_t hash = 0;
    ByteVector knot;
    for( int i = 0; i < rope.size(); i++ )
    {
        hash ^= rope[i];
        if( i % 16 == 15 )
        {
            knot.push_back( hash );
            hash = 0;
        }
    }

    return knot;
}

std::string tostring(ByteVector v)
{
    const char xlate[] = "0123456789abcdef";
    std::string s;
    for( auto c : v )
    {
        s += xlate[c>>4];
        s += xlate[c&15];
    }
    return s;
}

void
day10b()
{
    for( auto input : {
        "",
        "AoC 2017",
        "1,2,3",
        "1,2,4",
        "94,84,0,79,2,27,81,1,123,93,218,23,103,255,254,243"
    })
    {
        ByteVector v = knothash( input );
        std::cout << tostring(v) << "\n";
    }
}


#if 0

def makecounts():
    counts = []
    for i in range(256):
        c = 0
        for b in (1,2,4,8,16,32,64,128):
            if i & b:
                c += 1
        counts.append(c)
    return counts

counts = makecounts()

def countbits(hx):
    c = 0
    for byte in hx.decode('hex'):
        c += counts[ord(byte)]
    return c

def makearray(data):
    array = []
    for row in range(128):
        array.append( knothash('%s-%d' % (data,row) ) )
    return array

def parta(array):
    return sum( countbits(row) for row in array )

def convert(array):
    grid = []
    for row in array:
        binrow = []
        for c in row.decode('hex'):
            for b in (128,64,32,16,8,4,2,1):
                binrow.append( -1 if ord(c) & b else 0 )
        grid.append(binrow)
    return grid

def contiguous( grid, y, x, tag ):
    grid[y][x] = tag
    if x > 0 and grid[y][x-1] < 0:
        contiguous( grid, y, x-1, tag )
    if x < 127 and grid[y][x+1] < 0:
        contiguous( grid, y, x+1, tag )
    if y > 0 and grid[y-1][x] < 0:
        contiguous( grid, y-1, x, tag )
    if y < 127 and grid[y+1][x] < 0:
        contiguous( grid, y+1, x, tag )

def partb(grid):
    tag = 1
    for y in range(128):
        for x in range(128):
            if grid[y][x] == -1:
                contiguous( grid, y, x, tag )
                tag += 1
    return tag-1

array = makearray(test)
print 'Part A', parta(array)
grid = convert(array)
print 'Part B', partb(grid)
for y in range(16):
    print ' '.join('%3d' % k for k in grid[y][0:16])


array = makearray(live)
print 'Part A', parta(array)
grid = convert(array)
print 'Part B', partb(grid)
for y in range(16):
    print ' '.join('%3d' % k for k in grid[y][0:16])
#endif
