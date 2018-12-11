import md5
import itertools

key = 'uqwqemis'
#key = 'abc'

cnt = 0
chars = ['-']*8
while 1:
    raw = key + str(cnt)
    md5x = md5.md5(raw).hexdigest()
    if md5x[0:5] == '00000':
        if md5x[5] < '8':
            pos = ord(md5x[5]) - ord('0')
            if chars[pos] == '-':
                chars[pos] = md5x[6]
                print raw, md5x, ''.join(chars)
                if not '-' in chars: break
    cnt += 1

print ''.join(chars)



