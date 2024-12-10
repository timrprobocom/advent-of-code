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
"89010123\n"
"78121874\n"
"87430965\n"
"96549874\n"
"45678903\n"
"32019012\n"
"01329801\n"
"10456732");

bool DEBUG = false;
bool TEST = false;

typedef vector<string> StringVector;
typedef vector<vector<short>> ShortBlock;

ShortBlock parse( string src )
{
    ShortBlock sb(1);
    for( auto c : src )
    {
        if( c == '\n' )
            sb.push_back( vector<short>() );
        else
            sb.back().push_back( c-'0');
    }
    return sb;
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

Point dirs[4] = { {-1,0}, {1,0}, {0,-1}, {0,1}};

struct Record {
    short x;
    short y;
    short c;
    Record( short _x=0, short _y=0, short _c=0 )
    : x(_x), y(_y), c(_c)
    {}
};

pair<int,int> part1( ShortBlock & data )
{
    // Find the zeros.

    vector<Point> zeros;
    for( short y = 0; y < HEIGHT; y++ )
        for( short x = 0; x < WIDTH; x++ )
            if( !data[y][x] )
                zeros.push_back( Point({x,y}));
    
    queue<Record> queue;
    int part1 = 0;
    int part2 = 0;

    for( auto & z : zeros )
    {
        queue.emplace( Record(z.x,z.y,0) );
        set<Point> solutions;
        while( !queue.empty() )
        {
            Record p = queue.front();
            queue.pop();

            short c = p.c+1;
            for( auto & d : dirs )
            {
                short x0 = p.x+d.x;
                short y0 = p.y+d.y;
                if( 0 <= x0 && x0 < WIDTH && 0 <= y0 && y0 < HEIGHT && data[y0][x0] == c )
                {
                    if( c == 9 )
                    {
                        part2 ++;
                        solutions.insert( Point(x0,y0) );
                    }
                    else
                    {
                        queue.emplace( Record(x0, y0, c));
                    }
                }
            }
        }
        part1 += solutions.size();
    }
    return pair<int,int>(part1, part2);
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
        buffer << ifstream("day10.txt").rdbuf();
        input = buffer.str();
    }

    ShortBlock data = parse(input);
    WIDTH = data[0].size();
    HEIGHT = data.size();

    auto result = part1( data );
    cout << "Part 1: " << result.first << "\n";
    cout << "Part 2: " << result.second << "\n";
}
