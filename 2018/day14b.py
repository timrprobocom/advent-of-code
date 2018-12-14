test = (
    ( 5,  1245, 5 ),
    ( 9, 51589, 5 ),
    ( 18, 92510, 5 ),
    ( 2018, 594142, 6 ),
    ( 260321, 260321, 6 ),
)



def find( value, part1 ):
    digits = [int(digit) for digit in str(value)]
    scores = [3, 7]
    elf1, elf2 = 0, 1

    while (
        len(scores) < value + 10
    ) if part1 else (
        scores[-len(digits):] != digits and scores[-len(digits)-1:-1] != digits
    ):
        total = scores[elf1] + scores[elf2]
        scores.extend(divmod(total, 10) if total >= 10 else (total,))

        elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
        elf2 = (elf2 + 1 + scores[elf2]) % len(scores)

    print(
        ''.join(str(score) for score in scores[value:value+10])
    if part1 else
        len(scores) - len(digits) - (0 if scores[-len(digits):] == digits else 1)
    )

for a,b,c in test:
    find( a, True )
    find( b, False )
