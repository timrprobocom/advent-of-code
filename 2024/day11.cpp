#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
#include <cstdint>
#include <cstring>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <numeric>

using namespace std;

const string test("125 17");
const string live("4189 413 82070 61 655813 7478611 0 8");

bool DEBUG = false;
bool TEST = false;

/*
# The key here is recognizing that the stones are independent.  A given
# stone will always follow the same path.  So, we can cache the results 
# without actually remembering all of the stones.
*/

typedef map<pair<int64_t,int>,int64_t> cache_t;

int64_t blink( int64_t s, int n )
{
    static cache_t cache;
    pair<int64_t,int> key(s,n);
    if( cache.find(key) != cache.end() )
        return cache[key];
    if( !n )
        return 1;
    if( !s )
        return cache[key] = blink(1, n-1);

    string ss = to_string(s);
    if( ss.size() % 2 == 0 )
    {
        int64_t a = stol(ss.substr(0, ss.size()/2));
        int64_t b = stol(ss.substr(ss.size()/2));
        return cache[key] = blink(a,n-1)+blink(b,n-1);
    }
    return blink(s*2024, n-1);
}

int64_t part1(vector<int> data, int N)
{
    // This actually is marginally faster than the explicit loop.
    return std::accumulate(
        data.begin(),
        data.end(),
        0ll,
        [N](int64_t sum,int64_t i){return sum+blink(i,N);}
    );
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

    stringstream input( TEST ? test : live );
    vector<int> data{
        istream_iterator<int>(input),
        istream_iterator<int>()
    };

    cout << "Part 1: " << part1(data,25) << "\n";
    cout << "Part 2: " << part1(data,75) << "\n";
}
