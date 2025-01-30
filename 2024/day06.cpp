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

point_t NORTH(0,-1);
point_t EAST(-1,0);
point_t SOUTH(0,1);
point_t WEST(1,0);

point_t GUARD(-1,-1);

inline point_t turn_right( const point_t in )
{
    return point_t( -in.y, in.x );
}

struct Cell {
    int walkId;
    bool blocked;
    map<point_t, bool> walked;

    Cell()
        : walkId( -1 )
        , blocked( false )
    {
        maybeResetCell( 0 );
    }

    void maybeResetCell(int newwalk)
    {
        if( walkId != newwalk )
        {
            walkId = newwalk;
            walked[NORTH] = false;
            walked[EAST] = false;
            walked[SOUTH] = false;
            walked[WEST] = false;
        }
    }
};

typedef vector<vector<Cell>> grid_t;

void parseInput( const StringVector & data, grid_t & grid )
{
    grid.resize(HEIGHT);

    for( int y=0; y < HEIGHT; y++ )
    {
        grid[y].resize(WIDTH);
        for( int x=0; x < WIDTH; x++ )
        {
            char c = data[y][x];
            if( c == '#' )
                grid[y][x].blocked = true;
            else if( c == '^' )
                GUARD = point_t(x,y);
        }
    }
}

// A "path" step includes both a coordinate and a direction.

struct step_t
{
    point_t pt;
    point_t dir;
    bool operator==( step_t & other )
    {
        return pt==other.pt && dir==other.dir;
    }
    bool operator!=( step_t & other )
    {
        return !(*this==other);
    }
};

// Ugliness warning -- this gets passed from pass 1 to pass 2.

vector<step_t> g_originalPath;

int part1( StringVector & data, grid_t & grid )
{
    point_t gpt = GUARD;
    point_t dir = NORTH;
    g_originalPath.clear();

    for(;;)
    {
        g_originalPath.push_back({gpt,dir});
        point_t npt = gpt + dir;
        if( !(between(0, npt.x, WIDTH) && between(0, npt.y, HEIGHT)) )
            break;
        if( grid[npt.y][npt.x].blocked )
            dir = turn_right(dir);
        else
            gpt = npt;
    }

    // Count the unique cells in the path.

    set<point_t> visited;
    transform(
        g_originalPath.begin(),
        g_originalPath.end(),
        inserter(visited, visited.begin()),
        [](step_t & pth) { return pth.pt; }
    );

    return visited.size();
}


int walkCandidateMap( grid_t & grid,  step_t & point )
{
    static int currentWalk = 0;
    currentWalk++;
    point_t pt = point.pt;
    point_t direction = point.dir;

    for(;;)
    {
        // We keep walking until we get blocked.
        point_t npt = pt + direction;
        if( !(between(0, npt.x, WIDTH) && between(0, npt.y, HEIGHT)) )
            break;
        if( !grid[npt.y][npt.x].blocked )
        {
            pt = npt;
            continue;
        }
        Cell & currentCell = grid[pt.y][pt.x];
        currentCell.maybeResetCell(currentWalk);
        if( currentCell.walked[direction] )
            return 1;
        currentCell.walked[direction] = true;
        direction = turn_right(direction);
    }
    return 0;
}


int part2( StringVector & data, grid_t & grid )
{
    set<point_t> checked;
    checked.insert( GUARD );
    int countOfLoopPaths = 0;
    step_t point = g_originalPath[0];
    for( auto & step : g_originalPath )
    {
        if( step != point )
        {
            point_t block = step.pt;
            if( checked.find(block) == checked.end() )
            {
                checked.insert( block );
                grid[block.y][block.x].blocked = true;
                countOfLoopPaths += walkCandidateMap(grid, point);
                grid[block.y][block.x].blocked = false;
            }
        }
        point = step;
    }

    return countOfLoopPaths;
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

    vector<vector<Cell>> grid;
    parseInput( data, grid );

    cout << "Part 1: " << part1(data,grid) << "\n";
    cout << "Part 2: " << part2(data,grid) << "\n";
}
