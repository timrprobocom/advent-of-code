#include <string>
#include <vector>
#include <list>
#include <map>
#include <iostream>

using namespace std;

const char * test[] = {
"COM)B",
"B)C",
"C)D",
"D)E",
"E)F",
"B)G",
"G)H",
"D)I",
"E)J",
"J)K",
"K)L"
};


struct Node
{
    string me;
    string parent;
    vector<string> child;
    int depth;
    Node( string _me="" )
        : me( _me )
        , depth( 0 )
    {
    }
};

typedef map<string,Node> nodetree_t;
nodetree_t tree;

void add_to_tree( nodetree_t & tree, string both )
{
    int i = both.find(')');
    string left = both.substr( 0, i );
    string right= both.substr( i+1 );
    if( tree.find(left) == tree.end() )
        tree.emplace( left, left );
    if( tree.find(right) == tree.end() )
        tree.emplace( right, right );
    tree[left].child.push_back(right);
    tree[right].parent = left;
}

// Part 1

int xsum = 0;
int part1( nodetree_t & tree, string st, int depth )
{
    Node & e = tree[st];
    e.depth = depth;
    for(auto & i : e.child )
    {
        part1(tree, i, depth+1);
//        cout << st << ": After " << i << " now " << depth << "\n";
        xsum += depth + 1;
    }
    return xsum;
}
    
// Part 2.

typedef list<string> path_t;
void getpath( string el, path_t & path )
{
    Node & cell = tree[el];
    if( !cell.parent.empty() )
    {
        path.push_back( cell.parent );
        getpath( cell.parent, path );
    }
}

int main( int argc, char ** argv )
{
    // day06 test
    // day06 < day06.txt
    //
    bool testdata = (argc > 1) && (string(argv[1]) == "test");

    if( testdata )
    {
        // Test data.

        for( auto & ln : test )
            add_to_tree( tree, ln );
    }
    else
    {
        // Real data.

        string ln;
        while( getline( cin, ln ) )
            add_to_tree( tree, ln );
    }

    cout << "Part 1: " << part1(tree, "COM", 0) << "\n";

    // Part 2.

    if( testdata )
    {
        add_to_tree( tree, "K)YOU" );
        add_to_tree( tree, "I)SAN" );
    }

    path_t you; getpath("YOU", you);
    path_t santa; getpath("SAN", santa);
    path_t equal;

    for( auto & s : you )
        if( find( santa.begin(), santa.end(), s ) != santa.end() )
            equal.push_back( s );

    cout << "YOU: " << you.size() << "\n";
    cout << "SANTA: " << santa.size() << "\n";
    cout << "COMMON: " << equal.size() << "\n";

// How many steps on the two branches that are not in common:

    cout << "Part 2: " 
        << (you.size()-equal.size() + santa.size()-equal.size()) << "\n";
}

