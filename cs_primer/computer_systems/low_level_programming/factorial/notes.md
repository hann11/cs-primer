take arg n, return factorial

will deal with function calling itself, so registers will get clobbered
need to use stack to save registers

whats the stack?
the stack is a region of memory that grows and shrinks as functions are called and returned
it's a LIFO data structure
when a function is called, the stack grows
when a function returns, the stack shrinks
the stack is used to save the state of the program, so that the program can return to where it left off

how a factorial function might work in assembly:

take in an input n (in rdi)
set rax to 1

loop:
if n is <= 1, ret
multiply rax by n
decrement n
