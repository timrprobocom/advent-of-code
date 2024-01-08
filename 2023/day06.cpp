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
bool TEST = false;

typedef vector<string> StringVector;
typedef vector<int> IntVector;
typedef vector<int64_t> LongVector;

const string test(
"Time:      7  15   30\n"
"Distance:  9  40  200"
);

const string live(
"Time:        56     97     77     93\n"
"Distance:   499   2210   1097   1440"
);


// So, for the first race, hold time vs distance:
//  0  1  2  3  4  5  6  7
//  0  6 10 12 12 10  6  0
// It's a Pascal's triangle thing

// 0  1  2  3  4  5  6
// 0  5  8  9  8  5  0

int64_t compute( int64_t time, int64_t dist )
{
    int64_t d = 0;
    int64_t i = 0;
    int64_t n = time-1;
    while( d <= dist )
    {
        i ++;
        d += n;
        n -= 2;
    }

    return time + 1 -i - i;
}

int part1(string data)
{
    istringstream parse(data);
    IntVector time;
    IntVector dist;
    string word;
    bool dotime;
    while( parse >> word )
    {
        if( word == "Time:" )
            dotime = true;
        else if( word == "Distance:" )
            dotime = false;
        else if( dotime )
            time.push_back(stol(word));
        else
            dist.push_back(stol(word));
    }
    int sumx = 1;
    for( int i = 0; i < time.size(); i ++ )
        sumx *= compute( time[i], dist[i] );
    return sumx;
}
          
int part2(string data)
{
    istringstream parse(data);
    string stime;
    string sdist;
    string word;
    bool dotime;
    while( parse >> word )
    {
        if( word == "Time:" )
            dotime = true;
        else if( word == "Distance:" )
            dotime = false;
        else if( dotime )
            stime += word;
        else
            sdist += word;
    }

    int64_t time = stoll(stime);
    int64_t dist = stoll(sdist);
    return compute( time, dist );
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

    string data = TEST ? test : live;

    cout << "Part 1: " << part1(data) << "\n";
    cout << "Part 2: " << part2(data) << "\n";
}
