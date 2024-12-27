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
"###############\n"
"#...#...#.....#\n"
"#.#.#.#.#.###.#\n"
"#S#...#.#.#...#\n"
"#######.#.#.###\n"
"#######.#.#...#\n"
"#######.#.###.#\n"
"###..E#...#...#\n"
"###.#######.###\n"
"#...###...#...#\n"
"#.#####.#.###.#\n"
"#.#...#.#.#...#\n"
"#.#.#.#.#.#.###\n"
"#...#...#...###\n"
"###############"
);

bool DEBUG = false;
bool TEST = false;

typedef unsigned short byte_t;
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

typedef map<point_t,int> map_t;
point_t start;
point_t finish;

int dx[] = {-1,0,1,0};
int dy[] = { 0,-1,0,1};

map_t makemap( const string & data )
{
    set<point_t> walls;
    int x = 0;
    int y = 0;
    for( char c : data )
    {
        if( c == '\n' )
        {
            x = 0;
            y++;
            continue;
        }
        if( c == '#' )
            walls.insert( make_point(x,y) );
        else if( c == 'S' )
            start = make_point(x,y);
        else if( c == 'E' )
            finish = make_point(x,y);
        x++;
    }

    if( DEBUG )
    {
        cout << "Found " << walls.size() << " walls\n";
        cout << "Start " << getx(start) << "," << gety(start) << "\n";
        cout << "Finish " << getx(finish) << "," << gety(finish) << "\n";
    }

    map_t normals;
    point_t point = start;
    while( point != finish )
    {
        normals[point] = normals.size();
        for( int d = 0; d < 4; d++ )
        {
            byte_t x0 = getx(point) + dx[d];
            byte_t y0 = gety(point) + dy[d];
            point_t pt0 = make_point(x0,y0);
            if( 
                walls.find(pt0) == walls.end() &&
                normals.find(pt0) == normals.end()
            )
            {
                point = pt0;
                break;
            }
        }
    }
    normals[finish] = normals.size();
    return normals;
}

int mandist( point_t pt1, point_t pt2 )
{
    byte_t x1 = getx(pt1);
    byte_t y1 = gety(pt1);
    byte_t x2 = getx(pt2);
    byte_t y2 = gety(pt2);
    return abs(x2-x1) + abs(y2-y1);
}
    
int part2( map_t normal, point_t cheat, int criteria )
{
    int sumx = 0;
    map<int,int> counter;

    // For each pair of points, how much would be gained by shortcutting them?

    for( auto a : normal )
        for( auto b : normal )
        {
            if( a == b )
                continue;
            int md = mandist( a.first, b.first );
            if( md <= cheat )
            {
                int ad = b.second - a.second;
                int gain = ad - md;
                if( gain >= criteria )
                {
                    counter[gain] ++;
                    sumx += 1;
                }
            }
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

    string input = TEST ? test : file_contents("day20.txt");

    map_t normals = makemap(input);
    cout << "Part 1: " << part2(normals,  2, TEST ? 20 : 100) << "\n";
    cout << "Part 2: " << part2(normals, 20, TEST ? 50 : 100) << "\n";
}
