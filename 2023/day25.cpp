#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <random>
#include <algorithm>

using namespace std;

bool DEBUG = false;
bool TEST = false;

typedef vector<string> StringVector;
typedef vector<int> IntVector;
typedef vector<int64_t> LongVector;
typedef vector<vector<uint8_t>> ByteGrid;

const string test(
"jqt: rhn xhk nvd\n"
"rsh: frs pzl lsr\n"
"xhk: hfx\n"
"cmg: qnr nvd lhk bvb\n"
"rhn: xhk bvb hfx\n"
"bvb: xhk hfx\n"
"pzl: lsr hfx nvd\n"
"qnr: nvd\n"
"ntq: jqt hfx bvb xhk\n"
"nvd: lhk\n"
"lsr: lhk\n"
"rzs: qnr cmg lsr rsh\n"
"frs: qnr lhk lsr"
);

typedef map<string,StringVector> Graph;

void make_graph( string & data, Graph & graph )
{
    istringstream parse(data);
    string word;
    string base;
    while( parse >> word )
    {
        if( word.back() == ':' )
        {
            base = word.substr(0,word.size()-1);
        }
        else
        {
            graph[base].push_back(word);
            graph[word].push_back(base);
        }
    }
}


set<string> reachableNodes( Graph & graph, string start )
{
    set<string> seen;
    deque<string> queue;
    seen.insert(start);
    queue.push_back(start);
    while( !queue.empty() )
    {
        string v = queue.front();
        queue.pop_front();
        seen.insert(v);
        for( string edge : graph[v] )
            if( seen.find(edge) == seen.end() )
                queue.push_back(edge);
    }
    return seen;
}
            

string shortestPath( Graph & graph, const string & v1, const string & v2 )
{
    deque<string> queue;
    queue.push_back( v1 );
    set<string> seen;
    while( !queue.empty() )
    {
        string path = queue.front();
        queue.pop_front();
        string v = path.substr(path.size()-3);
        if( v == v2 )
            return path;
        seen.insert(v);
        for( string n : graph[v] )
            if( seen.find(n) == seen.end() )
                queue.push_back( path+","+n );
    }
    return "";
}



// We repeatedly pick two random vertices and find the shortest path between them via BFS.
// Then pick the top k most travelled edges and remove these from the graph and
// check if we have succesfully made a k cut. If so return it, if not we continue
//
// noCrossings - How many crossings to collect statistics on per attempt.
// k - Stop when we find a k-cut.
// Returns the size of one of the partitions.

int minimumCut( Graph & graph, int noCrossings, int cut=3 )
{
    vector<string> keys;
    for( auto & k : graph )
        keys.push_back(k.first);

    mt19937 generator(random_device{}());
    uniform_int_distribution<int> choose(0, keys.size()-1);

    for( ;; )
    {
        map<string,int> crossingCounts;
        for( int i = 0; i < noCrossings; i++ )
        {
            string v1 = keys[choose(generator)];
            string v2 = keys[choose(generator)];

            string path = shortestPath(graph,v1,v2);
            for( int j = 4; j < path.size(); j += 4 )
            {
                string p1 = path.substr(j-4,3);
                string p2 = path.substr(j,3);
                crossingCounts[p1+p2] ++;
            }
        }

        // Convert the crossing counters to something that can be sorted.

        typedef pair<int,string> IntString;
        vector<IntString> cross2;
        cross2.reserve( crossingCounts.size() );
        for( auto & kv : crossingCounts )
            cross2.emplace_back( kv.second, kv.first );
        sort( cross2.begin(), cross2.end(), [](auto & a, auto & b) {
            return a.first > b.first;
        });

        // Remove the 3 edges that we are guessing make the min cut.

        cross2.resize(3);

        Graph g2;
        for( auto & kv : graph )
            copy( kv.second.begin(), kv.second.end(), back_inserter(g2[kv.first]) );

        for( auto & c : cross2 )
        {
            string key0 = c.second.substr(0,3);
            string key1 = c.second.substr(3,3);
            auto p = find(g2[key0].begin(), g2[key0].end(), key1);
            if( p != g2[key0].end() )
                g2[key0].erase( p );
            auto q = find(g2[key1].begin(), g2[key1].end(), key0);
            if( q != g2[key1].end() )
                g2[key1].erase( q );
        }

        auto canReach = reachableNodes(g2, keys[0]);
        if( canReach.size() < graph.size() )
            return canReach.size();
    }

    return 0;
}


int64_t part1( Graph & graph )
{
    int one = minimumCut( graph, 10, 3 );
    int two = graph.size() - one;
    return one*two;
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
        buffer << ifstream("day25.txt").rdbuf();
        data = buffer.str();
    }

    Graph graph;
    make_graph( data, graph );

    cout << "Part 1: " << part1(graph) << "\n"; // 485607
}

