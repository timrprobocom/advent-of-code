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
"............\n"
"........0...\n"
".....0......\n"
".......0....\n"
"....0.......\n"
"......A.....\n"
"............\n"
"............\n"
"........A...\n"
".........A..\n"
"............\n"
"............"
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

typedef map<char, vector<Point>> spots_t;

#if 0
def printgrid(antinodes):
    grid = [list(row) for row in data]
    for x,y in antinodes:
        grid[y][x] = '#'
    for row in grid:
        print(''.join(row)) 
#endif

bool between( short low, short val, short hi )
{
    return (low <= val) && (val < hi);
}


int part1( spots_t & spots )
{
    set<Point> antinodes;
    for( auto && kv : spots )
    {
        for( int i1=0; i1 < kv.second.size(); i1 ++ )
            for( int i2=i1+1; i2 < kv.second.size(); i2 ++ )
            {
                int x0 = kv.second[i1].x;                
                int y0 = kv.second[i1].y;                
                int x1 = kv.second[i2].x;                
                int y1 = kv.second[i2].y;
                int dx = x1-x0;
                int dy = y1-y0;
                antinodes.insert( Point(x0-dx,y0-dy) );                
                antinodes.insert( Point(x1+dx,y1+dy) );                
            }
    }
    int sum = count_if( antinodes.begin(), antinodes.end(), [](const Point & pt){
        return between(0, pt.x, WIDTH) && between( 0, pt.y, HEIGHT);
    });
    return sum;
}


int part2( spots_t & spots )
{
    set<Point> antinodes;
    for( auto && kv : spots )
    {
        for( int i1=0; i1 < kv.second.size(); i1 ++ )
            for( int i2=i1+1; i2 < kv.second.size(); i2 ++ )
            {
                int x0 = kv.second[i1].x;                
                int y0 = kv.second[i1].y;                
                int x1 = kv.second[i2].x;                
                int y1 = kv.second[i2].y;
                int dx = x1-x0;
                int dy = y1-y0;
                while( between(0, x0, WIDTH) && between(0, y0, HEIGHT) )
                {
                    antinodes.insert( Point(x0,y0) );
                    x0 -= dx;
                    y0 -= dy;                
                }
                while( between(0, x1, WIDTH) && between(0, y1, HEIGHT) )
                {
                    antinodes.insert( Point(x1,y1) );
                    x1 += dx;
                    y1 += dy;                
                }
            }
    }
    return antinodes.size();
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
        buffer << ifstream("day08.txt").rdbuf();
        input = buffer.str();
    }

    StringVector data = split( input, "\n");
    WIDTH = data[0].size();
    HEIGHT = data.size();

    spots_t spots;
    for( int y = 0; y < HEIGHT; y++ )
        for( int x = 0; x < WIDTH; x++ )
            if( data[y][x] != '.' )
            {
                spots[data[y][x]].push_back( Point(x,y) );            
            }

    cout << "Part 1: " << part1(spots) << "\n";
    cout << "Part 2: " << part2(spots) << "\n";
}