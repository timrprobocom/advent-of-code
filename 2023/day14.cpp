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
"O....#....\n"
"O.OO#....#\n"
".....##...\n"
"OO.#O....O\n"
".O.....O#.\n"
"O.#..O.#.#\n"
"..O..#O..O\n"
".......O..\n"
"#....###..\n"
"#OO..#...."
);

int W = 0;
int H = 0;

// Parse the input.

void parse( istream & fin, StringVector & lines )
{
    string line;
    while( getline( fin, line ) )
        lines.push_back(line);
}

void tilt_n( StringVector & grid )
{
    for( int x = 0; x < W; x++)
    {
        int dy = 0;
        for( int y = 0; y < H; y++ )
        {
            char c = grid[y][x];
            if( c == '.' )
                dy++;
            else if( c == '#')
                dy = 0;
            else if( c == 'O')
            {
                grid[y][x] = '.';
                grid[y-dy][x] = 'O';
            }
        }
    }
}

void tilt_s( StringVector & grid )
{
    for( int x = 0; x < W; x++)
    {
        int dy = 0;
        for( int y = H-1; y >= 0; y-- )
        {
            char c = grid[y][x];
            if( c == '.' )
                dy++;
            else if( c == '#')
                dy = 0;
            else if( c == 'O')
            {
                grid[y][x] = '.';
                grid[y+dy][x] = 'O';
            }
        }
    }
}


void tilt_w( StringVector & grid )
{
    for( int y = 0; y < H; y++ )
    {
        int dx = 0;
        for( int x = 0; x < W; x++)
        {
            char c = grid[y][x];
            if( c == '.' )
                dx++;
            else if( c == '#')
                dx = 0;
            else if( c == 'O')
            {
                grid[y][x] = '.';
                grid[y][x-dx] = 'O';
            }
        }
    }
}


void tilt_e( StringVector & grid )
{
    for( int y = 0; y < H; y++ )
    {
        int dx = 0;
        for( int x = W-1; x >= 0; x--)
        {
            char c = grid[y][x];
            if( c == '.' )
                dx++;
            else if( c == '#')
                dx = 0;
            else if( c == 'O')
            {
                grid[y][x] = '.';
                grid[y][x+dx] = 'O';
            }
        }
    }
}


int weight( StringVector & grid )
{
    int sum = 0;
    for( int y = 0; y < H; y++ )
        sum += (H-y)*count(grid[y].begin(),grid[y].end(),'O');
    return sum;
}


uint64_t unique( StringVector & grid )
{
    // Join into a single string.
    string mass;
    for( auto & s : grid )
        mass += s;
    return hash<string>{}(mass);
}


void print( StringVector & grid )
{
    cout << "----\n";
    for( auto & s : grid )
        cout << s << "\n";
}


int part1( StringVector grid )
{
    tilt_n(grid);
    return weight(grid);
}


int part2( StringVector grid )
{
    map<uint64_t,int> seen;
    seen[0] = 0;
    IntVector scores(1);
    int pat0 = 0;
    for( ;; )
    {
        tilt_n(grid);
        tilt_w(grid);
        tilt_s(grid);
        tilt_e(grid);
        uint64_t cur = unique(grid);
        scores.push_back(weight(grid));
        if( DEBUG )
            cout << seen.size() << " " << scores.back() << " " << cur << "\n";
        if( seen.find(cur) != seen.end() )
        {
            pat0 = seen[cur];
            break;
        }
        seen[cur] = seen.size();
    }
    int cycle = seen.size() - pat0;
    int want =  (1000000000 - pat0) % cycle + pat0;
    return scores[want];
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
        ifstream data("day14.txt");
        parse(data, lines);
    }

    W = lines[0].size();
    H = lines.size();

    cout << "Part 1: " << part1(lines) << "\n";
    cout << "Part 2: " << part2(lines) << "\n";
}
