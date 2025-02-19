#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <cstdint>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <numeric>

using namespace std;

bool DEBUG = false;
bool TEST = false;

typedef vector<string> StringVector;
typedef vector<int> IntVector;
typedef vector<int64_t> LongVector;
typedef vector<vector<uint8_t>> ByteGrid;

const string test(
"broadcaster -> a, b, c\n"
"%a -> b\n"
"%b -> c\n"
"%c -> inv\n"
"&inv -> a"
);

const string test2(
"broadcaster -> a\n"
"%a -> inv, con\n"
"&inv -> b\n"
"%b -> con\n"
"&con -> output"
);


StringVector split( string src, string delim )
{
    StringVector sv;
    for( int j = src.find(delim); j != -1; )
    {
        sv.push_back( src.substr(0,j) );
        src = src.substr(j+delim.size());
        j = src.find(delim);
    }
    sv.push_back(src);
    return sv;
}


struct PartState {
    string src;
    string dst;
    int state;
};


class Part
{
protected:
    string m_Name;
    map<string,int> m_Inputs;
    vector<string> m_Outputs;
    int m_State;

public:
    Part()
        : m_Name("None")
        , m_State(0)
    {
    }

    Part( const string & name, const StringVector & sv )
        : m_Name(name)
        , m_State(0)
    {
        m_Outputs.resize( sv.size() );
        copy( sv.begin(), sv.end(), m_Outputs.begin() );
    }

    virtual void addinput(const string & inp)
    {
        m_Inputs[inp] = 0;
    }

    virtual void reset()
    {
        m_State = 0;
    }

    virtual vector<PartState> input(const string & inp, int signal)
    {
        return vector<PartState>();
    }

    virtual vector<PartState> output(int state)
    {
        vector<PartState> ps;
        for( auto & k : m_Outputs )
            ps.emplace_back( PartState({m_Name, k, state}) );
        return ps;
    }

    virtual map<string,int> & inputs() {
        return m_Inputs;
    }

    virtual vector<string> & outputs() {
        return m_Outputs;
    }

    void print() const {
        cout << m_Name << ":\n";
        cout << "  Inputs:";
        for( auto & kv : m_Inputs )
            cout << " " << kv.first;
        cout << "\n  Outputs:";
        for( auto & kv : m_Outputs )
            cout << " " << kv;
        cout << "\n";
    }
};

struct Broadcast : public Part
{
    Broadcast( const string & name, StringVector & sv )
        : Part( name, sv )
    {}

    virtual vector<PartState> input(const string &, int)
    {
        return output(0);
    }
};

struct FlipFlop : public Part
{
    FlipFlop( const string & name, StringVector & sv )
        : Part( name, sv )
    {}

    virtual vector<PartState> input( const string & inp, int signal )
    {
        if( !signal )
        {
            m_State = 1 - m_State;
            return output(m_State);
        }
        return vector<PartState>();
    }
};

struct Nand : public Part
{
    Nand( const string & name, StringVector & sv )
        : Part( name, sv )
    {}

    virtual void reset()
    {
        for( auto & k : m_Inputs )
            k.second = 0;
    }
    virtual vector<PartState> input( const string & inp, int signal )
    {
        m_Inputs[inp] = signal;
        // False if all inputs are true
        for( auto & p : m_Inputs )
            if( !p.second )
                return output(1);
        return output(0);
    }
};


typedef map<string,Part*> Circuit;

    
void parse( string & data, Circuit & circuit )
{
    circuit.clear();
    istringstream parse(data);
    string line;
    while( getline( parse, line ) )
    {
        auto s = split(line, " -> ");
        string & l = s[0];
        string & r = s[1];

        char one = l[0];
        if( one != 'b' )
            l = l.substr(1);
        auto parts = split( r, ", " );

        if( l == "broadcaster" )
            circuit[l] = new Broadcast(l,parts);
        else if( one == '%' )
            circuit[l] = new FlipFlop(l,parts);
        else if( one == '&' )
            circuit[l] = new Nand(l,parts);
    }


    circuit["rx"] = new Part("rx", StringVector());

    for( auto & c : circuit )
        for( auto & n : c.second->outputs() )
            if( circuit.find(n) != circuit.end() )
                circuit[n]->addinput(c.first);

    if( DEBUG )
    {
        for( auto & c : circuit )
        {
            cout << c.first << ": ";
            c.second->print();
        }
    }
}



int64_t part1( Circuit & circuit )
{
    int count[2] = {0,0};

    // Push da button
    
    for( int i = 0; i < 1000; i++ )
    {
        // Account for the button.
        count[0] += 1;
        deque<PartState> todo;

        auto k = circuit["broadcaster"]->output(0);
        copy( k.begin(), k.end(), back_inserter(todo) );

        while( !todo.empty() )
        {
            PartState ps = todo.front();
            todo.pop_front();

            count[ps.state] += 1;
            if( circuit.find(ps.dst) != circuit.end() )
            {
                auto k = circuit[ps.dst]->input(ps.src, ps.state);
                copy( k.begin(), k.end(), back_inserter(todo) );
            }
        }
    }
    if( DEBUG )
        cout << count[0] << " " << count[1] << "\n";
    return count[0]*count[1];
}


int64_t part2( Circuit & circuit )
{
    // Reset the circuit.

    for( auto & p : circuit )
        p.second->reset();

    // Now we have to find the cycles.
    // rx is fed by zh in my sample, and zh is fed by sx, jt, kb, ks.
    // rx only goes LOW (the target) when zh sends a HIGH, which only
    // happens when the four inputs go LOW.  So, find the cycles.

    set<string> check;
    for( auto & r1 : circuit["rx"]->inputs() )
        for( auto & r2 : circuit[r1.first]->inputs() )
            check.insert( r2.first );

    if( DEBUG )
    {
        cout << "Check: ";
        for( auto & s : check )
            cout << s;
        cout << "\n";
    }

    LongVector cycles;
    map<string,IntVector> prev;
    int t = 0;
    while( cycles.size() < 4 )
    {
        deque<PartState> todo;

        auto k = circuit["broadcaster"]->output(0);
        copy( k.begin(), k.end(), back_inserter(todo) );

        while( !todo.empty() )
        {
            PartState ps = todo.front();
            todo.pop_front();

            if( check.find(ps.dst) != check.end() && !ps.state )
            {
                if( prev[ps.dst].size() == 1 )
                {
                    cycles.push_back( t - prev[ps.dst][0] );
                }
                prev[ps.dst].push_back( t );
            }

            auto k = circuit[ps.dst]->input(ps.src, ps.state);
            copy( k.begin(), k.end(), back_inserter(todo) );
        }
        t += 1;
    }
    if( DEBUG )
    {
        for( int c : cycles )
            cout << c << " ";
        cout << "\n";
        for( auto & p : prev )
            cout << p.first << " has " << p.second.size() << "\n";
    }
    int64_t prod = 1;
    for( int64_t i : cycles )
        prod *= i;
    return prod;
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
        data = test2;
    }
    else 
    {
        stringstream buffer;
        buffer << ifstream("day20.txt").rdbuf();
        data = buffer.str();
    }

    // Parses into the globals parts and flows.

    Circuit circuit;
    parse(data,circuit);

    cout << "Part 1: " << part1(circuit) << "\n";
    if( !TEST )
        cout << "Part 2: " << part2(circuit) << "\n";
}
