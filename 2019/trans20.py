from PIL import Image

maze = [ln  for ln in open('day20.txt').read().splitlines()]

w = len(maze[3])
h = len(maze)


m = Image.new( 'RGB', (w*4,h*4) )
print( m.size ) 

for y,ln in enumerate(maze):
    for x,ch in enumerate(ln):
        if ch == ' ':
            continue
        if ch == 'A':
            c = (32,32,255)
        elif ch == 'Z':
            c = (32,255,32)
        elif ch.isalpha():
            c = (224,64,64)
        elif ch == '.':
            c = (128,128,128)
        elif ch == '#':
            c = (192,192,192)
        for dy in range(4):
            for dx in range(4):
                m.putpixel( (x*4+dx,y*4+dy), c )
m.save('maze20.png')

