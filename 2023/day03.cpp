#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <array>
#include <vector>
#include <set>
#include <algorithm>
#include <numeric>

using namespace std;

bool DEBUG = false;

const char * test1 = 
"467..114..\n"
"...*......\n"
"..35..633.\n"
"......#...\n"
"617*......\n"
".....+.58.\n"
"..592.....\n"
"......755.\n"
"...$.*....\n"
".664.598.."
;

typedef vector<string> StringVector;

int W = 0;
int H = 0;

struct Delta {
    int x;
    int y;
};

Delta const dirs[8]{{-1,-1},{-1,0},{-1,1},{0,-1},{0,1},{1,-1},{1,0},{1,1}};

bool OK(char c)
{
    return isdigit(c) || c == '.';
}

bool within( int lb, int val, int rb )
{
    return lb <= val && val < rb;
}

// How long is the number at position x?

int numdigits( string & row, int x )
{
    int l;
    for( l = 0; within(0, x+l, W) && isdigit(row[x+l]); l++ )
        ;
    return l;
}

// row[x] points to the middle of a number.  Extract the number.

int extract( string & row, int x )
{
    for( ; x > 0 && isdigit(row[x-1]); x-- )
        ;
    int l = numdigits(row,x);
    return stol(row.substr(x,l));
}

int part2( int part, StringVector & data )
{
    int sumx = 0;
    for( int y = 0; y < H; y++ )
    {
        string row = data[y];
        for( int x = 0; x < W; x++ )
        {
            if( !OK(row[x]) )
            {
                set<int> nums;
                for( auto & d : dirs )
                {
                    if( 
                        within(0, x+d.x, W) && 
                        within(0, y+d.y, H) &&
                        isdigit(data[y+d.y][x+d.x])
                    )
                        nums.insert( extract(data[y+d.y], x+d.x));
                }
                if( part == 1 )
                {
                    sumx += accumulate(nums.begin(), nums.end(), 0);
                }
                else
                {
                    int p = 1;
                    for( auto n : nums )
                        p *= n;
                    sumx += p;
                }            
            }
        }
    }
    return sumx;
}

void splitem( istream & is, StringVector & lines )
{
    string line;
    while( getline( is, line ) )
        lines.push_back( line );  
}

int main( int argc, char ** argv )
{
    bool TEST = false;
    while( *++argv )
    {
        string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg =="test")
            TEST = true;
    }

    StringVector data;
    if( TEST )
    {
        istringstream iss;
        iss.str( test1 );
        splitem( iss, data );
    }
    else
    {
        ifstream ifs("day03.txt");
        splitem( ifs, data );
    }

    W = data[0].size();
    H = data.size();

    cout << "Part 1: " << part2(1,data) << "\n";
    cout << "Part 2: " << part2(2,data) << "\n";
}


