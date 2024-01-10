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
"...#......\n"
".......#..\n"
"#.........\n"
"..........\n"
"......#...\n"
".#........\n"
".........#\n"
"..........\n"
".......#..\n"
"#...#....."
);


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



void expand( StringVector & lines, int delta, vector<Point> & stars )
{

    // Find the rows without galaxies.

    vector<int> nogrow( lines.size() );
    for( int y = 0; y < lines.size(); y++ )
        if( lines[y].find('#') == string::npos )
            nogrow[y] = 1;

    // Find the columns without galaxies.

    vector<int> counts( lines.front().size() );
    for( auto & row : lines )
        for( int x = 0; x < row.size(); x++ )
            if( row[x] == '#' )
                counts[x] += 1;

    vector<int> nogcol( counts.size() );
    for( int x = 0; x < counts.size(); x++ )
        if( !counts[x] )
            nogcol[x] = 1;

    stars.clear();
    int dy = 0;
    for( int y = 0; y < lines.size(); y++ )
    {
        string & row = lines[y];
        if( nogrow[y] )
        {
            dy += delta;
            continue;
        }
        int dx = 0;
        for( int x = 0; x < row.size(); x++ )
        {
            if( nogcol[x] )
                dx += delta;
            else if( row[x] == '#' )
                stars.push_back( Point({x+dx,y+dy}) );
        }
    }
}


int64_t part1( StringVector & lines, int delta )
{
    vector<Point> stars;
    expand(lines, delta-1, stars);

    int64_t mandist = 0;
    for( int i = 0; i < stars.size() - 1; i++ )
        for( int j = i; j < stars.size(); j++ )
            mandist += abs(stars[i].x-stars[j].x) + abs(stars[i].y-stars[j].y);

    return mandist;
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
        ifstream data("day11.txt");
        string line;
        while( getline( data, line ) )
            lines.push_back( line );
    }

    cout << "Part 1: " << part1(lines, 2) << "\n";
    if( TEST )
    {
        cout << "Test 10: " << part1(lines, 10) << "\n";
        cout << "Test 100: " << part1(lines, 100) << "\n";
    }
    cout << "Part 2: " << part1(lines, 1000000) << "\n";
}
