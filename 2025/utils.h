#include <vector>
#include <fstream>
#include <sstream>
#include <string>

typedef unsigned short byte_t;
typedef std::vector<std::vector<short>> ShortMatrix;
typedef std::vector<std::vector<int>> IntMatrix;
typedef std::vector<std::vector<int64_t>> LongMatrix;

typedef std::vector<std::string> StringVector;

StringVector split(const std::string src, const std::string delim = "\n")
{
    StringVector sv;
    int was = 0;
    for (
        int j = src.find(delim);
        j != -1;
        was = j + delim.size(), j = src.find(delim, was))
    {
        sv.push_back(src.substr(was, j - was));
    }
    sv.push_back(src.substr(was));
    return sv;
}

std::vector<StringVector> split_chunks(const std::string &src)
{
    std::vector<StringVector> build;
    auto mid = src.find("\n\n");
    if (mid == std::string::npos)
        return build;
    build.push_back(split(src.substr(0, mid)));
    build.push_back(split(src.substr(mid + 2)));
    return build;
}

// Splits on all groups of whitespace.  Works for string and int types.
// Anything that has an operator>>.

template<typename T>
std::vector<T> split_fields(const std::string src)
{
    std::vector<T> tokens;
    std::stringstream ss(src);
    T token;

    // Extract whitespace-separated tokens.
    while (ss >> token)
    {
        tokens.push_back(token);
    }
    return tokens;
}

template <typename T>
struct Point
{
    T x;
    T y;

    Point(int _x = 0, int _y = 0)
        : x(_x), y(_y)
    {
    }

    Point operator+(const Point<T> &other) const
    {
        return Point(x + other.x, y + other.y);
    }

    Point operator-(const Point<T> &other) const
    {
        return Point(x - other.x, y - other.y);
    }

    Point operator+=(const Point<T> &other)
    {
        x += other.x;
        y += other.y;
        return *this;
    }

    bool operator<(const Point &other) const
    {
        return x == other.x ? y < other.y : x < other.x;
    }

    bool operator==(const Point &other) const
    {
        return x == other.x && y == other.y;
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

std::string file_contents(const char *name)
{
    std::stringstream buffer;
    buffer << std::ifstream(name).rdbuf();
    return buffer.str();
}

template <typename T>
bool between(int low, T val, int hi)
{
    return (low <= val) && (val < hi);
}

template <typename T, typename U>
bool is_in(T ele, U &coll)
{
    return coll.find(ele) != coll.end();
}

template <typename T>
bool is_in(T ele, std::vector<T> coll)
{
    return std::find(coll.begin(), coll.end(), ele) != coll.end();
}
