## logical flow

C logic;

int bitvec 0;
char c;

given pointer to char (1byte) s (memory address)
set as char c = \*s (the actual char)

if c not null byte

- tolower c - check if 'A' <= c <= 'Z'
- - if so, add 32 to uppercase ascii

- if 'a' <= c <= 'z'
- - add to bitvector.

finish:
if bitvec & mask == mask, return 1, else return 0

first pass assembly logic;
the pointer is stored in rdi. note it is 1 byte per char

xor ecx, ecx to store bitvec
xor edx, edx to store char

in loop:
movzx edx, [rdi] ; move the char to register
cmp edx, 0 ; check if null byte
je finish ; exit loop if null byte

cmp edx, 65 ; check if less than 'A'
jle loop ; restart / continue
cmp edx, 90 ; check if greater than 'Z'
jge lowercheck ;
add edx, 32
jmp lowercheck ;

lowercheck:
cmp edx, 97 ;
jle loop ;
cmp edx, 122 ;
jge loop ;
sub edx, 97
shl edx 1
now or equals to ecx
jmp loop;

finish:
ecx and mask XOR mask
mov rax 1 if zero
else mov rax 0

note solved with a few fixes ^

## oz solution notes (note he uses a simpler C program)

```
%define MASK 0x07fffffe  ; nasm has macros. preprocessor deals with it.

section .text
global program
pangram:
    ; rdi source string
    xor ecx, ecx ; bs = 0
.loop:
    movzx edx, byte [rdi] ; c = *s ; mov zero extension
    cmp edx, 0
    je .end ; move to end
    add rdi, 1
    cmp edx, '@' ; works as @ one byte. if c <= 64, continue
    jl .loop
    and edx, 0x1f ; TODO, needed? doesnt need as takes mod32 in bts. this is to collapse lowercase and uppercase. this line is not needed.
    bts ecx, edx ; bitset on ecx, set bits on in edx. C should find this but who knows. Go maybe not.
    jmp loop
.end:
    xor eax, eax
    and ecx, MASK
    cmp ecx, MASK
    sete al, 1; set on condition (set when equal)
    ret
```
