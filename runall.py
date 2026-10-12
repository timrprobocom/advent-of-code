#! /usr/bin/python3

import os
import subprocess
import time

# python c++ go

# Python is slowest, then unoptimized C++, then go and optimized C++ are about the same.

def fetch(cmd):
    return subprocess.run( cmd, check=True, stdout=subprocess.PIPE).stdout.decode()

def prep(file, ext):
    if ext == '.cpp':
        subprocess.run(['g++', '--std=c++17', '-O3', '-o', file, file+ext, '-llapack'])
    elif ext == '.go':
        subprocess.run(['go', 'build', file+ext] )

def run(file, ext):
    if ext == '.py':
        return fetch(['python', fn+ext])
    else:
        return fetch(['./'+fn])

names = {'.py':'Python', '.cpp':'C++   ', '.go':'Go    '}

FIELD = 40

print('Python'.ljust(FIELD), 'C++'.ljust(FIELD), 'Go')
print('-'*(FIELD*3+2))

sums = [0,0,0]

for day in range(1,26):
    fn = f'day{day:02d}'
    gather = []
    times = []
    for lang in '.py','.cpp','.go':
        if os.path.exists(fn+lang):
            print(names[lang],end=' \r')
            prep( fn, lang )
            before = time.time()
            s = run( fn, lang )
            times.append( time.time() - before )
            gather.append( s.splitlines() )

    if not gather:
        continue
    print(fn,' ')
    pad = ''
    nextpad = ''
    for lns in zip(*gather):
        for i,ln in enumerate(lns):
            print(pad,end='')
            if len(ln) > FIELD:
                print(ln[:FIELD],end='')
                nextpad = ' '*((FIELD+1)*(i+1))
            else:
                print(ln.ljust(FIELD),end=' ')
                nextpad = ''
            nextpad = pad
        print()
    if len(gather) > 1 and ''.join(gather[0]) != ''.join(gather[1]):
        print("##### Python and C++ results do not match. *****")
    if len(gather) > 2 and ''.join(gather[0]) != ''.join(gather[2]):
        print("##### Python and Go results do not match. *****")
    for i,t in enumerate(times):
        sums[i] += t
        print( ('%10.3f'%t).ljust(FIELD), end=' ')
    print()

print("\nTotal times")
for t in sums:
    print( ('%10.3fs'%t).ljust(FIELD), end=' ')
print()

