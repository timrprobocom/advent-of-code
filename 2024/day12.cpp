#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
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
"RRRRIICCFF\n"
"RRRRIICCCF\n"
"VVRRRCCFFF\n"
"VVRCCCJFFF\n"
"VVVVCJJCFE\n"
"VVIVCCJJEE\n"
"VVIIICJJEE\n"
"MIIIIIJJEE\n"
"MIIISIJEEE\n"
"MMMISSJEEE"
);

bool DEBUG = false;
bool TEST = false;
#define DAY "day12"

int WIDTH = -1;
int HEIGHT = -1;

typedef Point<short> point_t;

point_t dirs[] = {
    point_t(-1,0),
    point_t(0,1),
    point_t(0,-1),
    point_t(1,0)
};

set<point_t> getregion( set<point_t> & region, point_t xy )
{
    queue<point_t> q;
    q.push( xy );
    set<point_t> found;
    found.insert( xy );

    while( !q.empty() )
    {
        point_t xy = q.front();
        q.pop();
        for( auto dxy : dirs )
        {
            point_t xy0 = xy + dxy;
            if( region.find(xy0) != region.end() && found.find(xy0) == found.end() )
            {
                found.insert( xy0 );
                q.push(xy0);
            }
        }
    }
    return found;
}

vector<set<point_t>> distinctsets( set<point_t> & region )
{
    vector<set<point_t>> regions;
    while( !region.empty() )
    {
        point_t xy = region.extract(region.begin()).value();
        set<point_t> newreg = getregion( region, xy );
        regions.push_back( newreg );
        for( auto pt : newreg )
            region.erase( pt );
    }
    return regions;
}

// Return the sum of points in the region that have a neighbor NOT in the region.

int perimeter( set<point_t> & region )
{
    int sum = 0;
    for( auto & xy : region )
        for( auto & dxy : dirs )
            sum += region.find(xy+dxy) == region.end();
    return sum;
};

// Find all of the border edges.  This includes all of the sides where they border, so
// it includes and x,y and a direction.

set<pair<point_t,point_t>> find_border( set<point_t> region )
{
    set<pair<point_t,point_t>> border;
    for( auto & xy : region )
    {
        for( auto & dxy : dirs )
        {
            if( 
                0 <= xy.x && xy.x < WIDTH &&
                0 <= xy.y && xy.y < HEIGHT &&
                region.find(xy+dxy) == region.end()
            )
                border.insert( pair(xy,dxy) );
        }
    }
    return border;
}

// Looking in a direction perpendicular to the outside edge(s), remove any edges
// that are also on the same border.

int sides( set<pair<point_t,point_t>> border )
{
    int sides = 0;
    while( !border.empty() )
    {
        auto xydxy = border.extract(border.begin()).value();
        point_t xy = xydxy.first;
        point_t dxy = xydxy.second;
        point_t perp[] = {
            point_t(-dxy.y,dxy.x),
            point_t(dxy.y,-dxy.x)
        };

        for( auto & pdxy : perp )
        {
            auto xy0 = pair(xy+pdxy, dxy);
            while( border.find(xy0) != border.end() )
            {
                border.erase(xy0);
                xy0.first += pdxy;
            }
        }

        sides ++;
    }
    return sides;
}

int64_t part1(vector<set<point_t>> & regions )
{
    return std::accumulate(
        regions.begin(),
        regions.end(),
        0ll,
        [](int64_t sum,set<point_t> & v){
            return sum + v.size() * perimeter(v);
        }
    );
}

int64_t part2(vector<set<point_t>> & regions )
{
    return std::accumulate(
        regions.begin(),
        regions.end(),
        0ll,
        [](int64_t sum,set<point_t> & v){
            set<pair<point_t, point_t>> border = find_border(v);
            return sum + v.size() * sides(border);
        }
    );
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

    string input = TEST ? test : file_contents(DAY".txt");
    StringVector grid = split(input);
    WIDTH = grid[0].size();
    HEIGHT = grid.size();

    // Process the map.  First, collect all similar cells.  Then, split letters thatn
    // have multiple distinct regions.

    map<char,set<point_t>> stats;
    for( int y = 0; y < HEIGHT; y++ )
        for( int x = 0; x < WIDTH; x++ )
            stats[grid[y][x]].insert( point_t(x,y) );

    vector<set<point_t>> regions;
    for( auto kv : stats )
        for( auto s : distinctsets(kv.second) )
            regions.push_back( s );

    if( DEBUG )
    {
        for( auto & v : regions )
        {
            for( auto & pt : v  )
                cout << "(" << pt.x << "," << pt.y << ") ";
            cout << "\n";
        }
    }

    cout << "Part 1: " << part1(regions) << "\n";
    cout << "Part 2: " << part2(regions) << "\n";
}
