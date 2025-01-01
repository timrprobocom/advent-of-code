#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
#include <cstdint>
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
"5,4\n"
"4,2\n"
"4,5\n"
"3,0\n"
"2,1\n"
"6,3\n"
"2,4\n"
"1,5\n"
"0,6\n"
"3,3\n"
"2,6\n"
"5,1\n"
"1,2\n"
"5,5\n"
"2,5\n"
"6,5\n"
"1,4\n"
"0,4\n"
"6,4\n"
"1,1\n"
"6,1\n"
"1,0\n"
"0,5\n"
"1,6\n"
"2,0\n"
);


bool DEBUG = false;
bool TEST = false;
#define DAY "day18"

int WIDTH = -1;

typedef Point<int> point_t;

point_t START = Point(0,0);
point_t FINISH;

point_t dirs[] = {
    Point(-1,0),
    Point(0,-1),
    Point(1,0),
    Point(0,1)
};

typedef pair<point_t,int> queue_t;


int shortest( set<point_t> & walls )
{
    queue<queue_t> myq;
    myq.push( pair(START, 0) );
    set<point_t> visited;
    visited.insert(START);

    while( !myq.empty() )
    {
        queue_t pt = myq.front();
        myq.pop();
        point_t xy = pt.first;
        int d = pt.second;
        if( xy == FINISH )
            return d;
        for( auto dxy : dirs )
        {
            int x0 = xy.x + dxy.x;
            int y0 = xy.y + dxy.y;
            point_t xy0(x0,y0);
            if( 0 <= x0 && x0 < WIDTH && 
                0 <= y0 && y0 < WIDTH &&
                walls.find(xy0) == walls.end() &&
                visited.find(xy0) == visited.end()
            )
            {
                visited.insert( xy0 );
                myq.push( pair(xy0, d+1) );
            }
        }
    }
    return -1;
}

int part1( vector<point_t> & walls )
{
    int limit = TEST ? 12 : 1024;
    set<point_t> subset;
    copy( 
        walls.begin(), 
        walls.begin()+limit, 
        inserter(subset, subset.begin())
    );

    return shortest(subset);
}

// Binary search.

point_t part2( vector<point_t> walls )
{
    int minx = TEST ? 12 : 1024;
    int maxx = walls.size();
    int mid = 0;
    set<point_t> subset;
    while( minx < maxx )
    {
        mid = (maxx+minx)/2;
        
        subset.clear();
        copy( 
            walls.begin(), 
            walls.begin()+mid, 
            inserter(subset, subset.begin())
        );

        if( shortest(subset) < 0 )
        {
            maxx = mid;
            if( DEBUG )
                cout << mid << " fails\n";
        }
        else
        {
            minx = mid+1;
            if( DEBUG )
                cout << mid << " passes\n";
        }
    }
    mid = (maxx+minx)/2;
    return walls[mid-1];
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

    WIDTH = TEST ? 7 : 71;
    FINISH = Point(WIDTH-1,WIDTH-1);

    string data = TEST ? test : file_contents(DAY".txt");

    vector<point_t> walls;
    int accum = 0;
    int x = 0;
    for( char c : data )
    {
        if( c == ',' )
        {
            x = accum;
            accum = 0;
        }
        else if( c == '\n' )
        {
            walls.emplace_back( x,accum );
            accum = 0;
        }
        else if( isdigit(c) )
        {
            accum = accum * 10 + c - '0';
        }
    }
    walls.emplace_back( x,accum );

    cout << "Part 1: " << part1(walls) << "\n";
    point_t ans = part2(walls);
    cout << "Part 2: " << ans.x << "," << ans.y << "\n";
}
