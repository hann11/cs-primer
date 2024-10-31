## matrix access

given a pointer to memory in rdi
and num of rows and cols
access the row index and col index of the matrix

i.e {{1,2,3}, {4,5,6}}
nrows = 2
ncols = 3
rowindex = 1
colindex = 2

pick out 6

you can access the right pointer by
orig pointer + (row*n_cols + col)*4 - figured on paper

rcx has the row index
imul rcx, rdx > rdx has n_cols
add rcx, r8 > r8 has col index
imul rcx, 4 > multiply by 4
add rdi, rcx > add rdi (orig pointer to start of array)
mov rax, [rdi] > access memory at the point, move to output register

## oz solution notes

machine doesnt distinguish between address or integers. its just a 64 bit register.
you can add integers to memory addresses to increase that memory address.

oz
imul ecx, edx
add ecx, r8d
imul ecx, 4
add rcx, rdi <- does full 64bit as its a pointer, not int now

mov rax, [rcx] <- take the integer from that memory location. like a pointer in C.

mov can be complicated.

double arr[4] - we are looking at a location, pointer arr + 4\*8 as size of double is 8.

x86 can do arr+i\*8
to simplify a bit

mov rax, [rdi+4*rcx]
can drop the add rcx, rdi
and the imul ecx, 4
