#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <numeric>

using namespace std;

bool DEBUG = false;
bool TEST = false;

typedef vector<string> StringVector;
typedef vector<int> IntVector;
typedef vector<int64_t> LongVector;
typedef vector<vector<uint8_t>> ByteGrid;

// I have replaced the backslashes with % here to avoid nonsense.

const string test(
"2413432311323\n"
"3215453535623\n"
"3255245654254\n"
"3446585845452\n"
"4546657867536\n"
"1438598798454\n"
"4457876987766\n"
"3637877979653\n"
"4654967986887\n"
"4564679986453\n"
"1224686865563\n"
"2546548887735\n"
"4322674655533"
);


int WID = 0;
int HGT = 0;

// Parse the input.

void parse( istream & fin, ByteGrid & grid )
{
    int c;
    grid.resize(1);
    while( (c = fin.get()) != EOF )
    {
        if( c == '\n' )
            grid.resize(grid.size() + 1);
        else
            grid.back().push_back( c-'0' );
    }
}


typedef unsigned short Direction;

#define makedir(dx,dy) (((dx+1)<<4) | (dy+1))
#define getdx(dir)     ((dir>>4)-1)
#define getdy(dir)     ((dir&15)-1)

Direction N = makedir(0,-1);
Direction W = makedir(-1,0);
Direction S = makedir(0,1);
Direction E = makedir(1,0);

Direction backward( Direction d )
{
    int dx = getdx(d);
    int dy = getdy(d);
    return makedir(-dx,-dy);
}


typedef int Location;

Location makeloc( int x, int y, Direction  dir )
{
    return (x << 16) | (y << 8) | dir;
}

#define getx(loc)      (loc >> 16)
#define gety(loc)      ((loc >> 8) & 255)
#define getdir(loc)    (loc & 255)


struct State
{
    int cost;
    int x;
    int y;
    Direction dir;
};

bool operator< (const State & a, const State & b )
{
    return a.cost > b.cost;
}

// This is a Dijkstra search.

int part1( ByteGrid & grid, int mind, int maxd )
{
    array<Direction,4> alldirs({N,E,S,W});
    int cost = 0;

    // Accum cost, X, Y, direction.  Cost has to be first so the dijkstra pop
    // gets the best choice so far.
    priority_queue<State> points;
    points.push(State({0,0,0,makedir(0,0)}));
    set<Location> seen;
    // At each step, we can go 1 and turn, or 2 and turn, or 3 and turn.
    while( !points.empty() )
    {
        State s = points.top();
        points.pop();

        // If we hit the exit, yahoo.

        if( s.x == WID-1 && s.y == HGT-1 )
            return s.cost;

        // If we've been here before, bail.

        Location loc = makeloc(s.x,s.y,s.dir);
        if( seen.find(loc) != seen.end() )
            continue;
        seen.insert(loc);

        if( DEBUG )
            cout << "Node score=" << s.cost << " y=" << s.y << " x=" << s.x << " dir=" << s.dir << "\n";

        // Check all possible directions.  We can't go the way we were going,
        // and we can't go back the way we came.

        for( Direction direction : alldirs )
        {
            if( direction == s.dir || direction == backward(s.dir) )
                continue;
            int dcost = 0;
            for( int distance = 1; distance < maxd+1; distance++ )
            {
                int xx = s.x + getdx(direction) * distance;
                int yy = s.y + getdy(direction) * distance;
                if( xx < 0 || xx >= WID || yy < 0 || yy >= HGT )
                    break;
                dcost += grid[yy][xx];
                if( distance >= mind )
                {
                    int newc = s.cost + dcost;
                    points.push(State({newc,xx,yy,direction}));
                }
            }
        }
    }
    return -1;
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

    ByteGrid grid;
    if( TEST )
    {
        istringstream data;
        data.str(test);
        parse(data, grid);
    }
    else 
    {
        ifstream data("day17.txt");
        parse(data, grid);
    }

    WID = grid[0].size();
    HGT = grid.size();

    cout << "Part 1: " << part1(grid,1,3) << "\n";
    cout << "Part 2: " << part1(grid,4,10) << "\n";
}
