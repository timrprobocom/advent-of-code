#include <fstream>
#include <iostream>
#include <cstdint>
#include <vector>
#include <numeric>
#include <algorithm>

#define test "flqrgnkx"
#define live "nbysizxe"

bool DEBUG = false;
bool TEST = false;

// 128 bits is 16 bytes

const char extra[] = {17,31,73,47,23,0};

typedef std::vector<uint8_t> ByteVector;
typedef std::vector<ByteVector> ByteArray;
typedef std::vector<int32_t> IntVector;
typedef std::vector<IntVector> IntArray;

class popcount_t {
    std::vector<int> counts;

public:
    popcount_t()
    {
        for( int i = 0; i < 256; i++ )
        {
            int cnt = 0;
            for( int b = 0; b < 8; b++ )
                if( i & (1 << b) )
                    cnt ++;
            counts.push_back( cnt );
        }
    }

    int count(ByteVector & bv )
    {
        int c = 0;
        for( auto & b : bv )
            c += counts[b];
        return c;
    }
};

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

ByteArray makearray(std::string data) {
    ByteArray array;
    for( int row = 0; row < 128; row++ ) {
        std::string inp = data + "-" + std::to_string(row);
        array.push_back( knothash(inp) );
    }
    return array;
}

int part1( ByteArray & array )
{
    popcount_t popcount;
    int sum = 0;
    for( auto & row : array )
        sum += popcount.count(row);
    return sum;
}

IntArray convert( ByteArray & array )
{
    IntArray grid;
    for( auto row : array )
    {
        IntVector binrow;
        for( auto c : row )
        {
            for( int b = 7; b >= 0; b-- )
            {
                binrow.push_back( c & (1<<b) ? -1 : 0 );
            }
        }
        grid.push_back( binrow );
    }
    return grid;
}

void contiguous( IntArray & grid, int y, int x, int tag )
{
    grid[y][x] = tag;
    if( x > 0 && grid[y][x-1] < 0 )
        contiguous( grid, y, x-1, tag );
    if( x < 127 && grid[y][x+1] < 0 )
        contiguous( grid, y, x+1, tag );
    if( y > 0 && grid[y-1][x] < 0 )
        contiguous( grid, y-1, x, tag );
    if( y < 127 && grid[y+1][x] < 0 )
        contiguous( grid, y+1, x, tag );
}

int part2( IntArray & grid ) 
{
    int tag = 1;
    for( int y = 0; y < 128; y++ )
        for( int x = 0; x < 128; x++ )
            if( grid[y][x] == -1 )
            {
                contiguous( grid, y, x, tag );
                tag ++;
            }
    return tag-1;
}

int main( int argc, char ** argv )
{
    std::string name = *argv;
    while( *++argv )
    {
        std::string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg =="test")
            TEST = true;
    }

    auto array = makearray(TEST ? test : live);
    std::cout << "Part 1: " << part1(array) << "\n";
    auto grid = convert(array);
    std::cout << "Part 2: " << part2(grid) << "\n";
}
