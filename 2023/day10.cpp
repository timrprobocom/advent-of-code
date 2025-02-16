#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <vector>
#include <map>
#include <deque>
#include <tuple>
#include <algorithm>
#include <numeric>

using namespace std;

bool DEBUG = false;
bool TEST = false;

typedef vector<string> StringVector;
typedef vector<int> IntVector;
typedef vector<int64_t> LongVector;

const string test(
"..F7.\n"
".FJ|.\n"
"SJ.L7\n"
"|F--J\n"
"LJ..."
);

const string test1(
".....\n"
".S-7.\n"
".|.|.\n"
".L-J.\n"
"....."
);

const string test2(
"...........\n"
".S-------7.\n"
".|F-----7|.\n"
".||.....||.\n"
".||.....||.\n"
".|L-7.F-J|.\n"
".|..|.|..|.\n"
".L--J.L--J.\n"
"..........."
);

struct Point {
    int x;
    int y;

    bool operator==(const Point & other)
    {
        return x==other.x & y == other.y;
    }

    string str() const
    {
        ostringstream s;
        s << "(" << x << "," << y << ")";
        return s.str();
    }
};

bool operator<(const Point & a, const Point & b )
{
    if( a.x == b.x )
        return a.y < b.y;
    return a.x < b.x;
}


struct Direction {
    int dx;
    int dy;

    bool operator==(const Direction & other)
    {
        return dx==other.dx & dy == other.dy;
    }

    string str() const
    {
        ostringstream s;
        s << "(" << dx << "," << dy << ")";
        return s.str();
    }
};


Direction N({0,-1});
Direction W({-1,0});
Direction S({0,1});
Direction E({1,0});

struct TwoPoint {
    Direction p0;
    Direction p1;
};

map<char,TwoPoint> dirs;
int X = 0;
int Y = 0;
int WIDTH = 0;
int HEIGHT = 0;

void Initialize(StringVector & lines)
{
    dirs['|'].p0 = N;
    dirs['|'].p1 = S;
    dirs['-'].p0 = E;
    dirs['-'].p1 = W;
    dirs['F'].p0 = S,
    dirs['F'].p1 = E,
    dirs['L'].p0 = N;
    dirs['L'].p1 = E;
    dirs['J'].p0 = N;
    dirs['J'].p1 = W;
    dirs['7'].p0 = S;
    dirs['7'].p1 = W;

    WIDTH = lines[0].size();
    HEIGHT = lines.size();

    // Find the S.

    for( Y = 0; Y < HEIGHT; Y++ )
    {
        X = lines[Y].find('S');
        if( X != string::npos )
            break;
    }

    // What's below the S?

    vector<Direction> poss;
    if( Y > 1 )
    {
        char c = lines[Y-1][X];
        if( dirs[c].p0 == S || dirs[c].p1 == S )
            poss.push_back(N);
    }
    if( Y < HEIGHT-1 )
    {
        char c = lines[Y+1][X];
        if( dirs[c].p0 == N || dirs[c].p1 == N )
            poss.push_back(S);
    }
    if( X < WIDTH-1 )
    {
        char c = lines[Y][X+1];
        if( dirs[c].p0 == W || dirs[c].p1 == W )
            poss.push_back(E);
    }
    if( X > 1 )
    {
        char c = lines[Y][X-1];
        if( dirs[c].p0 == E || dirs[c].p1 == E )
            poss.push_back(W);
    }

    char base = '?';
    for( auto & d : dirs )
    {
        if( d.second.p0 == poss[0] && d.second.p1 == poss[1] )
        {
            base = d.first;
            break;
        }
    }

    if( DEBUG )
    {
        cout << X << "," << Y << "\n";
//        print(X,Y,poss,base)
    }

    // Replace the 'S'.

    lines[Y][X] = base;
}


void print_data( StringVector lines )
{
    cout << "\n";
    for( auto & s : lines )
        cout << s << "\n";
}


// This contains the coordinates of the loop path.

typedef map<Point,int> Path;

struct PointElem {
    int x;
    int y;
    int c;
};


int part1(StringVector & lines, Path & found)
{
    int sumx = 0;
    deque<PointElem> pending;
    pending.push_back( PointElem({X,Y,0}) );
    
    // This is a BFS.

    while( !pending.empty() )
    {
        PointElem p = pending.front();
        pending.pop_front();
        found[Point({p.x,p.y})] = p.c;
        char ch = lines[p.y][p.x];
        for( auto dxy : {dirs[ch].p0, dirs[ch].p1} )
        {
            int x0 = p.x + dxy.dx;
            int y0 = p.y + dxy.dy;
            if( 0 <= x0 && x0 < WIDTH && 
                0 <= y0 && y0 < HEIGHT &&
                found.find(Point({x0,y0})) == found.end()
            )
                pending.push_back( PointElem({x0,y0,p.c+1}) );
        }
    }
    int maxx = 0;
    for( auto & f : found )
        maxx = max(maxx,f.second);

    return maxx;
}


void blank_path( StringVector & data, Path & found )
{
    for( int y = 0; y < HEIGHT; y++ )
        for( int x = 0; x < WIDTH; x++ )
            if( found.find(Point({x,y})) == found.end() )
                data[y][x] = '.';
}


int part2( StringVector & lines, Path & found )
{
    // Erase all cells not part of the path.
    blank_path(lines,found);
    if( DEBUG )
        print_data(lines);

    // Use the winding rule.  Scanning from the left, if we have 
    // encountered an odd number of edges, then the point is inside.
     
    int cells = 0;
    for( auto row : lines )
    {
        bool inside = false;
        for( auto c : row )
        {
            if( c == 'J' || c == 'L' || c == '|' )
                inside = not inside;
            if( inside && c == '.' )
                cells += 1;
        }
    }
    return cells;
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

    StringVector lines;
    if( TEST )
    {
        istringstream data;
        data.str(test);
        string line;
        while( getline( data, line ) )
            lines.push_back( line );
    }
    else 
    {
        ifstream data("day10.txt");
        string line;
        while( getline( data, line ) )
            lines.push_back( line );
    }

    Initialize( lines );

    Path found;
    cout << "Part 1: " << part1(lines, found) << "\n";
    cout << "Part 2: " << part2(lines, found) << "\n";
}
