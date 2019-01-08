#include <string>
#include <vector>
#include <stack>
#include <map>
#include <set>
#include <fstream>
#include <iostream>
#include <algorithm>

// So, here's the magic.  Rather than build all of the possible strings
// up to this point, pos simply holds the list of coordinates we might be
// at, based on all the alternatives to this point.  When we get an 
// alternative, we start again with the list of starting positions for 
// this set of alternatives.
//
// That's really clever.

typedef std::tuple<int,int> Coord;

Coord operator+(const Coord & a, const Coord & b )
{
    return Coord(std::get<0>(a)+std::get<0>(b),std::get<1>(a)+std::get<1>(b));
}


// The sizes here are essentially a diameter from the center.  Specifying
// 100,100 makes a matrix from [-100,100] in both directions.

class Maze 
    : public std::vector<int>
{
    int m_dx;
    int m_dy;
    int m_stride;
public:
    Maze( int width, int height )
        : std::vector<int>( (width+width+1)*(height+height+1), -1 )
        , m_dx( width )
        , m_dy( height )
        , m_stride( width+width+1 )
    {
    }

    int get( int x, int y )
    {
        return (*this)[(y+m_dy)*m_stride + x + m_dx];
    }

    int get( Coord c)
    {
        return get(std::get<0>(c),std::get<1>(c));
    }

    void set( int x, int y, int value )
    {
        (*this)[(y+m_dy)*m_stride + x + m_dx] = value;
    }

    void set( Coord c, int value )
    {
        set(std::get<0>(c),std::get<1>(c),value);
    }
};


typedef std::set<Coord> CellSet;

void createMaze( Maze & maze )
{
    Coord base( 0, 0 );
    maze.set( base, 0 );

    // the current positions that we're building on.
    CellSet pos;
    pos.insert( base );
    // a stack keeping track of (starts, ends) for groups.
    std::stack<CellSet> stack;
    // current possible starting and ending positions.
    CellSet starts, ends;
    starts.insert( base );
    ends.insert( base );

    static std::map<char, Coord> directions;
    if( directions.empty() )
    {
        directions['N'] = Coord(0,-1);
        directions['E'] = Coord(1, 0);
        directions['S'] = Coord(0, 1);
        directions['W'] = Coord(-1,0);
    }

    for( char c = getchar(); c >= 0; c = getchar() )
    {
        switch( c )
        {
            case '|':
                // An alternate: update possible ending points, and restart the group.
                ends.insert( pos.begin(), pos.end() );
                pos = starts;
                break;
            case 'N':
            case 'E':
            case 'S':
            case 'W':
            {
                // Move in a given direction, by updating all of possible positions
                // we might have started at.  Remember step counts in the maze.
                Coord dir = directions[c];
                CellSet newpos;
                for( auto cell : pos )
                {
                    int steps = maze.get( cell );
                    Coord maybe = cell + dir;
                    if( maze.get( maybe ) < 0 )
                    {
                        maze.set( maybe, steps+1 );
                        newpos.insert( maybe );
                    }
                }
                pos = newpos;
                break;
            }
            case '(':
                // Start of group.  Push the current starting set so we can use
                // it later, and start a new group.
                stack.push( starts );
                starts = pos;
                ends.clear();
                break;
            case ')':
                // End of group.  Add the current positions as possible endpoints,
                // and pop the last positions off the stack.
                pos.insert( ends.begin(), ends.end() );
                starts = stack.top();
                stack.pop();
                break;
        }
    }
}


int main()
{
    // Build the graph of all possible movements.

    Maze graph(100,100);
    createMaze( graph );

    std::cout << "Part 1: " << *std::max_element(graph.begin(), graph.end() ) << "\n";
    std::cout << "Part 2: " << std::count_if( graph.begin(), graph.end(), [](int i){return i >= 1000;}) << "\n";
}
