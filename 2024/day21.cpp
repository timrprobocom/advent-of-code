#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
#include <cstdint>
#include <limits.h>
#include <cstring>
#include <cmath>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <numeric>

#include "utils.h"

using namespace std;

const string test(
"029A\n"
"980A\n"
"179A\n"
"456A\n"
"379A"
);

const string live(
"973A\n"
"836A\n"
"780A\n"
"985A\n"
"413A"
);

bool DEBUG = false;
bool TEST = false;

typedef unsigned short point_t;

inline point_t make_point(byte_t x, byte_t y)
{
    return (x<<8)|y;
}
inline byte_t getx(point_t pt)
{
    return pt>>8;
}
inline byte_t gety(point_t pt)
{
    return pt&0xff;
}

typedef pair<point_t,string> queue_t;
#if 0
inline queue_t make_queue(point_t pt, string s)
{
    return make_pair(pt,s);
}
inline queue_t make_queue(byte_t x, byte_t y, string s)
{
    return make_pair(make_point(x,y),s);
}
inline point_t getpoint(queue_t q)
{
    return q.first;
}
inline string gets(queue_t q)
{
    return q.second;
}
#endif

// This is faster than a map<char,point_t>.

/*
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
*/

constexpr point_t buttons(char c)
{
    switch(c)
    {
        case '7': return make_point(0,0);
        case '8': return make_point(1,0);
        case '9': return make_point(2,0);
        case '4': return make_point(0,1);
        case '5': return make_point(1,1);
        case '6': return make_point(2,1);
        case '1': return make_point(0,2);
        case '2': return make_point(1,2);
        case '3': return make_point(2,2);
        case 'X': return make_point(0,3);
        case '0': return make_point(1,3);
        case 'A': return make_point(2,3);
    }
    return make_point(0,0);
}

/*
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
*/

constexpr point_t dirpad(char c)
{
    switch(c)
    {
        case 'X': return make_point(0,0);
        case '^': return make_point(1,0);
        case 'A': return make_point(2,0);
        case '<': return make_point(0,1);
        case 'v': return make_point(1,1);
        case '>': return make_point(2,1);
    }
    return make_point(0,0);
}


int64_t cheapest( point_t pt0, point_t pt1, int botcount=2 );
int64_t cheapestAuxPad( point_t pt0, point_t pt1, int robots );
int64_t cheapestRobot( const string & keys, int robots );

struct cache_t {
    point_t pt0;
    point_t pt1;
    int robots;

    bool operator<(const cache_t & other) const
    {
          return pt0 < other.pt0 || 
                 (pt0==other.pt0 && pt1 < other.pt1) || 
                 ((pt0==other.pt0 && pt1==other.pt1) && robots < other.robots);
    }
};

map<cache_t, int64_t> cache;

// @cache
int64_t cheapestAuxPad( point_t pt0, point_t pt1, int robots )
{
    cache_t me({pt0,pt1,robots});
    if( cache.find(me) != cache.end())
        return cache[me];

    int64_t res = INT64_MAX;
    queue<queue_t> q;

    q.push( pair(pt0, "") );

    while( !q.empty() )
    {
        auto [xy, s] = q.front();
        q.pop();
        if( xy == pt1 )
        {
            res = min( res, cheapestRobot( s+"A", robots-1 ));
            continue;
        }
        if( xy == dirpad('X') )
            continue;
        if( getx(xy) < getx(pt1) )
            q.push( pair(make_point(getx(xy)+1, gety(xy)), s+">"));
        else if( getx(xy) > getx(pt1) )
            q.push( pair(make_point(getx(xy)-1, gety(xy)), s+"<"));
        if( gety(xy) < gety(pt1) )
            q.push( pair(make_point(getx(xy), gety(xy)+1), s+"v"));
        else if( gety(xy) > gety(pt1) )
            q.push( pair(make_point(getx(xy), gety(xy)-1), s+"^"));
    }
    cache[me] = res;
    return res;        
}


int64_t cheapestRobot( const string & keys, int robots )
{
    if( !robots )
        return keys.size();
    int64_t sumx = 0;
    point_t pt0 = dirpad('A');
    for( char c : keys )
    {
        point_t pt1  = dirpad(c);
        sumx += cheapestAuxPad( pt0, pt1, robots);
        pt0 = pt1;
    }
    return sumx;
}


int64_t cheapest( point_t pt0, point_t pt1, int botcount )
{
    int64_t res = INT64_MAX;
    queue<queue_t> q;

    q.push( pair(pt0, "") );

    while( !q.empty() )
    {
        auto [xy, s] = q.front();
        q.pop();
        if( xy == pt1 )
        {
            res = min( res, cheapestRobot( s+"A", botcount ) );
            continue;
        }
        if( xy == buttons('X') )
            continue;
        if( getx(xy) < getx(pt1) )
            q.push( pair(make_point(getx(xy)+1, gety(xy)), s+">" ));
        else if( getx(xy) > getx(pt1) )
            q.push( pair(make_point(getx(xy)-1, gety(xy)), s+"<" ));
        if( gety(xy) < gety(pt1) )
            q.push( pair(make_point(getx(xy), gety(xy)+1), s+"v" ));
        else if( gety(xy) > gety(pt1) )
            q.push( pair(make_point(getx(xy), gety(xy)-1), s+"^" ));
    }
    return res;
}


int64_t part1( StringVector & data, int bots=2 )
{
    int64_t sumx = 0;
    for( auto & line : data )
    {
        int64_t res = 0;
        point_t pt0 = buttons('A');
        for( char c : line )
        {
            if( DEBUG )
                cout << "---" << c << "---\n";
            point_t pt1 = buttons(c);
            res += cheapest( pt0, pt1, bots);
            pt0 = pt1;
        }
        if( DEBUG )
            cout << res << "\n";

        int val = 0;
        for( auto c : line )
            if( isdigit(c) )
                val = val * 10 + c - '0';
        sumx += val * res;
    }
    return sumx;
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

    string input = TEST ? test : live;
    StringVector data = split(input, "\n");

    cout << "Part 1: " << part1(data,  2) << "\n";
    cout << "Part 2: " << part1(data, 25) << "\n";
}
