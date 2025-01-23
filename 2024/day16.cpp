#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <string>
#include <iterator>
#include <cstdint>
#include <cstring>
#include <cmath>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <numeric>

#include "utils.h"

using namespace std;

const string test(
"###############\n"
"#.......#....E#\n"
"#.#.###.#.###.#\n"
"#.....#.#...#.#\n"
"#.###.#####.#.#\n"
"#.#.#.......#.#\n"
"#.#.#####.###.#\n"
"#...........#.#\n"
"###.#.#####.#.#\n"
"#...#.....#.#.#\n"
"#.#.#.###.#.#.#\n"
"#.....#...#.#.#\n"
"#.###.#.#.#.#.#\n"
"#S..#.....#...#\n"
"###############"
);

const string test2(
"#################\n"
"#...#...#...#..E#\n"
"#.#.#.#.#.#.#.#.#\n"
"#.#.#.#...#...#.#\n"
"#.#.#.#.###.#.#.#\n"
"#...#.#.#.....#.#\n"
"#.#.#.#.#.#####.#\n"
"#.#...#.#.#.....#\n"
"#.#.#####.#.###.#\n"
"#.#.#.......#...#\n"
"#.#.###.#####.###\n"
"#.#.#...#.....#.#\n"
"#.#.#.#####.###.#\n"
"#.#.#.........#.#\n"
"#.#.#.#########.#\n"
"#S#.............#\n"
"#################\n"
);

bool DEBUG = false;
bool TEST = false;
#define DAY "day16"

typedef Point<short> point_t;

point_t left(const point_t pt)
{
    return point_t( pt.y, -pt.x );
}

point_t right(const point_t pt)
{
    return point_t( -pt.y, pt.x );
}

bool startswith( string & haystack, string needle )
{
    return haystack.substr(0, needle.size()) == needle;
}

// This is quicker than the map of points.

vector<string> lines;

bool is_wall( point_t pt )
{
    return lines[pt.y][pt.x] == '#';
}

void printgrid( set<point_t> & path )
{
    for( int y = 0; y < lines.size(); y++ )
    {
        for( int x = 0; x < lines[y].size(); x++ )
        {
            if( is_in( point_t(x,y), path ) )
                cout << 'O';
            else
                cout << lines[y][x];
        }
        cout << "\n";
    }
}

void printgrid( vector<point_t> & path )
{
    set<point_t> xpath( path.begin(), path.end() );
    printgrid( xpath );
}

// Cheating; we build this in part1 and use it in part2.

map<point_t, int> scores;

int part1( point_t start, point_t finish )
{
    typedef tuple< int, point_t, point_t > queue1_t;
    queue<queue1_t> q;
    q.push( queue1_t(0, start, point_t(1,0)) );
    scores[start] = 0;

    // This is a simple BFS.

    while( !q.empty() )
    {
        auto [score, point, dir] = q.front();
        q.pop();
        if( DEBUG )
            cout << score << " " << q.size() << " \r" << flush;

        for( auto d2 : { dir, right(dir), left(dir) } )
        {
            int pain = d2 == dir ? 1 : 1001;
            point_t p2 = point + d2;
            if( !is_wall(p2) )
            {
                auto v = scores.find(p2);
                if( v == scores.end() || v->second > score+pain )
                {
                    scores[p2] = score+pain;
                    q.push( tuple( score+pain, p2, d2));
                }
            }
        }
    }
    return scores[finish];
}

int part2( point_t start, point_t finish )
{
    typedef tuple< int, point_t, point_t > queue1_t;
    queue<queue1_t> q;
    q.push( queue1_t(scores[finish], finish, point_t(-1,0)) );
    q.push( queue1_t(scores[finish], finish, point_t(0,1)) );
    set<point_t> goods;
    goods.insert(finish);

    // Do a BFS backwards.  We keep going as long as the score keeps going down.
 
    while( !q.empty() )
    {
        auto [score, point, dir] = q.front();
        q.pop();
        if( DEBUG )
            cout << point.x << "," << point.y << " " << score << "\n" << flush;

        for( auto d2 : { dir, right(dir), left(dir) } )
        {
            int pain = d2 == dir ? 1 : 1001;
            point_t p2 = point + d2;
            auto v = scores.find(p2);
            if( 
                v != scores.end() &&
                v->second <= score-pain &&
                goods.find(p2) == goods.end()
            )
            {
                goods.insert(p2);
                q.push( tuple(score-pain, p2, d2));
            }
        }
    }
    return goods.size();
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

    string data = TEST ? test2 : file_contents(DAY".txt");
    point_t start;
    point_t finish;
    lines = split(data);
    for( int y = 0; y < lines.size(); y++ )
        for( int x = 0; x < lines[y].size(); x++ )
        {
            char c = lines[y][x];
            if( c == 'S' )
                start = point_t(x,y);
            else if( c == 'E' )
                finish = point_t(x,y);
        }

    cout << "Part 1: " << part1( start, finish) << "\n";
    cout << "Part 2: " << part2( start, finish) << "\n";
}
