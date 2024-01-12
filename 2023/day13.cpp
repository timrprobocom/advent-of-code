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
"#.##..##.\n"
"..#.##.#.\n"
"##......#\n"
"##......#\n"
"..#.##.#.\n"
"..##..##.\n"
"#.#.##.#.\n"
"\n"
"#...##..#\n"
"#....#..#\n"
"..##..###\n"
"#####.##.\n"
"#####.##.\n"
"..##..###\n"
"#....#..#"
);


// Parse the input.

void parse( istream & fin, vector<StringVector> & lines )
{
    string line;
    lines.resize( 1 );
    while( getline( fin, line ) )
    {
        if( line.empty() )
            lines.resize( lines.size()+1 );
        else
            lines.back().push_back( line );
    }
}


int compare_columns(StringVector & chart, int a, int b)
{
    int sum = 0;
    for( auto & row : chart )
        sum += row[a] != row[b];
    return sum;
}


int compare_rows(StringVector & chart, int a, int b)
{
    int sum = 0;
    int W = chart[a].size();
    for( int i = 0; i < W; i++ )
        sum += chart[a][i] != chart[b][i];
    return sum;
}


// 9 1 check 1   0 1
// 9 2 check 2   01 23
// 9 3 check 3   012 345
// 9 4 check 4   0123 4567
// 9 5 check 4   1234 5678
// 9 6 check 3   345 678 
// 9 7 check 2   56 78
// 9 8 check 1   7 8

int find_h_reflect(StringVector & chart, int target=0)
{
    int W = chart[0].size();
    int H = chart.size();
    for( int col = 1; col < W; col++ )
    {
        int check = min(col, W-col);
        int miss = 0;
        for( int i = 0; i < check; i++ )
            miss += compare_columns( chart, col-1-i, col+i );

        if( miss == target )
        {
            if( DEBUG )
                cout << "H" << col << "\n";
            return col;
        }
    }
    return 0;
}

int find_v_reflect(StringVector & chart,int target=0)
{
    int W = chart[0].size();
    int H = chart.size();
    for( int row = 1; row < H; row++ )
    {
        int check = min(row, H-row);
        int miss = 0;
        for( int i = 0; i < check; i++ )
            miss += compare_rows( chart, row-1-i, row+i );

        if( miss == target )
        {
            if( DEBUG )
                cout << "V" << row << "\n";
            return row;
        }
    }
    return 0;
}


int part1( int part, vector<StringVector> & charts )
{
    int sumx = 0;
    for( auto & chart : charts )
    {
        int h = find_h_reflect(chart,part-1);
        int v = find_v_reflect(chart,part-1);
        if( DEBUG )
            cout << h << " " << v << "\n";
        sumx += 100*v+h;
    }
    return sumx;
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

    vector<StringVector> charts;
    if( TEST )
    {
        istringstream data;
        data.str(test);
        parse(data, charts);
    }
    else 
    {
        ifstream data("day13.txt");
        parse(data, charts);
    }

    cout << "Part 1: " << part1(1,charts) << "\n";
    cout << "Part 2: " << part1(2,charts) << "\n";
}
