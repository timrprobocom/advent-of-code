import sys
from pprint import pprint


test = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [line.rstrip() for line in open('day04.txt')]

calls = [int(x) for x in data[0].split(',')]
data.pop(0)
data.pop(0)

# We'll just create a set of boards, each board is a 9-element list.

boards = []
board = []
for line in data:
    if not line:
        boards.append(board)
        board = []
    else:
        board.extend( [int(x) for x in line.split()] )
boards.append(board)
print(len(boards))

def check(board):
    for row in range(5):
        if sum(board[row*5:row*5+5]) == -5:
            return True
        if all(board[i*5+row] < 0 for i in range(5)):
            return True
    return False

def part(part,calls,boards):
    boards = [row[:] for row in boards]
    done = [False]*len(boards)
    for call in calls:
        for bno,board in enumerate(boards):
            if done[bno]:
                continue
            if call in board:
                i = board.index(call)
                board[i] = -1
                if check(board):
                    if DEBUG:
                        print("WINNER", call, bno, board)
                    done[bno] = True
                    if part == 1 or all(done):
                        sumx = sum(x for x in board if x >= 0)
                        return sumx * call

print("Part 1:", part(1, calls, boards) ) # 34506
print("Part 2:", part(2, calls, boards) ) # 7686

