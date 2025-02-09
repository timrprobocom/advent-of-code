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

print('Python'.ljust(30), 'C++'.ljust(30), 'Go')
print('-'*92)

for day in range(1,26):
    fn = f'day{day:02d}'
    gather = []
    times = []
    for lang in '.py','.cpp','.go':
        if os.path.exists(fn+lang):
            print(lang,end=' \r')
            prep( fn, lang )
            before = time.time()
            s = run( fn, lang )
            times.append( time.time() - before )
            gather.append( s.splitlines() )

    print(fn)
    pad = ''
    for lns in zip(*gather):
        for i,ln in enumerate(lns):
            print(pad,end='')
            if len(ln) > 30:
                print(ln)
                pad = ' '*(31*(i+1))
            else:
                print(ln.ljust(31),end='')
                pad = ''
        print()
    for t in times:
        print( ('%10.3f'%t).ljust(31), end='')
    print()

