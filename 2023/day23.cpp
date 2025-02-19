#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <cstdint>
#include <vector>
#include <map>
#include <set>
#include <array>
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

const string test(
"#.#####################\n"
"#.......#########...###\n"
"#######.#########.#.###\n"
"###.....#.>.>.###.#.###\n"
"###v#####.#v#.###.#.###\n"
"###.>...#.#.#.....#...#\n"
"###v###.#.#.#########.#\n"
"###...#.#.#.......#...#\n"
"#####.#.#.#######.#.###\n"
"#.....#.#.#.......#...#\n"
"#.#####.#.#.#########v#\n"
"#.#...#...#...###...>.#\n"
"#.#.#v#######v###.###v#\n"
"#...#.>.#...>.>.#.###.#\n"
"#####v#.#.###v#.#.###.#\n"
"#.....#...#...#.#.#...#\n"
"#.#########.###.#.#.###\n"
"#...###...#...#...#.###\n"
"###.###.#.###v#####v###\n"
"#...#...#.#.>.>.#.>.###\n"
"#.###.###.#.###.#.#v###\n"
"#.....###...###...#...#\n"
"#####################.#"
);

int WIDTH = 0;
int HEIGHT = 0;

typedef unsigned short Direction;

#define makedir(dx,dy) (((dx+1)<<4) | (dy+1))
#define getdx(dir)     ((dir>>4)-1)
#define getdy(dir)     ((dir&15)-1)

Direction U = makedir(0,-1);
Direction L = makedir(-1,0);
Direction D = makedir(0,1);
Direction R = makedir(1,0);

Direction backward( Direction d )
{
    short dx = getdx(d);
    short dy = getdy(d);
    return makedir(-dx,-dy);
}

array<Direction,4> directions{U,L,D,R};

enum {
    UU = 1,
    LL = 2,
    DD = 4,
    RR = 8
};

struct Point {
    short x;
    short y;

    bool operator==(const Point & other)
    {
        return x==other.x && y == other.y;
    }
};

bool operator<(const Point & a, const Point & b )
{
    if( a.x == b.x )
        return a.y < b.y;
    return a.x < b.x;
}

Point START({1,0});
Point TARGET;

typedef map<Point,short> ValidMap;

// Construct a map of the valid directions from any given point.

void parse( string & data, StringVector & grid, ValidMap & valid1, ValidMap & valid2 )
{
    istringstream parse(data);
    string line;
    while( getline( parse, line ) )
    {
        short y = grid.size();
        grid.push_back( line );
        for( short x = 0; x < line.size(); x++ )
        {
            char c = line[x];
            if( c != '#' )
                valid2[Point({x,y})] = UU|RR|DD|LL;
            if( c == '.' )
                valid1[Point({x,y})] = UU|RR|DD|LL;
            else if( c == '>' )
                valid1[Point({x,y})] = RR;
            else if( c == 'v' )
                valid1[Point({x,y})] = DD;
        };
    }
    WIDTH = grid[0].size();
    HEIGHT = grid.size();
    TARGET.x = WIDTH-2;
    TARGET.y = HEIGHT-1;
}

// Make an adjacency graph.

typedef map<Point,int> PathMap;
typedef map<Point,PathMap> AdjacencyGraph;

AdjacencyGraph make_graph(const StringVector & data, ValidMap & valid)
{
    AdjacencyGraph graph;
    for( short y = 0; y < HEIGHT; y++ )
        for( short x = 0; x < WIDTH; x++ )
        {
            Point pt({x,y});
            if( valid.find(pt) != valid.end() )
            {
                short possible = valid[pt];
                PathMap adj;
                for( int i = 0; i < 4; i++ )
                {
                    if( valid[pt] & (1<<i) )
                    {
                        short x1 = x + getdx(directions[i]);
                        short y1 = y + getdy(directions[i]);
                        Point pt1({x1,y1});
                        if( valid.find(pt1) != valid.end() )
                            adj[pt1] = 1;
                    }
                }
                graph[pt] = adj;
            }
        }
    return graph;
}

struct Tracking {
    Point pt;
    int length;
    set<Point> seen;
};

// Optimize the graph by just connecting the hubs.

AdjacencyGraph optimize_graph(AdjacencyGraph & graph)
{
    set<Point> hubs;
    hubs.insert( START );
    hubs.insert( TARGET );
    for( auto & kv : graph )
    {
        if( kv.second.size() > 2 )
            hubs.insert( kv.first );
    }

    if( DEBUG )
        cout << "Found " << hubs.size() << " hubs\n";

    // For each hub, find the next hubs in line.

    AdjacencyGraph newgraph;
    for( auto & hub : hubs )
    {
        PathMap adj;
        deque<Tracking> queue;
        queue.push_back( Tracking({hub,1,set<Point>()}) );

        while( !queue.empty() )
        {
            Tracking t = queue.front();
            queue.pop_front();
            // Can this ever happen?
            if( t.seen.find(t.pt) != t.seen.end() )
                continue;
            set<Point> seen = t.seen;
            seen.insert( t.pt );
            for( auto & kv : graph[t.pt] )
            {
                const Point & pt2 = kv.first;
                if( seen.find(pt2) == seen.end() )
                {
                    if( hubs.find(pt2) != hubs.end() )
                        adj[pt2] = t.length;
                    else
                        queue.push_back( Tracking({pt2,t.length+1,seen}) );
                }
            }
        }
        newgraph[hub] = adj;
    }
    return newgraph;
}

struct Traverse {
    Point pt;
    int cost;
};

int64_t traverse(AdjacencyGraph & graph)
{
    vector<Traverse> queue;
    queue.push_back( Traverse({START,0}) );
    int maxsize = 0;
    set<Point> seen;
    while( !queue.empty() )
    {
        Traverse t = queue.back();
        queue.pop_back();
        if( t.cost < 0 )
            seen.erase( t.pt );
        else if ( t.pt == TARGET )
        {
            if( t.cost > maxsize )
            {
                maxsize = t.cost;
                if( DEBUG )
                    cout << queue.size() << " " << maxsize << "\n";
            }
        }
        else if( seen.find(t.pt) == seen.end() )
        {
            seen.insert(t.pt);
            queue.push_back( Traverse({t.pt, -1}) );
            for( auto & g : graph[t.pt] )
                queue.push_back( Traverse({g.first, t.cost+g.second}) );
        }
    }
    return maxsize;
}




int64_t part1( StringVector & grid, ValidMap & valid )
{
    AdjacencyGraph graph = make_graph(grid,valid);
    graph = optimize_graph(graph);
    return traverse(graph);
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

    string data;
    if( TEST )
    {
        data = test;
    }
    else 
    {
        stringstream buffer;
        buffer << ifstream("day23.txt").rdbuf();
        data = buffer.str();
    }


    StringVector grid;
    ValidMap valid1;
    ValidMap valid2;
    parse( data, grid, valid1, valid2 );

    cout << "Part 1: " << part1(grid,valid1) << "\n"; // 2154
    cout << "Part 2: " << part1(grid,valid2) << "\n"; // 6654
}

