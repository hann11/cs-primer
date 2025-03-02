# fib

fkn tough problem. stared at fac and solved it non-recursielvey, then got help from cs:app with how to write it recursively.

with factorial;

if n <= 1, return 1,
else, return n \* fact(n-1)

with recursive call, it goes down the tree, then up the tree, ie.

fac(4)

return 4 * fac(3)
calls fac(3)
return 3*fac(2)
calls fac(2)
return 2*fac(1)
return 2*1
-> return 3*2
-> return 4*6
need to rollup, need to have access to the n to multiply by, so we store in the stack, rolls up and down.

excluding base case;

push rdi (n)
dec rdi
call fac
pop rdi
imul rax, rdi

need to push and pop together.

fib is a bit harder, need two recursive calls, also need to store fib(n-1) return value as fib(n-2) will clobber it

push rdi (n)
dec rdi (n-1)
call fib
pop rdi (n) re-align stack
push rax (return from fib(n-1))
sub rdi, 2 (n-2)
call fib
pop rcx (return from fib(n-1))
add rax, rcx
ret

## oz notes

starts with pseudocode, if n<=1, return n.

general case:
return fib(n-1) + fib(n-2)

```
    mov eax, edi (base case)
    once loaded, compare edi to 1
    jle .end

    ; general case, naively want to compute n-1
    sub edi, 1
    call fib ; decrement n and call fib, call fib on n-1.
    ; then get a result in eax
    sub edi, 1
    call fib; f(n-2). problem is we are modifying edi within fib and eax within fib. shared within all the fib calls that are currently running (not ret'd)
    ;problem is that edi keeps going we need to keep the value of it on the stack and restore it

.end:
    ret ; eax loaded with n
```

```
    mov eax, edi
    cmp edi, 1
    jle .end

    sub edi, 1
    push rdi ; push n-1 to top of the stack
    call fib
    pop rdi ; get back n-1 into edi

    push rax ; keep the result of fib(n-1) prevent clobbering in next fib call
    sub edi, 1
    call fib

    ; eax has f(n-2) need to add, its ontop of stack - n-1
    pop rcx ;
    add eax, ecx
    ret

.end
    ret
```

critical to have as many pushes as pops, otherwise stack will be stuffed for everything.

in terms of stack alignment; call pushes return address (8bytes) to the stack.

need to push full 64bit register values (rdi) instead of edi (32bit)

stack grows toward smaller addresses, reduces stack pointer size by 8bytes when pushing 64bit to the stack.

stack alignment; +8, +16, then can call with +16. don't fully get this +8 +16
for each call, before the call, need to be multiple of 16. oz says no big deal.
push extra 8bytes if 8bytes off to be aligned to get multiple of 16.

be careful not to use rbx as main uses that; need to check x86 calling convention. important to understand the calling convention.

not every function local needs to go onto the stack, just if gonna call other fns/be called by other fns. prevent clobbering on function calls of registers.
