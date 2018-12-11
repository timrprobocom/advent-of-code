#include <stdio.h>
#include <stdint.h>

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

int main()
{
#if 0
    GeneratorB g1(   65, 16807, 4 );
    GeneratorB g2( 8921, 48271, 8 );
#else
    GeneratorB g1(  277, 16807, 4 );
    GeneratorB g2(  349, 48271, 8 );
#endif

    int count = 0;
//    for( int i = 0; i < 40000000; i++ )
    for( int i = 0; i < 5000000; i++ )
    {
        if( (g1.next() & 0xffff) == (g2.next() & 0xffff) )
            count++;
    }

    printf( "Answer is %d\n", count );
}

