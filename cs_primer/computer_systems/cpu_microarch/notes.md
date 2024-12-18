# About this module

Peel back the abstraction layer that the CPU provides, start to understand the implementation of the CPU (Microarchitecture)

whole point of abstraction is to program to the abstraction; assembly etc, CPU fetch decodes executes.

that's reasonable to consider, but also nice to see how the CPU actually works and how the abstraction leaks.

It is extremely complex and quite blackbox, but some simple examples might show how the abstraction leaks.

# Moving beyond fetch/decode/execute

Started by saying CPU fde a machine code instruction every CPU cycle. Decent starting point.

REALITY; Skylake https://en.wikichip.org/wiki/intel/microarchitectures/skylake_(client)

![alt text](<../../../Screenshot 2024-12-13 at 3.31.58 PM.png>)

if you feel the "API" of the CPU is enough, then stay with that abstraction. however let's dive a bit deeper.

no longer have single cycle cpu's. used to.

### Pipelining

more efficient to design a CPU where instructions move through CPU like a factory. progressive evaluation of instruction through the stages.
consider fetching done indep of decoding indep of execution, indep of writing to registers.

while one being decoded, next can be fetched, etc.

keep all stations engaged, more efficient.

Pipelining; started non Intel then adopted.

- around 20 stages (arch dependent)
- initial latency around 15-20 cpu cycles
  whenever see a branch instruction, could take 15-20 cpu cycles to fully eval a branch instruction. (if, then)
  until evaluated, don't know whether to execute next instruction or exit or else or whatever.
- rather than waiting 15-20 cpu cycles, we have Branch Prediction

### Branch Prediction / speculative execution

bc we have additional latency, would like to guess the outcome of the final eval through the pipe of a branch instruction. Then speculatively execute the instructions we believe would be next. If number odd, do this. Say we guess it's odd, we do that path and execute that. Push those instructions (takes 15-20 cpu to know answer) through pipeline.

Retirement portion; buffer of results might get retired if the branch is correct. In the interim, if a branch misprdeiction, lets see.

If every branch correct, skip the 15-20 cpu cycle.

Cost of misprediction; flush all partial results.
Want tokeep factory busy; build things without outcome. Guessed grey widget instead of red. Better to take risk and toss than have cost of waiting.

If you have poor branch preiction, you can restructure code to make it better.

### Instruction fetching

Not necessarily fetching 1 instruction at a time. Kinda batched. Fetches 16 bytes at a time (16bytes/cycle in image)
populate instruction cache. Dont wanna go to main memory (slow).
Prefetching too.

Decoded in 4 ways; complex decoder, simple decoders. Up to 5 microops.

Simple model; machine code insttruction decoded and executed.
No longer just executig machine code instructions. MCI are decoded to uops. uops are a language internal to cpu.
machine code instruction an external api.
add eax, [ebx] (dereference from mem) - gets translated to micro-operations.
they aren't public. People try reverse engineering but difficult.

can instruction fuse, treat multiple operations as one. more efficient cpu design.

### Out of order execution; can do with microops.

can still do without microops, but it helps a lot.

it's the idea that given a stall, trying to retrieve from memory, could do some eecution of other instructions elsewhere that might come later; breaks the idea of FDE once again.

if can split an add into load and arithmetic add (eax [ebx]) cpu can figure what to do out of order.

Execution Engine has multiple Ports, with different execution units they point to. There's 4 integer ALU's and a few different other execution units.

### Numerous execution units, organised into Ports (1-8 in Skylake) rather than just 1 ALU (don't execute 1 instr at a time)

means up to 8 pieces of execution. of course this requires out of order execution.
if you have a+b+c, it's blocked on adding b to a and c to a. Requires two operations. If code laid out differently, what referecnees what, what dependencies between microops, you may get a significant degree of paralleism in the EE.
Integer arithemtic; add everything to same accumulator, CPU can't tell, need to be done sequentially. Pushed one at a time.
But what if you have multiple accumulators? Merge them later. Do the adds independently. Can do 4 executions per CPU cycle. HINT for problem1.
Throughput from CPU of 4 additions retired per CPU cycle.

Can also have bottleneck reading from RAM. Depends if memory bound. If everything running smoothly, throughput should be 4 adds/cycle.

Previous model implied general purpose registers of the word size; 16 registers all 64bits. HOWEVER we have Register renaming.

### Register Renaming

When writing assembly, specifying rgisters. They're just logical names for registers. CPU has its own set of registers; skylake might have 160 registers for integers, which are reusbale slots that can have a name associated when the cpu describes.
useful if have add eax [ebx] 2 microops

you may name registers in a way where assumed dependency of one instruction on another.
add to eax, xor, add again
xor breaks the dependency chain; prev operations then aren't relevant to the register. CPU can logically think as separate registers and can do more out of order execution.

aside; can have up to 512 bit wide registers (not just 64). if you have long registers

### SIMD

General Purpose Registers vs AVX-512
64bit (1int op per time) vs. 16 32 bit integers can fit into a register/ shorts can do 32 16bit ints.

If have a pair of registers and fit 16 ints per register, you can do pairwise vector ops.

Look at all ints in SIMD reg 1, reg 2, then can do that.

Vector dot product; huge parallelism from larger registers
single instruction, multiple data

we just spoke about 1 core above.
You can get way more, n cores.
