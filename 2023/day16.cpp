#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <vector>
#include <map>
#include <set>
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

// I have replaced the backslashes with % here to avoid nonsense.

const string test(
".|...%....\n"
"|.-.%.....\n"
".....|-...\n"
"........|.\n"
"..........\n"
".........%\n"
"..../.%%..\n"
".-.-/..|..\n"
".|....-|.%\n"
"..//.|...."
);


int WID = 0;
int HGT = 0;

// Parse the input.

void parse( istream & fin, StringVector & lines )
{
    string line;
    while( getline( fin, line ) )
    {
        replace( line.begin(), line.end(), '%', '\\' );
        lines.push_back(line);
    }
}


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

bool operator<(const Direction & a, const Direction & b )
{
    if( a.dx == b.dx )
        return a.dy < b.dy;
    return a.dx < b.dx;
}


Direction N({0,-1});
Direction W({-1,0});
Direction S({0,1});
Direction E({1,0});

map<Direction,Direction> fslash;
map<Direction,Direction> bslash;

Direction change( char c, Direction d )
{
    if( fslash.empty() )
    {
        fslash[N] = E;
        fslash[S] = W;
        fslash[E] = N;
        fslash[W] = S;
        bslash[N] = W;
        bslash[S] = E;
        bslash[E] = S;
        bslash[W] = N;
    }

    return c == '/' ? fslash[d] : bslash[d];
}


#if 0
struct Beam {
    int x;
    int y;
    Direction dir;

    int hash() const {
        return (x << 16) | (y << 8) | ((dir.dx+1) << 4) | (dir.dy+1);
    };
};


bool operator<(const Beam & a, const Beam & b )
{
    return a.hash() < b.hash();
}
#endif
typedef int Beam;

Beam makebeam( int x, int y, Direction & dir )
{
    return (x << 16) | (y << 8) | ((dir.dx+1) << 4) | (dir.dy+1);
}

#define getx(beam)      beam >> 16
#define gety(beam)      (beam >> 8) & 255
#define getdir(beam)    Direction({(beam>>4)&15-1,beam&15-1})

void print( StringVector & grid )
{
    cout << "----\n";
    for( auto & s : grid )
        cout << s << "\n";
}


void printg(set<Beam> & seen)
{
    string s(WID, '.');
    StringVector grid(HGT, s);
    for( auto & p : seen )
        grid[gety(p)][getx(p)] = '#';
    for( auto & row : grid )
        cout << row << "\n";
}


int process(StringVector & grid, Beam start )
{
    deque<Beam> beams;
    beams.push_back(start);
    set<Beam> seen;

    while( !beams.empty() )
    {
        Beam beam = beams.front();
        beams.pop_front();
        if( seen.find(beam) != seen.end() )
            continue;

        seen.insert(beam);
        int x = getx(beam);
        int y = gety(beam);
        Direction dir = getdir(beam);

        char c = grid[y][x];
        if( c == '/' || c == '\\' )
        {
            dir = change(c, dir);
        }
        else if( c == '|' && (dir == E || dir == W))
        {
            if( y > 0 )
                beams.push_back( makebeam(x,y-1,N) );
            dir = S;
        }
        else if( c == '-' && (dir == N || dir == S))
        {
            if( x > 0 )
                beams.push_back( makebeam(x-1,y,W) );
            dir = E;
        }
        x += dir.dx;
        y += dir.dy;
        if( 0 <= x && x < WID && 0 <= y && y < HGT )
            beams.push_back( makebeam(x,y,dir) );
    }

    if( DEBUG )
        printg(seen);
    set<int> gather;
    for( auto & b : seen )
        gather.insert( b >> 8 );
    return gather.size();
}


int part1( StringVector & grid )
{
    return process(grid, makebeam(0,0,E) );
}


int part2( StringVector & grid )
{
    int ener = 0;
    for( int y = 0; y < HGT; y++ )
    {
        ener = max( ener, process(grid, makebeam(0,    y,E)));
        ener = max( ener, process(grid, makebeam(WID-1,y,W)));
    }
    for( int x = 0; x < WID; x++ )
    {
        ener = max( ener, process(grid, makebeam(x,    0,S)));
        ener = max( ener, process(grid, makebeam(x,HGT-1,N)));
    }
    return ener;
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
        parse(data, lines);
    }
    else 
    {
        ifstream data("day16.txt");
        parse(data, lines);
    }

    WID = lines[0].size();
    HGT = lines.size();

    cout << "Part 1: " << part1(lines) << "\n";
    cout << "Part 2: " << part2(lines) << "\n";
}
