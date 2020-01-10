#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <tuple>
#include <map>
#include <set>

bool TRACE = false;

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
"########################\n",

// Part 2, answer 72.
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

typedef std::map<char,std::tuple<Point,int,std::string> > lookupData_t;

template<typename T>
struct vector2d : public std::vector<T>
{
    std::vector<T> m_vec;
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
    std::vector<std::string> m_Maze;
    std::vector<Point> m_Adit;

    std::map<char,Point> m_Locations;
    std::map<char,std::map<char,int>> m_Steps;
    std::map<char,std::map<char,std::string>> m_Doors;
    std::map<std::string, int> m_Seen;

    Maze( std::istream && iss )
    {
        for( std::string ln; std::getline( iss, ln );  )
        {
            m_Maze.push_back( ln );
            for( int i = 0; i < ln.size(); i++ )
            {
                if( ln[i] == '@' )
                    m_Adit.emplace_back( i, m_Maze.size() - 1 );
            }
        }
    }

    void print()
    {
        for( auto ln : m_Maze )
            std::cout << ln << "\n";
    }

    void findall( char cfrom, Point & start )
    {
        std::map<Point, std::string> upcoming;
        m_Locations[cfrom] = start;
        upcoming[start] = "";
        vector2d<uint8_t> visited( m_Maze[0].size(), m_Maze.size() );
        int steps = 0;

        while( !upcoming.empty() )
        {
            std::map<Point,std::string> more;
            for( auto && m : upcoming )
            {
                Point cur = m.first;
                std::string  intheway = m.second;

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
                visited[cur] = 1;
                for( auto & facing : movements )
                {
                    Point next = cur + facing;
                    char ch = at(next);
                    if( visited[next] || ch == '#' )
                        continue;
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

    virtual int search( std::string sitting, std::string found ) = 0;
};


class Maze_BFS : public Maze
{
public:
    Maze_BFS( std::istream && iss )
        : Maze( std::move(iss) )
        {}
    int search( std::string sitting, std::string found );
};


class Maze_DFS : public Maze
{
public:
    Maze_DFS( std::istream && iss )
        : Maze( std::move(iss) )
        {}
    int search( std::string sitting, std::string found );
};


std::string sub(std::string s, int i, char c)
{
    return s.substr(0,i)+c+s.substr(i+1);
}

std::string ssort( std::string s )
{
    std::sort( s.begin(), s.end() );
    return s;
}

int Maze_BFS::search( std::string start, std::string found )
{
    std::map<std::string, int> unchecked;
    unchecked[start+found] = 0; 
    int nrobots = start.size();
    int result = 0;

    // Keep going as long as there are paths we haven't tested.
    // Because this is "breadth-first", each time through this loop
    // processed all of the paths of a single length.  The next pass
    // will be one step longer.
    while( !unchecked.empty() )
    {
        if( TRACE )
            std::cout << "Depth " << unchecked.begin()->second << "\n";

        std::map<std::string, int> more;
        std::vector<int> paths;

        // For each path that needs to be checked:

        for( auto & item : unchecked )
        {
            std::string sitting = item.first.substr(0,nrobots);
            std::string found = item.first.substr(nrobots);
            int steps = item.second;
            paths.push_back( steps );

            // For each robot:
            for( int si = 0; si < nrobots; si++ )
            {
                char s = sitting[si];

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
                    std::string doors = m_Doors[s][key];
                    if( std::any_of( 
                        doors.begin(), doors.end(),
                        [&found](char ch){ return found.find(tolower(ch)) == found.npos;})
                    )
                        continue;

                    // If this new path has alread been enumerated, and
                    // this path to the same state is shorter, keep it.

                    auto newsit = sub(sitting,si,key)+ssort(found+key);
                    if( more.find(newsit) != more.end() && more[newsit] <= steps+dstep )
                        continue;
                    more[newsit] = steps+dstep;
                }
            }
        }
        // When we have nothing new, we have our answer.
        if( more.empty() )
            return *std::min_element(paths.begin(), paths.end() );
        unchecked = more;
    }
    return 0;
}


int Maze_DFS::search( std::string sitting, std::string found )
{
    if( TRACE )
        std::cout << "New search " << sitting << " " << found << "\n";

    // If we've been in this situation before, we don't need to go again.
    if( m_Seen.find( sitting+found ) != m_Seen.end() )
    {
        return m_Seen[sitting+found];
    }

    std::vector<int> paths;

    // For each robot:
    for( int si = 0; si < sitting.size(); si++ )
    {
        char s = sitting[si];
        // For each key the robot can see:
        for( auto pt : m_Steps[s] )
        {
            char key = pt.first;
            if( key < 'a' )
                continue;
            // If we've already picked it up, ignore.
            if( found.find( key ) != found.npos )
                continue;

            // If there's a door in the way without a key, ignore.
            int dstep = m_Steps[s][key];
            std::string doors = m_Doors[s][key];
            if( std::any_of( 
                doors.begin(), doors.end(),
                [&found](char ch){ return found.find(tolower(ch)) == found.npos;})
            )
                continue;
            // Go explore this path.
            paths.push_back( dstep + search(sub(sitting,si,key), ssort(found+key)) );
        }
    }

    int ans = paths.empty() ? 0 : *std::min_element(paths.begin(),paths.end());
    if( TRACE )
        std::cout << (sitting+found) << ": " << ans << "\n";
    m_Seen[sitting+found] = ans;
    return ans;
}


int main( int argc, char ** argv )
{
    bool do_bfs = false;
    Maze * maze = nullptr;
    int input = -1;
    std::string filename;

    while( *++argv )
    {
        if( strcmp(*argv,"trace") == 0 )
            TRACE = true;
        else if( strcmp(*argv,"bfs") == 0 )
            do_bfs = !do_bfs;
        else if( isdigit(*argv[0]) )
            input = *argv[0]-'1';
        else
            filename = *argv;
    }

    if( do_bfs )
        if( filename.empty() )
            maze = new Maze_BFS( std::istringstream(test[input]) );
        else
            maze = new Maze_BFS( std::ifstream( filename ) );
    else
        if( filename.empty() )
            maze = new Maze_DFS( std::istringstream(test[input]) );
        else
            maze = new Maze_DFS( std::ifstream( filename ) );

    maze->print();
    for( auto & pt : maze->m_Adit )
    {
        std::cout << "(" << pt.x << "," << pt.y << ")\n";
    }

    // Find all of the targets.

    for( int i = 0; i < maze->m_Adit.size(); i++ )
    {
        maze->findall( '0'+i, maze->m_Adit[i] );
    }

    // Find the distance betweeen targets.

    for( auto & v : maze->m_Locations )
    {
        maze->findall( v.first, v.second );
    }

    if( TRACE )
        for( auto & v : maze->m_Steps )
            for( auto p : v.second )
                std::cout << v.first << " to " << p.first << ": " << p.second << "\n";

    if( maze->m_Adit.size() == 1 )
        std::cout << "Part 1: " << maze->search( "0", "@" ) << "\n";
    else
        std::cout << "Part 2: " << maze->search( "0123", "@" ) << "\n";
}
