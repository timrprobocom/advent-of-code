#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <cstdint>
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
"...........\n"
".....###.#.\n"
".###.##..#.\n"
"..#.#...#..\n"
"....#.#....\n"
".##..S####.\n"
".##..#...#.\n"
".......##..\n"
".##.#.####.\n"
".##..##.##.\n"
"..........."
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
    int dx = getdx(d);
    int dy = getdy(d);
    return makedir(-dx,-dy);
}


struct Point {
    int x;
    int y;

    bool operator==(const Point & other)
    {
        return x==other.x & y == other.y;
    }
};

bool operator<(const Point & a, const Point & b )
{
    if( a.x == b.x )
        return a.y < b.y;
    return a.x < b.x;
}


Point origin;

void parse( string & data, StringVector & grid )
{
    istringstream parse(data);
    string line;
    while( getline( parse, line ) )
    {
        int i = line.find('S');
        if( i != string::npos )
        {
            origin.x = i;
            origin.y = grid.size();
        }
        grid.push_back( line );
    }
}

// 40 rocks in test
// 2290 rocks in real
            
Direction directions[4] = {U,L,D,R};

int64_t part1( StringVector & grid )
{
    int steps = TEST ? 6 : 64;
    deque<Point> queue;
    set<Point> newq;
    queue.push_back(origin);
    for( int i = 0; i < steps; i++ )
    {
        newq.clear();
        while( !queue.empty() )
        {
            Point p = queue.front();
            queue.pop_front();
            for( auto dir : directions )
            {
                int x1 = p.x+getdx(dir);
                int y1 = p.y+getdy(dir);
                Point pt({x1,y1});
                if( 0 <= x1 && x1 < WIDTH && 0 <= y1 && y1 < HEIGHT && grid[y1][x1] != '#' )
                    newq.insert(pt);
            }
        }
        queue.resize(newq.size());
        copy( newq.begin(), newq.end(), queue.begin() );
    }
    return queue.size();
}


int64_t part2( StringVector & grid )
{
// Once we get past an initial start up time, The number of cells at
// each multiple of the grid width, is quadratic.  If the 2nd derivative
// is N, then the first derivative is k
//  f''(x) = N
//  f'(x)  = Nx + b
//  f(x)   = (N/2)x**2 + bx + c
//
// If you look up how to derive a quadratic from differences, you'll find
//  a = d2[0]/2
//  b = d1[0] - 3a
//  c = d0[0] - a - b
// Oddly, this starts counting with 1, so we have to compensate for that.
//
// We gather the counts where (step % width) == (steps % width), so we're
// always at the same point in the cycle.  Note that the offset is where
// the S is, so we're sampling just as we reach the edge of a grid.
//
// It takes about 45 seconds to compute enough differences to ensure
// we know the second differences have stabilized.

    int steps = TEST ? 5000 : 26501365;
    int offset = steps % WIDTH;
    IntVector nums;
    IntVector diff1;
    IntVector diff2;

    deque<Point> queue;
    set<Point> newq;
    queue.push_back(origin);
    for( int i = 0; i < steps; i++ )
    {
        if( i % WIDTH == offset )
        {
            nums.push_back(queue.size());
            if( nums.size() > 1 )
                diff1.push_back( nums[nums.size()-1]-nums[nums.size()-2] );
            if( diff1.size() > 1 )
                diff2.push_back( diff1[diff1.size()-1]-diff1[diff1.size()-2] );
            if( DEBUG )
            {
                cout << i << " [";
                for( int n : nums ) cout << n << ", ";
                cout << "] [";
                for( int n : diff1 ) cout << n << ", ";
                cout << "] [";
                for( int n : diff2 ) cout << n << ", ";
                cout << "]\n";
            }
            if( diff2.size() > 1 && diff2[diff2.size()-1] == diff2[diff2.size()-2] )
                break;
        }
        newq.clear();
        while( !queue.empty() )
        {
            Point p = queue.front();
            queue.pop_front();
            for( auto dir : directions )
            {
                int x1 = p.x+getdx(dir);
                int y1 = p.y+getdy(dir);
                int x2 = (x1 < 0 ? (x1%WIDTH+WIDTH) : x1) % WIDTH;
                int y2 = (y1 < 0 ? (y1%HEIGHT+HEIGHT) : y1) % HEIGHT;
                if( grid[y2][x2] != '#' )
                    newq.insert(Point({x1,y1}));
            }
        }

        queue.resize(newq.size());
        copy( newq.begin(), newq.end(), queue.begin() );
    }
    
    // Use the first and second differences to find the quadratic
    // coefficients.

    int64_t skips = nums.size() - 4;
    int64_t a = diff2[skips] / 2;
    int64_t b = diff1[skips] - 3*a;
    int64_t c = nums[skips] - a - b;
    if(DEBUG)
        cout << skips << ", " << a << ", " << b << ", " << c << "\n";
    int64_t n = steps/WIDTH-skips+1;
    return (a * n + b) * n + c;
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
        buffer << ifstream("day21.txt").rdbuf();
        data = buffer.str();
    }

    WIDTH = data.find('\n');
    HEIGHT = (data.size()+1)/(WIDTH+1);

    StringVector grid;
    parse( data, grid );

    cout << "Part 1: " << part1(grid) << "\n";
    cout << "Part 2: " << part2(grid) << "\n";
}


