#include <vector>
#include <fstream>
#include <sstream>
#include <string>

typedef unsigned short byte_t;
typedef std::vector<std::vector<short>> ShortMatrix;
typedef std::vector<std::vector<int>> IntMatrix;
typedef std::vector<std::vector<int64_t>> LongMatrix;

typedef std::vector<std::string> StringVector;

StringVector split( std::string src, std::string delim="\n" )
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

std::vector<StringVector> split_chunks( const std::string & src )
{
    std::vector<StringVector> build;
    auto mid = src.find("\n\n");
    if( mid == std::string::npos )
        return build;
    build.push_back( split( src.substr( 0, mid )) );
    build.push_back( split( src.substr(mid+2)) );
    return build;
}

template<typename T>
struct Point {
    T x;
    T y;

    Point( int _x=0, int _y=0)
    : x(_x), y(_y)
    {}

    bool operator<(const Point & other) const
    {
        return x == other.x ? y < other.y : x < other.x;
    }

    bool operator==(const Point & other) const
    {
        return x==other.x && y == other.y;
    }
};


// There are three common ways my solutions fetch the inputs.
// 1. Get the entire input as a string:
//    string input = TEST ? test : file_contents("day10.txt");
// 2. If short, embed both the live and test data in the code:
//    string input = TEST ? test : live;
// 3. Create a stringstream containing the input:
//    stringstream input;
//    if( TEST )
//        input << test;
//    else
//        input << ifstream("day22.txt").rdbuf();


std::string file_contents(const char * name)
{
    std::stringstream buffer;
    buffer << std::ifstream(name).rdbuf();
    return buffer.str();
}


template<typename T>
bool between( T low, T val, T hi )
{
    return (low <= val) && (val < hi);
}
