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
"???.### 1,1,3\n"
".??..??...?##. 1,1,3\n"
"?#?#?#?#?#?#?#? 1,3,1,6\n"
"????.#...#... 4,1,1\n"
"????.######..#####. 1,6,5\n"
"?###???????? 3,2,1"
);


// Parse the input.

void parse( string & line, string & maps, IntVector & nums )
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

typedef tuple<int,int64_t,size_t> Params;

int64_t makehash(IntVector & n)
{
    int64_t h;
    for( auto i : n )
        h = h*12 + i;
    return h;
}

map<Params,int64_t> memoize;

int64_t gen( string pat, int size, IntVector & nums )
{
    if( nums.empty() )
        return pat.find('#') == string::npos;

    Params check(size,makehash(nums),hash<string>{}(pat));
    if( memoize.find(check) != memoize.end())
        return memoize[check];

    int now = nums.front();
    IntVector rest( nums.begin()+1, nums.end());
    int after = accumulate( rest.begin(), rest.end(), rest.size());

    int64_t count = 0;
    string t(now, '#');
    for( int before = 0; before < size-after-now+1; before++ )
    {
        string s = string(before,'.') + t + ".";
        if( match( pat, s ) )
        {
            int n = min(pat.size(),s.size());
            count += gen( pat.substr(n), size-now-before-1, rest );
        }
    }

    memoize[check] = count;
    if( memoize.size() % 100000 == 0 )
    cout << memoize.size() << "\n";
    return count;
}

int64_t count_matches( string & pat, IntVector & nums )
{
    return gen( pat, pat.size(), nums );
}


int part1( StringVector & lines )
{
    string pat;
    IntVector nums;

    int sumx = 0;
    for( auto & s : lines )
    {
        parse( s, pat, nums );
        sumx += count_matches( pat, nums );
    }
    return sumx;
}


int64_t part2( StringVector & lines )
{
    string pat;
    IntVector nums;

    int64_t sumx = 0;
    for( auto & s : lines )
    {
        parse( s, pat, nums );
        int n = nums.size();
        pat = pat + "?" + pat + "?" + pat + "?" + pat + "?" + pat;
        for( int i = 0; i < n * 4; i++ )
            nums.push_back( nums[i] );
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
        ifstream data("day12.txt");
        string line;
        while( getline( data, line ) )
            lines.push_back( line );
    }

    cout << "Part 1: " << part1(lines) << "\n";
    cout << "Part 2: " << part2(lines) << "\n";
}
