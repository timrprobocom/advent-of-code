#include <stdio.h>
#include <cstdint>
#include <string>
#include <iostream>

bool DEBUG = false;
bool TEST = false;

struct Generator
{
    uint64_t val;
    uint64_t mult;

    Generator( uint32_t start_, uint32_t mult_ )
        : val( start_ )
        , mult( mult_ )
    {
    }

    int next()
    {
        return val = (val * mult) % 0x7fffffff;
    }
};

struct GeneratorB
{
    uint64_t val;
    uint64_t mult;
    uint32_t mod;

    GeneratorB( uint32_t start_, uint32_t mult_, uint32_t mod_ )
        : val( start_ )
        , mult( mult_ )
        , mod( mod_ )
    {
    }

    int next()
    {
        do{
            val = (val * mult) % 0x7fffffff;
        } while( val % mod );
        return val;
    }
};

int part1( uint32_t start1, uint32_t start2,  uint32_t mod1, uint32_t mod2, int loops )
{
    GeneratorB g1( start1, 16807, mod1 );
    GeneratorB g2( start2, 48271, mod2 );
    int count = 0;
    for( int i = 0; i < loops; i++ )
        if( (g1.next() & 0xffff) == (g2.next() & 0xffff) )
            count++;
    return count;
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

    int start1 = TEST ?   65 : 277;
    int start2 = TEST ? 8921 : 349;

    std::cout << "Part 1: " << part1( start1, start2, 1, 1, 40000000 ) << "\n";
    std::cout << "Part 2: " << part1( start1, start2, 4, 8,  5000000 ) << "\n";
}

