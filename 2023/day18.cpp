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

const string test(
"R 6 (#70c710)\n"
"D 5 (#0dc571)\n"
"L 2 (#5713f0)\n"
"D 2 (#d2c081)\n"
"R 2 (#59c680)\n"
"D 2 (#411b91)\n"
"L 5 (#8ceee2)\n"
"U 2 (#caa173)\n"
"L 1 (#1b58a2)\n"
"U 2 (#caa171)\n"
"R 2 (#7807d2)\n"
"U 3 (#a77fa3)\n"
"L 2 (#015232)\n"
"U 2 (#7a21e3)"
);


typedef unsigned short Direction;

#define makedir(dx,dy) (((dx+1)<<4) | (dy+1))
#define getdx(dir)     ((dir>>4)-1)
#define getdy(dir)     ((dir&15)-1)

Direction U = makedir(0,-1);
Direction L = makedir(-1,0);
Direction D = makedir(0,1);
Direction R = makedir(1,0);

map<char,Direction> directions;

Direction backward( Direction d )
{
    int dx = getdx(d);
    int dy = getdy(d);
    return makedir(-dx,-dy);
}

void Initialize()
{
    directions['R'] = R;
    directions['L'] = L;
    directions['U'] = U;
    directions['D'] = D;
    directions['0'] = R;
    directions['1'] = D;
    directions['2'] = L;
    directions['3'] = U;
}


int64_t part1( int part, string & data )
{

// This implements Gauss's "shoelace formula" for computing the area of
// a polygon described by its vertex coordinates.  "Shoelace" would 
// normally accumulate both x*dy and y*dx, but since the sides are all
// horizontal and vertical, the sums are the same.

    int64_t area = 0;
    int64_t perim = 0;
    int x=0;
    int y=0;

    string word0;
    string word1;

    istringstream parse(data);
    string word;
    while( parse >> word )
    {
        if( isdigit(word[0]) )
            word1 = word;
        else if( word.size() == 1 )
            word0 = word;
        else
        {
            Direction dir;
            int dist;

            if( part == 1 )
            {
                dist = stoi(word1);
                dir = directions[word0[0]];
            }
            else
            {
                dist = stoi(word.substr(2,5), nullptr, 16);
                dir = directions[word[7]];
            }
            
            int64_t dx = dist * getdx(dir);
            int64_t dy = dist * getdy(dir);
            area += x * dy;
            perim += dist;
            x += dx;
            y += dy;
        }
    }
    if( DEBUG )
        cout << area << " " << perim << "\n";

    return area + perim / 2 + 1;
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
        buffer << ifstream("day18.txt").rdbuf();
        data = buffer.str();
    }

    Initialize();

    cout << "Part 1: " << part1(1,data) << "\n";
    cout << "Part 2: " << part1(2,data) << "\n";
}
