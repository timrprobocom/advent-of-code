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
typedef deque<int> IntDeque;
typedef vector<int64_t> LongVector;

const string test(
"???.### 1,1,3\n"
".??..??...?##. 1,1,3\n"
"?#?#?#?#?#?#?#? 1,3,1,6\n"
"????.#...#... 4,1,1\n"
"????.######..#####. 1,6,5\n"
"?###???????? 3,2,1"
);


// Parse the input.

void parse( string & line, string & maps, IntDeque & nums )
{
    int accum = 0;
    maps.clear();
    nums.clear();
    for( char c : line )
    {
        if( isdigit(c) )
        {
            accum = accum * 10 + c - '0';
        }
        else if( c == ',' )
        {
            nums.push_back( accum );
            accum = 0;
        }
        else if( c != ' ' )
        {
            maps += c;
        }
    }
    nums.push_back(accum);
}

// Does chk match the first pat of pat?

bool match( string & pat,  string & chk )
{
    int m = min(pat.size(), chk.size());
    for( int i = 0; i < m; i++ )
        if( pat[i] != '?' && pat[i] != chk[i] )
            return false;
    return true;
}

// Each call of this does one chunk of #s.  We generage all possible strings that
// end with "###." for this chunk.  If that prefix matches the current spot in the 
// pattern, we recursively try the next.  It's only the memoizing that allows 
// this to run in finite time.

int gen( string pat, int size, IntDeque nums )
{
    // TODO
    // I probably need to memoize this.

    if( nums.empty() )
        return pat.find('#') == string::npos;

    int now = nums.front();
    nums.pop_front();
    int after = accumulate( nums.begin(), nums.end(), 0 ) + nums.size();

    int count = 0;
    string t(now, '#');
    cout << "now is " << now << ", t is " << t << "\n";
    for( int before = 0; before < size-after-now+1; before++ )
    {
        string s = string(before,'.') + t + ".";
        cout << "Checking " << pat << " vs " << s << "\n";
        if( match( pat, s ) )
        {
            if( pat.size() >= s.size() )
            count += gen( pat.substr(s.size()), size-now-before-1, nums );
        }
    }

    return count;
}

int count_matches( string & pat, IntDeque & nums )
{
    return gen( pat, pat.size(), nums );
}


int64_t part1( StringVector & lines )
{
    string pat;
    IntDeque nums;

    int sumx = 0;
    for( auto & s : lines )
    {
        parse( s, pat, nums );
        sumx += count_matches( pat, nums );
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

    cout << "Part 1: " << part1(lines) << "\n";
//    cout << "Part 2: " << part2(lines) << "\n";
}
