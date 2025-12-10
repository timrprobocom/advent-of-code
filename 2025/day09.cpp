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
    "7,1\n"
    "11,1\n"
    "11,7\n"
    "9,7\n"
    "9,5\n"
    "2,5\n"
    "2,3\n"
    "7,3"
);

#define DAY "day09"

bool DEBUG = false;
bool TEST = false;

typedef Point<int> point_t;

int64_t part1 ( const vector<point_t> & data )
{
    int64_t best = 0;
    for( int i = 0; i < data.size(); i++ )
        for( int j = i+1; j < data.size(); j++ )
        {
            int64_t area =
                int64_t(abs(data[i].x-data[j].x)+1) *
                int64_t(abs(data[i].y-data[j].y)+1);
            best = max(area, best);
        }
    return best;
}

int64_t part2 ( const vector<point_t> & data )
{
    int64_t best = 0;
    for( int i = 0; i < data.size(); i++ )
        for( int j = i+1; j < data.size(); j++ )
        {
            int64_t area =
                int64_t(abs(data[i].x-data[j].x)+1) *
                int64_t(abs(data[i].y-data[j].y)+1);

            if( area < best )
                continue;

            int x1 = min( data[i].x, data[j].x );
            int x2 = max( data[i].x, data[j].x );
            int y1 = min( data[i].y, data[j].y );
            int y2 = max( data[i].y, data[j].y );

            bool maybe = true;
            for( int k = 0; k < data.size() - 1; k++ )
            {
                point_t p1 = data[k];
                point_t p2 = data[k+1];
                if( p1.x == p2.x )
                {
                    int py0 = min( p1.y, p2.y );
                    int py1 = max( p1.y, p2.y );
                    if( x1 < p1.x && p1.x < x2 && py0 <= y2 && py1 >= y1 )
                    {
                        maybe = false;
                        break;
                    }
                } else {
                    // Horizontal.
                    int px0 = min( p1.x, p2.x );
                    int px1 = max( p1.x, p2.x );
                    if( y1 < p1.y && p1.y < y2 && px0 <= x2 && px1 >= x1 )
                    {
                        maybe = false;
                        break;
                    }
                }
            }
            if( maybe )
            {
                if( DEBUG )
                    cout << area << "\t" << data[i].x << "," << data[i].y << " " << data[j].x << "," << data[j].y << "\n";
                best = area;
            }
    }
    return best;
}

int main( int argc, char ** argv )
{
    string name = *argv;
    while( *++argv )
    {
        string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg =="test")
            TEST = true;
    }

    string input = TEST ? test : file_contents(DAY".txt");

    // Construct points.

    vector<point_t> points;
    for( auto & line : split(input) )
    {
        auto p = split(line,",");
        points.emplace_back(point_t{
            stoi(p[0]),
            stoi(p[1])
        });
    }

    cout << "Part 1: " << part1(points) << "\n";
    cout << "Part 2: " << part2(points) << "\n";
}
