#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <vector>
#include <set>
#include <map>

using namespace std;

// 13312 ORE for 1 FUEL:

const char * test1=
    "157 ORE => 5 NZVS\n"
    "165 ORE => 6 DCFZ\n"
    "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL\n"
    "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ\n"
    "179 ORE => 7 PSHF\n"
    "177 ORE => 5 HKGWZ\n"
    "7 DCFZ, 7 PSHF => 2 XJWVT\n"
    "165 ORE => 2 GPVTF\n"
    "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT\n";

// 180697 ORE for 1 FUEL:

const char * test2=
    "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG\n"
    "17 NVRVD, 3 JNWZP => 8 VPVL\n"
    "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL\n"
    "22 VJHF, 37 MNCFX => 5 FWMGM\n"
    "139 ORE => 4 NVRVD\n"
    "144 ORE => 7 JNWZP\n"
    "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC\n"
    "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV\n"
    "145 ORE => 6 MNCFX\n"
    "1 NVRVD => 8 CXFTF\n"
    "1 VJHF, 6 MNCFX => 4 RFSQX\n"
    "176 ORE => 6 VJHF\n";

// 2210736 ORE for 1 FUEL:

const char * test3 =
    "171 ORE => 8 CNZTR\n"
    "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL\n"
    "114 ORE => 4 BHXH\n"
    "14 VRPVC => 6 BMBT\n"
    "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL\n"
    "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT\n"
    "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW\n"
    "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW\n"
    "5 BMBT => 4 WPTQ\n"
    "189 ORE => 9 KTJDG\n"
    "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP\n"
    "12 VRPVC, 27 CNZTR => 2 XDBXC\n"
    "15 KTJDG, 12 BHXH => 5 XCVML\n"
    "3 BHXH, 2 VRPVC => 7 MZWV\n"
    "121 ORE => 7 VRPVC\n"
    "7 XCVML => 6 RJRHP\n"
    "5 BHXH, 4 VRPVC => 5 LTCX\n";


//  Topological sort.

struct Graph 
{
    map<string,vector<string>> m_Graph;
    set<string> m_Nodes;

protected:
    map<string,bool> m_Visited;
    vector<string> m_Order;
    
public:
    void addEdge( string u, string v )
    {
        m_Nodes.insert( u );
        m_Nodes.insert( v );
        m_Graph[u].push_back( v );
    }

protected:
    void topoSortUtil( const string & v )
    {
        m_Visited[v] = true;
        for( auto && i : m_Graph[v] )
            if( !m_Visited[i] )
                topoSortUtil( i );
        m_Order.push_back( v );
    }

public:
    vector<string> topoSort()
    {
        // Mark all vertices not visited.
        for( auto && i : m_Nodes )
            m_Visited[i] = false;

        for( auto && i : m_Nodes )
            if( ! m_Visited[i] )
                topoSortUtil( i );

        reverse( m_Order.begin(), m_Order.end() );
        return m_Order;
    }
};


bool TRACE = false;
bool TEST = false;

struct Mix 
{
    string m_Sym;
    int64_t m_Qty;
    vector<pair<string,int64_t> > m_Needs;

    Mix( string _sym="", int64_t _qty=0 )
        : m_Sym( _sym )
        , m_Qty( _qty )
        { }

    Mix( const Mix & other )
        : m_Sym( other.m_Sym )
        , m_Qty( other.m_Qty )
        { }

    string repr()
    {
        string s = "<Mix " + m_Sym + " x " + to_string(m_Qty) + " from ";
        for( auto & need : m_Needs )
        {
            s += " + " + need.first + " " + to_string(need.second);
        }
        s += ">";
        return s;
    }
};


vector<string> parse(istream & s, map<string,Mix> & tree )
{
    Graph graph;
    s.clear();
    s.seekg( 0 );

    string ln;
    while( getline( s, ln ) )
    {
        // "# xxx, # xxx => # xxx"

        vector<pair<string,int64_t>> recipe;
        string token;
        istringstream scan(ln);
        while( 1 )
        {
            scan >> token;
            if( token == "=>" )
                break;
            int qty = stoi(token);
            scan >> token;
            if( token.back() == ',' )
                token.resize( token.size() - 1 );
            recipe.emplace_back( token, qty );
        }

        scan >> token;
        int qty = stoi(token);
        string sym;
        scan >> sym;

        Mix chem( sym, qty );
        chem.m_Needs = recipe;
        tree[sym] = chem;

        for( auto part : recipe )
        {
            graph.addEdge( sym, part.first );
        }
    }

    return graph.topoSort();
}


void processloop( map<string,Mix> & tree, map<string,int64_t> & amts, const string & chem )
{
    int64_t qty = amts[chem];
    amts[chem] = 0;
    if( TRACE )
        cout << qty << " of " << chem << " needs:\n";
    Mix & mix = tree[chem];
    qty = (qty+mix.m_Qty-1) / mix.m_Qty;
    if( TRACE )
        cout << "   " << qty << "  units\n";
    for( auto && need : mix.m_Needs )
    {
        if( TRACE )
            cout << "   " << (need.second * qty) << " of " << need.first << "\n";
        amts[need.first] += need.second*qty;
    }
}

int64_t process( istream & s, int64_t target )
{
    cout << "process trying for " << target << "\n";
    map<string,Mix> tree;
    vector<string> order = parse( s, tree );

    map<string,int64_t> amts;
    amts["FUEL"] = target;
    amts["ORE"] = 0;

    if( TRACE )
    {
        for( auto && k : order )
            cout << "'" << k << "': " << amts[k] << ", ";
        cout << "\n";
    }

    for( auto && i : order )
    {
        if( i == "ORE" )
            break;
        processloop( tree, amts, i );
        if( TRACE )
        {
            cout << "Stores: ";
            for( auto && k : order )
                cout << "'" << k << "': " << amts[k] << ", ";
            cout << "\n";
        }
    }

    return amts["ORE"];
}

int64_t process( const char * tst, int64_t target )
{
    istringstream iss( tst );
    return process( iss, target );
}

int64_t part2( istream & setup )
{
    int64_t ore = 1000000000000;
    int64_t guess = 1;

    // Times 10 until we go over.

    for( ;; )
    {
        int64_t got = process( setup, guess );
        if( TRACE )
            cout << guess << " got " << got << "\n";
        if( got > ore )
            break;
        if( got < 0 )
            return -1;
        guess *= 10;
    }

    // Back down and do one digit at a time.

    guess /= 10;
    int64_t incr = guess;

    while( incr )
    {
        guess += incr;
        int64_t got = process( setup, guess );
        if( TRACE )
            cout << guess << " got " << got << "\n";
        if( got > ore )
        {
            guess -= incr;
            incr /= 10;
        }
    }
    return guess;
}

int64_t part2( const char * tst )
{
    istringstream iss( tst );
    return part2( iss );
}

int main(int argc, char ** argv )
{
    std::ifstream real( "day14.txt" );

    while( *++argv )
    {
        std::string arg(*argv);
        if( arg == "trace" )
            TRACE = true;
        if( arg == "test" )
            TEST = true;
    }

    if( TEST )
    {
        cout << "Test 1: " << process(test1, 1) << "\n";
        cout << "Test 2: " << process(test2, 1) << "\n";
        cout << "Test 3: " << process(test3, 1) << "\n";
    }
    cout << "*** Part 1: " << process(real,1) << "\n";

    if( TEST )
    {
        cout << "Test 1: " << part2(test1) << "\n";
        cout << "Test 2: " << part2(test2) << "\n";
        cout << "Test 3: " << part2(test3) << "\n";
    }
    cout <<"*** Part 2: " << part2( real )  << "\n";
}
