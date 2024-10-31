calling convention: for xmm registers (not x87 registers)
first two args in xmm0, xmm1
return value in xmm0 too. good design with inplace operations

mulss - mul scalar single precision.
xmm design to do vector pairwise ops if you want. do all at once, a nice optimisation

need a reference to pi/3.
can't encode an imm into floating point like imul.
cant do that for mulss. but can dereference an address.

mulss xmm0, xmm0
mulss xmm0, xmm1
mulss xmm0, [pi]

section .rodata gives write protection, can't overwrite it.

define pi as a floating point. skip a step by encoding pi/3, dont need to division. save a cpu cycle.

here we use xmm registers with specific instructions for multiplication (mulss).

operate over vectors so will make code fkn fast!
