## fetch decode execute

simplified, basic model of how a cpu works

assume cpu has a register that stores one instruction

fetch instruction from memory and store in the register
instruction is a sequence of bits (maybe add contents of register 1 and register 2)

decode unit reads the bits, sends signals across CPu to maybe the ALU to perform the addition
components say this register is read, this register is written to.

execute; ALU does the execution

next instruction comes through. might get function call or flow control conditional; execute might be figuring out the next instruction to fetch/decode/execute

keep track of the current instruction in the program counter "instruction pointer" in x86, stores the address of the next instruction in memory to fetch/decode/execute.

highly iterative machine.

## computer arch / instruction set / microarchitecture

comp arch: generalised design of cpu, isa, microarch, etc.
instruction set; how it's exposed; machine code processor reads and acts upon. word size, registers, etc.
microarchitecture; amd vs. intel etc. how the processor implements the ISA.

64bit version of x86; diff organisations have same instruction sets. amd came up with instruction set, intel used in x86
ISA is from amd64. microarch's are different and usually quite opaque.

isa; opcodes, machine instructions available, etc.

## registers in x86

```
(lldb) reg re
General Purpose Registers:
       rax = 0x0000000108a01910
       rbx = 0x0000000108a01bd0
       rcx = 0x00000003040ea470
       rdx = 0x00000003040ea2f8
       rdi = 0x0000000000000001
       rsi = 0x00000003040ea2e8
       rbp = 0x00000003040ea2c0
       rsp = 0x00000003040ea0a8
        r8 = 0x0000000000000000
        r9 = 0x0000000000008000
       r10 = 0x0000000000000000
       r11 = 0x0000000000008000
       r12 = 0x00000003040ea0d0
       r13 = 0x0000000000000000
       r14 = 0x0000000100000f93  hello`main
       r15 = 0x00000003040ea250
       rip = 0x0000000100000f93  hello`main
    rflags = 0x0000000000000202
        cs = 0x000000000000002b
        fs = 0x0000000000000000
        gs = 0x0000000000000000
```

a lot of complexity in this ISA is to do wit backward compatibility to 16bit registers in the 70s

ax
bx
cx
dx
di <- dest
si <- stream stuff source
bp
sp <- stack pointer
ip <- instruction pointer (currently executing instruction)
flags <- stuff from prev instructions (did last overflow, etc, did last comparison == 0)

all above are 16bit registers

if using the above on a 64bit machine, they are aliases for the lower order 16 bits of the physical 64 bit registers

intel named eax - extended ax with 32bits.

rax - 64bit - includes eax and ax.
r just stands for register

rip - 64bit instruction pointer

see all in lldb; `reg re --all`
