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


typedef unsigned short Direction;

#define makedir(dx,dy) (((dx+1)<<4) | (dy+1))
#define getdx(dir)     ((dir>>4)-1)
#define getdy(dir)     ((dir&15)-1)

Direction N = makedir(0,-1);
Direction W = makedir(-1,0);
Direction S = makedir(0,1);
Direction E = makedir(1,0);

Direction change( char c, Direction d )
{
    int dx = getdx(d);
    int dy = getdy(d);
    return c == '/' ?  makedir(-dy,-dx) : makedir(dy,dx);
}


typedef int Beam;

Beam makebeam( int x, int y, Direction  dir )
{
    return (x << 16) | (y << 8) | dir;
}

#define getx(beam)      (beam >> 16)
#define gety(beam)      ((beam >> 8) & 255)
#define getdir(beam)    (beam & 255)


void printg(set<Beam> & seen)
{
    string s(WID, '.');
    StringVector grid(HGT, s);
    cout << "\n";
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
int k=0;

    while( !beams.empty() )
    {
k += 1;
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
        x += getdx(dir);
        y += getdy(dir);
        if( 0 <= x && x < WID && 0 <= y && y < HGT )
            beams.push_back( makebeam(x,y,dir) );
    }

    if( DEBUG )
        printg(seen);
    set<int> gather;
    for( auto & b : seen )
        gather.insert( b >> 8 );
cout << start << " " << k << "\n";
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
