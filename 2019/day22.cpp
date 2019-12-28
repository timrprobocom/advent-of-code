#include <iostream>
#include <fstream>
#include <sstream>
#include <numeric>
//#include "uint128.h"

bool TRACE = false;

// Find the multiplicative inverse in a modulus field.

// This is the Extended Euclidean Algorithm.  It does not care about the
// totient.  It does, however, fail if a is negative, so we compensate.
// It is basically doing a GCD.

int64_t invert( int64_t a, int64_t n )
{
    int64_t t = 0;
    int64_t newt = 1;
    int64_t r = n;
    int64_t newr = a > 0 ? a : a + n;

    while( newr )
    {
        int64_t q = r / newr;
        int64_t t0 = t;
        t = newt;
        newt = t0 - q * newt;
        int64_t r0 = r;
        r = newr;
        newr = r0 - q * newr;
    }

    return t >= 0 ? t : t+n;
}

// Do modular exponentiation.

int64_t pow( int64_t b, int64_t e, int64_t m )
{
    int64_t result = 1;
    b = b & m;
    while( e > 0 )
    {
        if( e & 1 )
            result = (result * b) % m;
        e >>= 1;
        b = (b * b) % m;
    }
    return result;
}


const char * test1 = 
"deal into new stack\n"
"cut -2\n"
"deal with increment 7\n"
"cut 8\n"
"cut -4\n"
"deal with increment 7\n"
"cut 3\n"
"deal with increment 9\n"
"deal with increment 3\n"
"cut -1\n";
// Result: 9 2 5 8 1 4 7 0 3 6

bool startswith( const std::string & haystack, const std::string & needle )
{
    return haystack.substr( 0, needle.size() ) == needle;
}

int lastfield( const std::string & s )
{
    int n = s.find_last_of( ' ' );
    return std::stoi( s.substr(n+1) );
}

// A deck can be encoded as ax+b mod n.

class Deck
{
public:
    int64_t count;
    int64_t base;
    int64_t incr;

    Deck( int k )
        : count( k )
        , base( 0 )
        , incr( 1 )
    {
    }

protected:
    void cut(int64_t n)
    {
        base = (base + incr * n + count) % count;
    }

    void reverse()
    {
        incr = count - incr;
        base = (base + incr + count) % count;
    }

    void increment(int64_t n)
    {
        incr = (incr * invert(n, count)) % count;
    }

public:
    void run( std::istream & iss )
    {
        for( std::string ln; getline( iss, ln ); )
        {
            if( TRACE )
                std::cout << ln << "\n";
            if( startswith( ln, "cut" ) )
                cut( lastfield(ln) );
            if( startswith( ln, "deal with") )
                increment( lastfield(ln) );
            if( startswith( ln, "deal into") )
                reverse();
            if( TRACE )
                std::cout << "(" << base << "," << incr << ")\n";
        }
    }
};

// Do a part 1 test.  Should be 9 2 5 8 1 4 7 0 3 6, or 9+3x.

void part1test()
{
    int COUNT = 10;
    Deck deck(COUNT);
    deck.run( std::istringstream(test1) );
    std::cout << "(" << deck.base << "," << deck.incr << ")\n";
    int b = deck.base;
    int m = deck.incr;
    for( int x=0; x < COUNT; x++ )
        std::cout << ((m*x+b) % COUNT);
    std::cout << "\n";
}

// Do part 1.  Should be 4775.

void part1()
{
    int COUNT = 10007;
    Deck deck(COUNT);
    deck.run( std::ifstream("day22.txt") );
    std::cout << "(" << deck.base << "," << deck.incr << ")\n";
    int b = deck.base;
    int m = deck.incr;

    for( int x=0; x < COUNT; x++ )
    {
        if( (m*x+b) % COUNT == 2019 )
        {
            std::cout << "Part 1: " << x << "\n";
            break;
        }
    }
}

// Do part 2.  Shouild be 37889219674304.
//
// This requires 128-bit arithmetic.

void part2()
{
    int64_t COUNT = 119315717514047;
    Deck deck(COUNT);
    deck.run( std::ifstream("day22.txt") );
    std::cout << "(" << deck.base << "," << deck.incr << ")\n";
    int b = deck.base;
    int m = deck.incr;

// So, each cycle through will do
// bn = mn * b
// mn = m
// So it's a geometric series.  b x (1-m^cycles) / (1-m).
// The formula comes from Wikipedia.  There's magic to do
// exponentiation and inversion in a modulus field.

    int64_t cycles = 101741582076661;
    int64_t finalm = pow( m, cycles, COUNT );
    int64_t finalb = (b * (1 - finalm) * invert(1 - m, COUNT)  ) % COUNT;
    std::cout << "(" << finalm << "," << finalb << ")\n";

    int tgt = 2020;
    std::cout << "Part 2: " << ((finalm * tgt + finalb) % COUNT) << "\n";
}

int main()
{
    part1test();
    part1();
    part2();
}
