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

typedef vector<string> StringVector;

StringVector split( string src, string delim )
{
    StringVector sv;
    for( int j = src.find(delim); j != -1; )
    {
        sv.push_back( src.substr(0,j) );
        src = src.substr(j+delim.size());
        j = src.find(delim);
    }
    sv.push_back(src);
    return sv;
}

int WIDTH = -1;
int HEIGHT = -1;

struct Point {
    short x;
    short y;

    Point( short _x=0, short _y=0)
    : x(_x), y(_y)
    {}

    bool operator<(const Point & other) const
    {
        return ((x << 16) | y) < ((other.x << 16) | other.y);
    }

    bool operator==(const Point & other) const
    {
        return x==other.x && y == other.y;
    }
};

const Point directions[] = {    // N  E  S  W
    Point({0,-1}),
    Point({1,0}),
    Point({0,1}),
    Point({-1,0})
};

Point find_guard( StringVector& data )
{
    for( int y=0; y < HEIGHT; y++ )
    {
        int x = data[y].find('^');
        if( x != string::npos )
            return Point(x,y);
    }
    return Point(-1,-1);
}

set<Point> solve( StringVector & data )
{
    set<Point> steps;
    set<Point> lines[4];
    Point g = find_guard( data );
    int dir = 0;
    for(;;)
    {
        steps.insert(g);
        lines[dir].insert(g);
        Point n(
            g.x + directions[dir].x,
            g.y + directions[dir].y
        );
        if( 0 <= n.x && n.x < WIDTH && 0 <= n.y && n.y < HEIGHT )
        {
            if( lines[dir].find(n) != lines[dir].end() )
                return set<Point>();
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
    set<Point> visits = solve(data);
    int sums = 0;
    for( auto && pt : visits )
    {
        data[pt.y][pt.x] = '#';
        if( solve(data).empty() )
            sums ++;
        data[pt.y][pt.x] = '.';
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

    string input;
    if( TEST )
    {
        input = test;
    }
    else 
    {
        stringstream buffer;
        buffer << ifstream("day06.txt").rdbuf();
        input = buffer.str();
    }

    StringVector data = split( input, "\n");
    WIDTH = data[0].size();
    HEIGHT = data.size();

    cout << "Part 1: " << part1(data) << "\n";
    cout << "Part 2: " << part2(data) << "\n";
}
