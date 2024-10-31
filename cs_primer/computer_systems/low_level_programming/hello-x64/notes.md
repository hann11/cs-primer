assembly is a close match of machine code but makes it human readable rather than just raw byte encoding

usually 1line is 1 machine code instruction

\_main: label; doesn't end up in the code.

global \_main "directive" tells assembler to use \_main in the table to use in linking

section .text - ouput obj file turns stuff into machine code instructions that OS will know to load into text segment of memory to be exuected

section .data tells OS by way of obj file to end up in data segment; compile time data thats known when compiler (assembler) runs.
diff to stack/heap which is known at runtime

https://www.nasm.us/doc/

we are trying to do a hello world, want to write a string to stdout. requies a syscall

first instr: mov rax, 0x... move this value to the register rax. when you run syscall machine code instruction, causes cpu to switch to OS. looks in registers, based on that can perform system call.

we want certain registers to be populaed with values,so OS when looks knows what to do.

OS needs to know what syscall to do -> need that in the right register.

on macos, 0x02000004 is the syscall for write.
mov rdi 1, thats the file descriptor for stdout.
want to write the message, labelled in the assembly last line.

mov rsi, message;
mov rdx, 13; length of bytes to print. includes newline?

mov rax, ... another syscall setup
syscall is exit, want to exit with particular code.
tells OS to end the program.

xor rdi, rdi. xor whats in the rdi register with itself, updates rdi register inplace. zeros out the register.

xor rdi, rdi is cheaper than mov 0.

don't do anything after syscall for exit.

assembling the program:
nasm is an assembler;

`nasm -fmacho64 hello_mac.asm`
gives back object file
mach is for mac format

can compile just to object file with c compiler.

can look at disassembler which tries to put back into assembly.
`objdump -d hello_mac.o`

```
Disassembly of section __TEXT,__text:

0000000000000000 <_main>:
       0: b8 04 00 00 02                movl    $33554436, %eax         ## imm = 0x2000004
       5: bf 01 00 00 00                movl    $1, %edi
       a: 48 be 00 00 00 00 00 00 00 00 movabsq $0, %rsi
      14: ba 0d 00 00 00                movl    $13, %edx
      19: 0f 05                         syscall
      1b: b8 01 00 00 02                movl    $33554433, %eax         ## imm = 0x2000001
      20: 48 31 ff                      xorq    %rdi, %rdi
      23: 0f 05                         syscall
```

each assembly instruction here (not always) has a machine code instruction.

the machine code insructions are variable length. xor takes 3 bytes, mov takes a bit more
syscall easy 2 byte instruction

the disassembly is a little differnet to what we wrote; movl is used to indicate that it's a 4byte move. operand order is switched too; rdi, 1 to $1, %edi.
due to being two common assembly syntaxes for x86; intel and at&t. disassembly is at&t. nasm uses intel syntax, easier to read and work with.

`objdump -x86-asm-syntax=intel -d hello_mac.asm`

we now have non-executable object file. doesn't have prelude to execute before main executes.

to make it executable, need to run it through the LINKER.

`ld hello_mac.o -o hello -macosx_version_min 11.0 -L /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/lib -lSystem -no_pie` (requires Rosetta)

We can also step through the execution via LLDB.

`lldb  ./hello`

`b main` to set breakpoint at main

`r` to step

```
Process 94497 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = breakpoint 1.1
    frame #0: 0x0000000100000f93 hello`main
hello`main:
->  0x100000f93 <+0>:  mov    eax, 0x2000004
    0x100000f98 <+5>:  mov    edi, 0x1
    0x100000f9d <+10>: movabs rsi, 0x100001000
    0x100000fa7 <+20>: mov    edx, 0xd
Target 0: (hello) stopped.
```

check `reg re eax`

```
eax = 0x08a01910
```

step with `s`

```
(lldb) s
Process 94497 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = instruction step into
    frame #0: 0x0000000100000f98 hello`main + 5
hello`main:
->  0x100000f98 <+5>:  mov    edi, 0x1
    0x100000f9d <+10>: movabs rsi, 0x100001000
    0x100000fa7 <+20>: mov    edx, 0xd
    0x100000fac <+25>: syscall
Target 0: (hello) stopped.
```

note movabs rsi, 0x100001000 the value there is the string hello world.

`reg re eax`

```
eax = 0x02000004
```

mov modified the register to store that.

one can check registers with
`reg re` or `register read`

next we move 1 to rdi (it already had 1 in it)

before we do movabs rsi, 0x100001000
rsi = 0x00000003040ea2e8

now step

reg re rsi
rsi = 0x0000000100001000 message
