section .data

a:      dd      1
b:      dd      0
c:      dd      0
d:      dd      0
e:      dd      0
f:      dd      0
g:      dd      0
h:      dd      0

%macro mkstring 2
    %1: db %2,10
    .len equ $ - %1
%endmacro

mkstring the_end, "The end"
mkstring bump_d, "Bumped d"
mkstring bump_h, "Bumped h"
mkstring one_rnd, "One round"

%macro fetch 1
    %ifnum %1
        mov     eax, %1
    %elifidn %1,d
        mov     eax, edx
    %elifidn %1,g
        mov     eax, ecx
    %else
        mov     eax, [%1]
    %endif
%endmacro

%macro store 2
    %ifidn %2,d
        %1     edx, eax
    %elifidn %2,g
        %1     ecx, eax
    %else
        %1     [%2], eax
    %endif
%endmacro


%macro xset 2
    fetch       %2
    store       mov, %1
%endmacro

%macro xmul 2
    fetch %2
    imul     eax, [%1]
    store    mov, %1
%endmacro

%macro xsub 2
    fetch %2
    store sub, %1
%endmacro

%macro xjnz 2
    %ifnum %1
        jmp     %2
    %else
        fetch   %1
        test    eax, eax
        jnz     %2
    %endif
%endmacro

%macro puts 1
    push dword %1.len
    push dword %1
    push 1
    mov eax, 4
    sub esp, 4
    int 0x80
    add esp, 16
%endmacro

section .text
global start
start:

.l0:  xset b, 65
.l1:  xset c, b
.l2:  xjnz a, .l4 ; 2
.l3:  xjnz 1, .l8 ; 5
.l4:  xmul b, 100
.l5:  xsub b, -100000
.l6:  xset c, b
.l7:  xsub c, -17000
.l8:  xset f, 1
.l9:  xset d, 2
.l10: xset e, 2
.l11: xset g, d
.l12: xmul g, e
.l13: xsub g, b
.l14: xjnz g, .l16 ; 2
.l15: xset f, 0
.l16: xsub e, -1
.l17: xset g, e
.l18: xsub g, b
.l19: xjnz g, .l11 ; -8
.l20: xsub d, -1
.l21: xset g, d
.l22: xsub g, b
.l23: xjnz g, .l10 ; -13
    puts one_rnd
    jmp .l32
.l24: xjnz f, .l26 ; 2
.l25: xsub h, -1
    puts bump_h
.l26: xset g, b
.l27: xsub g, c
.l28: xjnz g, .l30 ; 2
.l29: xjnz 1, .l32 ; 3
.l30: xsub b, -17
.l31: xjnz 1, .l8 ; -23

.l32:
    ;; printf

    puts the_end

    ;; Exit

    push dword 0
    mov eax, 1
    sub esp, 12
    int 0x80


