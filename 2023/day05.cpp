#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <array>
#include <vector>
#include <set>
#include <algorithm>
#include <numeric>

using namespace std;

bool DEBUG = false;
bool TEST = false;

typedef vector<string> StringVector;
typedef vector<int> IntVector;
typedef vector<int64_t> LongVector;

const string test(
"seeds: 79 14 55 13\n"
"\n"
"seed-to-soil map:\n"
"50 98 2\n"
"52 50 48\n"
"\n"
"soil-to-fertilizer map:\n"
"0 15 37\n"
"37 52 2\n"
"39 0 15\n"
"\n"
"fertilizer-to-water map:\n"
"49 53 8\n"
"0 11 42\n"
"42 0 7\n"
"57 7 4\n"
"\n"
"water-to-light map:\n"
"88 18 7\n"
"18 25 70\n"
"\n"
"light-to-temperature map:\n"
"45 77 23\n"
"81 45 19\n"
"68 64 13\n"
"\n"
"temperature-to-humidity map:\n"
"0 69 1\n"
"1 0 69\n"
"\n"
"humidity-to-location map:\n"
"60 56 37\n"
"56 93 4\n"
);

struct Triad {
    int64_t a;
    int64_t b;
    int64_t n;
};

typedef vector<Triad> TriadVector;

struct Range {
    int64_t lo;
    int64_t size;
};

typedef vector<Range> RangeVector;

// Convert the input into a list of seed numbers, and a
// list of maps.  Each map is a list of tuples, (dest,src,len).

void process(istream & data, LongVector & seeds, vector<TriadVector> & maps)
{
    string word;
    string lastmap = "";
    vector<LongVector> ints;

    while( data >> word )
    {
        if( word.back() == ':' )
        {
            // New mapping.
            ints.push_back( LongVector() );
        }
        else if (isdigit(word[0]))
        {
            ints.back().push_back(stol(word));
        }
    }

    // Pop the first for seeds.

    seeds.swap( ints.front() );
    ints.erase( ints.begin() );

    // Convert the integer lists to triads, to make them easier to sort.

    maps.resize( ints.size() );
    for( int j = 0; j < ints.size(); j++ )
    {
        LongVector & m = ints[j];
        for( int i = 0; i < m.size(); i+=3 )
            maps[j].push_back(Triad({m[i],m[i+1],m[i+2]}));
    }

    // Sort them all.

    for( auto & iv : maps )
    {
        sort( iv.begin(), iv.end(), [](const Triad & a, const Triad & b) { return a.b < b.b; });
    }

    if( DEBUG )
        for( auto & iv : maps )
        {
            cout << "Map: ";
            for( auto t : iv )
                cout << "(" << t.a << " " << t.b << " " << t.n << ") ";
            cout << "\n";
        }
}

#if 0

// Map a single value through a single map.

int64_t mapping( TriadVector & mapx, int64_t inval )
{
    for( auto & m : mapx )
    {
        if( m.b <= inval && inval <= m.b+m.n )
            return inval - m.b + m.a;
    }
    return inval;
}


// Map a single value through all of the maps.

int64_t domapping( vector<TriadVector> & maps, int64_t i )
{
    for( auto & m : maps )
        i = mapping( m, i );
    return i;
}

#endif

// We need to intersect the ranges.
// There are 3 cases to consider:
//   * The range starts before any map
//   * The range intersects one or more maps
//   * The range extends beyond the last map
//
//  So given 79,14  against 50,98,2 and 52,50,48
//    We get 79,14 had a delta of +2
//  Given 40,70  against 50,98,2 and 52,50,48
//    We get 40,10 with delta 0
//           50,48 with a delta of +2
//           98,2 with a delta of -48
//           100,10 with a delta of 0



// Map a single range through a single map, which may produce several ranges.

void maprange( TriadVector & mapx, Range rng, vector<Range> & result )
{
    int64_t hi = rng.lo+rng.size;
    if( rng.lo < mapx[0].b )
    {
        int64_t take = min(hi, mapx[0].b) - rng.lo;
        result.push_back(Range({rng.lo, take}));
        rng.lo += take;
    }
    if( rng.lo == hi)
        return;
    
    for( auto & m : mapx )
    {
        if( m.b <= rng.lo && rng.lo <= m.b + m.n )
        {
            int64_t take = min(hi, m.b+m.n) - rng.lo;
            result.push_back(Range({rng.lo+m.a-m.b, take}));
            rng.lo += take;
        }
        if( rng.lo == hi )
            return;
    }
    
    if( rng.lo < hi )
        result.push_back(Range({rng.lo, hi-rng.lo}));
}

// Map a set of ranges through a single map.

void domapranges( TriadVector & mapx, RangeVector & rngs, RangeVector & result )
{
    result.clear();
    for( auto & rng : rngs )
        maprange( mapx, rng, result );
}


// Map a set of ranges through all of the maps.

void doallmapranges( vector<TriadVector> & maps, RangeVector & rngs )
{
    for( auto & m : maps )
    {
        RangeVector result;
        domapranges( m, rngs, result );
        rngs.swap(result);
    }
}

#if 0
int64_t part1( LongVector & seeds, vector<TriadVector> & maps )
{
    int64_t minx = 999999999999;
    for( int64_t s : seeds )
    {
        int64_t v = domapping( maps, s );
        if( v < minx )
            minx = v;
    }
    return minx;
}
#endif

int64_t part2( int part, LongVector & seeds, vector<TriadVector> & maps )
{
    RangeVector ranges;
    if( part == 1 )
    {
        for( auto s : seeds )
            ranges.push_back(Range({s,1}));
    } else {
        for( int i = 0; i < seeds.size(); i += 2)
            ranges.push_back(Range({seeds[i],seeds[i+1]}));
    }
    doallmapranges(maps, ranges);
    int64_t minx = 999999999999;
    for( auto & r : ranges )
        minx = min(r.lo, minx);
    return minx;
}


int main( int argc, char ** argv )
{
    while( *++argv )
    {
        string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg =="test")
            TEST = true;
    }

    istringstream data;
    if( TEST )
    {
        data.str( test );
    }
    else 
    {
        stringstream buffer;
        buffer << ifstream("day05.txt").rdbuf();
        data.str( buffer.str() );
    }

    vector<TriadVector> maps;
    LongVector seeds;
    process( data, seeds, maps );

#if 0
    cout << "Part 1: " << part1(seeds, maps) << "\n";
#endif
    cout << "Part 1: " << part2(1, seeds, maps) << "\n";
    cout << "Part 2: " << part2(2, seeds, maps) << "\n";
}
