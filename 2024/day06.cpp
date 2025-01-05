#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstdint>
#include <cstring>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <numeric>

#include "utils.h"

using namespace std;

const string test(
"....#.....\n"
".........#\n"
"..........\n"
"..#.......\n"
".......#..\n"
"..........\n"
".#..^.....\n"
"........#.\n"
"#.........\n"
"......#..."
);

bool DEBUG = false;
bool TEST = false;

int WIDTH = -1;
int HEIGHT = -1;

typedef Point<short> point_t;

const point_t directions[] = {    // N  E  S  W
    point_t({0,-1}),
    point_t({1,0}),
    point_t({0,1}),
    point_t({-1,0})
};

point_t find_guard( StringVector& data )
{
    for( int y=0; y < HEIGHT; y++ )
    {
        int x = data[y].find('^');
        if( x != string::npos )
            return point_t(x,y);
    }
    return point_t(-1,-1);
}

set<point_t> solve( StringVector & data )
{
    set<point_t> steps;
    set<point_t> lines[4];
    point_t g = find_guard( data );
    int dir = 0;
    for(;;)
    {
        steps.insert(g);
        lines[dir].insert(g);
        point_t n = g + directions[dir];
        if( between(0, n.x, WIDTH) && between(0, n.y, HEIGHT) )
        {
            if( lines[dir].find(n) != lines[dir].end() )
                return set<point_t>();
            else if( data[n.y][n.x] != '#' )
                g = n;
            else
                dir = (dir + 1) % 4;
        }
        else
            break;
    }
    return steps;
}

int part1( StringVector & data )
{
    return solve(data).size();
}

int part2( StringVector & data )
{
    set<point_t> visits = solve(data);
    int sums = 0;
    for( auto && pt : visits )
    {
        char c = data[pt.y][pt.x];
        data[pt.y][pt.x] = '#';
        if( solve(data).empty() )
            sums ++;
        data[pt.y][pt.x] = c;
    }
    return sums;
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

    string input = TEST ? test : file_contents("day06.txt");
    
    StringVector data = split( input, "\n");
    WIDTH = data[0].size();
    HEIGHT = data.size();

    cout << "Part 1: " << part1(data) << "\n";
    cout << "Part 2: " << part2(data) << "\n";
}
