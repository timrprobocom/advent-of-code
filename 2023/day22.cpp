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
"1,0,1~1,2,1\n"
"0,0,2~2,0,2\n"
"0,2,3~2,2,3\n"
"0,0,4~0,2,4\n"
"2,0,5~2,2,5\n"
"0,1,6~2,1,6\n"
"1,1,8~1,1,9"
);


struct Brick
{
    int x0, y0, z0;
    int x1, y1, z1;

    static Brick make(string s)
    {
        vector<int> nums(1);
        for( char c : s )
        {
            if( isdigit(c) )
                nums.back() = nums.back()*10 + c - '0';
            else
                nums.push_back(0);
        }
        return Brick({nums[0],nums[1],nums[2],nums[3],nums[4],nums[5]});
    }
};


// How far can this brick drop?  Find the tallest brick
// below us.

#define makexy(x,y)     (((x)<<16)|(y))

typedef map<int,int> Tops;

int how_much_drop(Tops & top, Brick & brick)
{
    int peak = 0;
    for( int x = brick.x0; x <= brick.x1; x++ )
        for( int y = brick.y0; y <= brick.y1; y++ )
            peak = max(peak, top[makexy(x,y)]);
    return brick.z0-peak-1;
}


// Drop all the bricks that can be dropped.  We remember the
// highest brick for each x,y in `top`.  We sorted the bricks
// by z, so we're always building from bottom to top.

int countdrops(vector<Brick> & bricks, int except)
{
    int dropped = 0;
    Tops top;
    for( int i = 0; i < bricks.size(); i++ )
    {
        if( i == except )
            continue;

        Brick & brick = bricks[i];

        int dz = how_much_drop(top,brick);
        if( dz )
            dropped += 1;

        int z1 = brick.z1 - dz;

        // Register the new peak.

        for( int x = brick.x0; x <= brick.x1; x++ )
            for( int y = brick.y0; y <= brick.y1; y++ )
                top[makexy(x,y)] = z1;
    }
    return dropped;
}


void drop(vector<Brick> & bricks)
{
    Tops top;
    for( auto & brick : bricks )
    {
        // If it can be dropped, drop it.

        int dz = how_much_drop(top,brick);
        brick.z0 -= dz;
        brick.z1 -= dz;

        // Register the new peak.

        for( int x = brick.x0; x <= brick.x1; x++ )
            for( int y = brick.y0; y <= brick.y1; y++ )
                top[makexy(x,y)] = brick.z1;
    }
}


auto part1( vector<Brick> & bricks )
{
    int sum1 = 0;
    int sum2 = 0;

    // Eliminate all the gaps.
    drop(bricks);

    // For each brick, if we remove the brick, how many will fall?
    for( int i = 0; i < bricks.size(); i++ )
    {
        int dropped = countdrops(bricks,i);
        sum1 += !dropped;
        sum2 += dropped;
    }
    return make_tuple(sum1, sum2);
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
        buffer << ifstream("day22.txt").rdbuf();
        data = buffer.str();
    }

    istringstream parse(data);
    string line;
    vector<Brick> bricks;
    while( getline(parse,line) )
    {
        bricks.push_back(Brick::make(line));
    }

    sort( bricks.begin(), bricks.end(), [](Brick & a, Brick & b){return a.z0<b.z0;} );

    auto [p1,p2] = part1(bricks);
    cout << "Part 1: " << p1 << "\n";
    cout << "Part 2: " << p2 << "\n";
}

