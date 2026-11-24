#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdint>
#include <algorithm>
#include <vector>
#include <string>
#include <tuple>
#include <map>
#include <set>

using namespace std;

bool DEBUG = false;
bool TEST = false;

// Answer 8.
const char * test[] =  {
"#########\n"
"#b.A.@.a#\n"
"#########\n",

// Answer 86.
"########################\n"
"#f.D.E.e.C.b.A.@.a.B.c.#\n"
"######################.#\n"
"#d.....................#\n"
"########################\n",

// Answer 136.
"#################\n"
"#i.G..c...e..H.p#\n"
"########.########\n"
"#j.A..b...f..D.o#\n"
"########@########\n"
"#k.E..a...g..B.n#\n"
"########.########\n"
"#l.F..d...h..C.m#\n"
"#################""",

// Answer 81.
"########################\n"
"#@..............ac.GI.b#\n"
"###d#e#f################\n"
"###A#B#C################\n"
"###g#h#i################\n"
"########################\n"
};

// Part 2, answer 72.
const char * test2[] =  {
"#############\n"
"#g#f.D#..h#l#\n"
"#F###e#E###.#\n"
"#dCba@#@BcIJ#\n"
"#############\n"
"#nK.L@#@G...#\n"
"#M###N#H###.#\n"
"#o#m..#i#jk.#\n"
"#############\n"
};


struct Point {
    int x;
    int y;
    Point( )
        : x(0)
        , y(0)
        {}
    Point( int _x, int _y )
        : x(_x)
        , y(_y)
        {}

    bool operator< (const Point & other) const
    {
        return x < other.x || y < other.y;
    }

    bool operator== (const Point & other) const
    {
        return x==other.x && y==other.y;
    }

    bool operator!= (const Point & other) const
    {
        return x!=other.x || y!=other.y;
    }

    Point operator+( const Point & other )
    {
        return Point( x+other.x, y+other.y );
    }

    Point& operator+=( const Point & other )
    {
        x += other.x;
        y += other.y;
        return *this;
    }
};


Point movements[4] = { Point(0,-1),Point(0,1),Point(-1,0),Point(1,0) };

template<typename T>
struct vector2d : public vector<T>
{
    vector<T> m_vec;
    int m_w;
    int m_h;
    vector2d(int w, int h)
        : m_vec(w*h)
        , m_w(w)
        , m_h(h)
    {
    }

    T & at(int x, int y)
    {
        return m_vec.at(y*m_w+x);
    }

    T & operator[](Point & pt )
    {
        return at(pt.x,pt.y);
    }
};

struct Maze
{
    vector<string> m_Maze;
    Point m_Adit;

    map<char,Point> m_Locations;
    map<char,map<char,int>> m_Steps;
    map<char,std::map<char,std::string>> m_Doors;
    map<std::string, int> m_Seen;

    Maze( const string & str )
    {
        istringstream iss( str );
        map<char,Point> keys;
        map<char,Point> doors;
        for( string ln; std::getline( iss, ln );  )
        {
            int y = m_Maze.size();
            m_Maze.push_back( ln );
            for( int i = 0; i < ln.size(); i++ )
            {
                if( ln[i] == '@' )
                    m_Adit = Point( i, y );
                else if( 'A' <= ln[i] && ln[i] <= 'Z' )
                    doors[ln[i]] = Point( i, y );
                else if( 'a' <= ln[i] && ln[i] <= 'z' )
                    keys[ln[i]] = Point( i, y );
            }
        }

        for( auto kv : doors )
        {
            if( keys.find(tolower(kv.first)) == keys.end() )
            {
                m_Maze[kv.second.y].replace( kv.second.x, 1, " " );
            }
        }
    }

    void print()
    {
        for( auto ln : m_Maze )
            cout << ln << "\n";
    }

    void findall( char cfrom, Point & start )
    {
        map<Point, string> upcoming;
        m_Locations[cfrom] = start;
        upcoming[start] = "";
        vector2d<uint8_t> visited( m_Maze[0].size(), m_Maze.size() );
        int steps = 0;

        while( !upcoming.empty() )
        {
            map<Point,string> more;
            for( auto && m : upcoming )
            {
                Point cur = m.first;
                string intheway = m.second;
                visited[cur] = 1;

                char ch = at(cur);
                if( islower(ch) && steps )
                {
                    m_Locations[ch] = cur;
                    m_Steps[cfrom][ch] = steps;
                    m_Doors[cfrom][ch] = intheway;
                    m_Steps[ch][cfrom] = steps;
                    m_Doors[ch][cfrom] = intheway;
                }
                else if( isupper(ch) )
                    intheway += ch;

                for( auto & facing : movements )
                {
                    Point next = cur + facing;
                    char ch = at(next);
                    if( !visited[next] && ch != '#' )
                        more[next] = intheway;
                }
            }
            upcoming = more;
            steps ++;
        }
    }

    char at( const Point & pt )
    {
        return m_Maze[pt.y][pt.x];
    }

    virtual int search( char sitting, std::string found ) = 0;
};


class Maze_BFS : public Maze
{
public:
    Maze_BFS( const string & str )
        : Maze( str )
        {}
    int search( char sitting, string found );
};


class Maze_DFS : public Maze
{
public:
    Maze_DFS( const string & str )
        : Maze( str )
        {}
    int search( char sitting, string found );
};


string ssort( std::string s )
{
    sort( s.begin(), s.end() );
    return s;
}

int Maze_BFS::search( char start, std::string found )
{
    map<std::string, int> unchecked;
    unchecked[start+found] = 0; 
    int nrobots = 1;
    int result = 0;

    // Keep going as long as there are paths we haven't tested.
    // Because this is "breadth-first", each time through this loop
    // processed all of the paths of a single length.  The next pass
    // will be one step longer.
    while( !unchecked.empty() )
    {
        if( DEBUG )
            cout << "Depth " << unchecked.begin()->second << "\n";

        map<std::string, int> more;
        vector<int> paths;

        // For each path that needs to be checked:

        for( auto & item : unchecked )
        {
            char sitting = item.first[0];
            string found = item.first.substr(1);
            int steps = item.second;
            paths.push_back( steps );

            char s = sitting;

            // For each key this robot can see:
            for( auto pt : m_Steps[s] )
            {
                char key = pt.first;
                if( key < 'a' )
                    continue;
                if( found.find( key ) != found.npos )
                    continue;
                // If there's a door in the way without a key, ignore.
                int dstep = m_Steps[s][key];
                string doors = m_Doors[s][key];
                if( any_of( 
                    doors.begin(), doors.end(),
                    [&found](char ch){ return found.find(tolower(ch)) == found.npos;})
                )
                    continue;

                // If this new path has alread been enumerated, and
                // this path to the same state is shorter, keep it.

                string keys(1,key);
                auto newsit = keys+ssort(found+keys);
                if( more.find(newsit) != more.end() && more[newsit] <= steps+dstep )
                    continue;
                more[newsit] = steps+dstep;
            }
        }
        // When we have nothing new, we have our answer.
        if( more.empty() )
            return *min_element(paths.begin(), paths.end() );
        unchecked = more;
    }
    return 0;
}


int Maze_DFS::search( char sitting, std::string found )
{
    if( DEBUG )
        cout << "New search " << sitting << " " << found << "\n";

    // If we've been in this situation before, we don't need to go again.
    if( m_Seen.find( sitting+found ) != m_Seen.end() )
    {
        return m_Seen[sitting+found];
    }

    vector<int> paths;

    // For each robot:

    // For each key the robot can see:
    for( auto pt : m_Steps[sitting] )
    {
        char key = pt.first;
        if( key < 'a' )
            continue;
        // If we've already picked it up, ignore.
        if( found.find( key ) != found.npos )
            continue;

        // If there's a door in the way without a key, ignore.
        int dstep = m_Steps[sitting][key];
        string doors = m_Doors[sitting][key];
        if( any_of( 
            doors.begin(), doors.end(),
            [&found](char ch){ return found.find(tolower(ch)) == found.npos;})
        )
            continue;
        // Go explore this path.
        paths.push_back( dstep + search(key, ssort(found+key)) );
    }

    int ans = paths.empty() ? 0 : *min_element(paths.begin(),paths.end());
    if( DEBUG )
        cout << (sitting+found) << ": " << ans << "\n";
    m_Seen[sitting+found] = ans;
    return ans;
}


string readall( const char * filename  )
{
    ifstream file(filename);
    ostringstream oss;
    oss << file.rdbuf();
    return oss.str();
}

void split( vector<string> & live, const string & sin )
{
    auto size = sin.find("\n") + 1;
    int mid = (size-1) / 2 + 1;
    live.resize(4);
    for( int i = 0; i < mid*size; i += size )
    {
        live[0] += sin.substr(i, mid)+"\n";
        live[1] += sin.substr(i+mid-1, mid)+"\n";
    }
    for( int i = (mid-1)*size; i < sin.size(); i += size )
    {
        live[2] += sin.substr(i, mid)+"\n";
        live[3] += sin.substr(i+mid-1, mid)+"\n";
    }
}

int solve( Maze * maze )
{
    if( DEBUG ) {
        maze->print();
        cout << "(" << maze->m_Adit.x << "," << maze->m_Adit.y << ")\n";
    }

    // Find all of the targets.

    maze->findall( '0', maze->m_Adit );

    // Find the distance betweeen targets.

    for( auto & v : maze->m_Locations )
    {
        maze->findall( v.first, v.second );
    }

    if( DEBUG )
        for( auto & v : maze->m_Steps )
            for( auto p : v.second )
                cout << v.first << " to " << p.first << ": " << p.second << "\n";

    return maze->search( '0', "@" );
}

int main( int argc, char ** argv )
{
    bool do_bfs = false;
    Maze * maze = nullptr;
    int input = -1;
    string filename;

    while( *++argv )
    {
        string arg(*argv);
        if( arg == "debug" )
            DEBUG = true;
        else if( arg == "test" )
            TEST = true;
        else if( arg == "bfs" )
            do_bfs = !do_bfs;
    }

    vector<string> live1;
    vector<string> live2;

    if( TEST ) {
        for( auto pc : test )
            live1.push_back(pc);
        for( auto pc : test2 )
            live2.push_back(pc);
    } else {
        live1.push_back( readall("day18.txt") );
        split( live2, readall("day18b.txt"));
    }

    int sum = 0;
    for( auto && problem : live1 )
    {
        if( do_bfs )
            maze = new Maze_BFS( problem );
        else
            maze = new Maze_DFS( problem );

        sum += solve(maze);
    }
    cout << "Part 1: " << sum << "\n";

    sum = 0;
    for( auto && problem : live2 )
    {
        if( do_bfs )
            maze = new Maze_BFS( problem );
        else
            maze = new Maze_DFS( problem );

        sum += solve(maze);
    }
    cout << "Part 2: " << sum << "\n";
}
