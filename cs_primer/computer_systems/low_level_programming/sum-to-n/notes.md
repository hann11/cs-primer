take arg n, an integer

in a loop, sum from numbers 1 to n

expose to what a loop looks like at a level of machine
for/while etc get compiled to something diff at machine level

figure basic arithmetic
consider what a "function" means

heaps of instructions to pick from for x86
thibk categorically; 3-4 groups.

1. arithmetic; there is an add instruction.
   add has diff forms of instruction.
   first instruction; add "al" 1byte worth to an 8bit value; imm8 (encoded in the register). can do for a number like 5

can just add eax to ebx for instance and it should work

2. change location of instruction pointer / program counter - whats the next thing to execute? usually goes up sequentially. fetch decode execute.
   if you call a function, the IP will move to the definition of the function pointer in memory. "jump".
   conditional/switch statement; conditionally changing instruction pointer value. these are all versions of "jump".
   conditional branch = jump in x86. arm calls them branch.
   Jcc -> jump if condition is met. has heaps of options. JGE: Jump if greater than or equal to. If greater than zero; setup zero in a register, then jge. when not zero it does stuff.

   result of comparison will be in flag bits. by doing comparison, flag bits will be set.

compare: CMP; compare two operands.

3. memory manipulation; lots from the instruction mov. not relevant here.

this exercise is for arithmetic and looping.

.. when we have code that interoperates, need convention for how functions are invoked and some aspects of the stack.

i.e. read first arg; where is it? on unix dervied OS, convention is to put first arg in the register rdi. "calling convention".

for this exercise; the first arg (only arg here) will be in rdi. it's a 32bit int so will also be in edi. return value will go into rax/eax.

section .text
global sum_to_n
sum_to_n: # write program here. needs a loop and does stuff.
ret

no syntax in assembly saying sum_to_n is a function that takes arguments. sum_to_n is just a label.
will be assemlbed to have a location the test code jumps to.
before it jumps, it puts n into rdi.
read n from rdi. thats how functions work at a low level.
put result into rax.
ret is a fancy jump that'll jump back to test runner.

make will
compile tests.c into tests.o

compile sum_to_n to sum_to_n.o
links them together
creates output file tests

compile, assemble, link, execute all in one

first obj; return 0.

## Notes from solving:

run without anything returns whatever is in rax to start with, note its non zero.

mov rax, 0 returns 0

mov rax, rdi moves rdi to rax

rdi is the function input from c

thinking approach:
need to do a check if we still need to loop:

- cmp something to something
- - result stored in eflags register
- - jcc then checks this result and will jump out if not right ???

need somewhere to store the sum and the number to compare.
rcx

store; sum
store; n (will be in rdi)
store; current n we are up to while summing

compare n to current n

how do we enter the loop?
tbd; jump?

how do we exit the loop?
cmp rdi and loop counter
jg ..?

##pseudocode

set rax to 0 via xor itself or mov rax 0
same with rcx

enter loop;
check if rcx is greater than rdi using `cmp`
jump if greater than and ret, else:
add rax and rcx
increase rcx by 1

solution:

```
section .text
global sum_to_n
sum_to_n:
	mov rax, 0
	mov rcx, 0

loop:
	add rax, rcx
	cmp rcx, rdi
	jge end
	inc rcx
	jmp loop

end:
	ret
```

can make it cleaner:
add rax, rcx
inc rcx
cmp rcx, rdi
jle loop
ret

can also do it in reverse without using rcx:
add rax, rdi
dec rdi
cmp rdi, 0
jge loop

## oz solution notes

get first case to pass;
`mov rax, 0`

variables are a high level construct like n = 5. n in a stack frame, register, stack memory, moves around. register allocation is a compiler problem. it's done for us

we need to store the accumulator in a registry ourselves

as we are using ints, refer to last 32 bits of register. edi instead of rdi.

semantically mov is fine for rax, rax
it turns out its faster to xor ( 1 fewer bytes to encode)

apparently from bruce dawson: mov eax, 0 -> eax 32 bit register, constant 32 bits, get a 5 byte instruction

xor eax, eax is just 2 bytes long.

SUB modifies flags...
if result is zero...
can look at flag with jump, can omit the compare.

```
add eax, edi
sub edi, 1
jg _loop; checks if 0 flag not on. (greater than)
ret
```

this is a do while loop in C, we do something befre checking loop True

Optimized:

```
mov rax, rdi ; copy rdi to rax
inc rax ; increase by 1
imul rax, rdi ; multiply together
shr rax, 1 ; shift right by 1 bit, equivalent to dividing by 2
ret ; fin
```
