#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
#include <cstdint>
#include <limits.h>
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
"kh-tc\n"
"qp-kh\n"
"de-cg\n"
"ka-co\n"
"yn-aq\n"
"qp-ub\n"
"cg-tb\n"
"vc-aq\n"
"tb-ka\n"
"wh-tc\n"
"yn-cg\n"
"kh-ub\n"
"ta-co\n"
"de-co\n"
"tc-td\n"
"tb-wq\n"
"wh-td\n"
"ta-ka\n"
"td-qp\n"
"aq-cg\n"
"wq-ub\n"
"ub-vc\n"
"de-ta\n"
"wq-aq\n"
"wq-vc\n"
"wh-yn\n"
"ka-de\n"
"kh-ta\n"
"co-tc\n"
"wh-qp\n"
"tb-vc\n"
"td-yn"
);

bool DEBUG = false;
bool TEST = false;

int part1( StringVector & data )
{
    map<string,set<string>> connx;
    for( auto & line : data )
    {
        string a = line.substr(0,2);
        string b = line.substr(3,2);
        connx[a].insert(b);
        connx[b].insert(a);
    }
    set<string> uniq;
    for( auto & kv : connx )
    {
        string k = kv.first;
        for( auto & v1 : kv.second )
            for( auto & v2 : kv.second )
                if( 
                    (k[0] == 't' || v1[0] == 't' || v2[0] == 't') && 
                    v1 != v2 && 
                    connx[v2].find(k) != connx[v2].end() &&
                    connx[v2].find(v1) != connx[v2].end()
                )
                {
                    vector<string> u({k,v1,v2});
                    sort( u.begin(), u.end() );
                    uniq.insert( u[0]+u[1]+u[2] );
                }
    }
    return uniq.size();
}


string part2( StringVector & data )
{
    map<string,set<string>> connx;
    for( auto & line : data )
    {
        string a = line.substr(0,2);
        string b = line.substr(3,2);
        connx[a].insert(b);
        connx[b].insert(a);
        connx[a].insert(a);
        connx[b].insert(b);
    }

    vector<set<string>> matches;
    for( auto & kv1 : connx )
        for( auto & kv2 : connx )
            if( kv1 != kv2 )
            {
                matches.push_back(set<string>());
                set_intersection(
                    kv1.second.begin(), kv1.second.end(),
                    kv2.second.begin(), kv2.second.end(),
                    inserter(matches.back(), matches.back().begin())
                );
            }

    map<string, int> poss;
    for( auto & m : matches )
    {
        if( m.size() < 4 )
            continue;

        set<string> base( connx[*m.begin()] );
        for( auto & n : m )
        {
            set<string> newbase;
            set_intersection(
                base.begin(), base.end(),
                connx[n].begin(), connx[n].end(),
                inserter(newbase, newbase.begin())
            );
            base.swap(newbase);
        }
        if( !base.empty() )
        {
            string maker;
            for( auto & b : base )
            {
                if( !maker.empty() )
                    maker += ",";
                maker += b;
            }
            poss[maker] ++; 
        } 
    }

    if( DEBUG )
    {
        for( auto & kv : poss )
            cout << kv.first << ": " << kv.second << "\n";
    }

    // Return the most common subset found.

    using pvtype = decltype(poss)::value_type;
    auto m = max_element(
        poss.begin(), poss.end(), 
        []( const pvtype & p1, const pvtype & p2 )
        {
            return p1.second < p2.second;
        }
    );

    return m->first;
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

    string input = TEST ? test : file_contents("day23.txt");

    StringVector data = split(input, "\n");

    cout << "Part 1: " << part1(data) << "\n";
    cout << "Part 2: " << part2(data) << "\n";
}
