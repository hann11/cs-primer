# Video

nothing fancy about this problem. No special algorithm. need to go through and add the numbers.

Nothing silly, all sequentially accessed.

We could improve this and make it faster, with some caveats.
Watch the explainer first (microarch)

need 3rd party library (google benchmark)

Keep optimization at O1. Realistic, makes most basic optimisations. At O0, not thinking about optimisations. Copy values in/out of stack and memory. O1 keeps in regsiters.
O2 very hard to beat. Will consider disassembly of O2.

At O1, you can make some improvements to the function at O1, might disappear at O2.

Whats the point? Lose value at high level optimisation
Challenge to find simple example to motivate these topics

O2 might be compilers interpretation/understanding of the microarchitecture.

Just playfully pull the thread and see what happens; have fun.

## Sol

Struggle to install Cmake, but based on oz Expanded FDE video, thinking:

if you have a+b+c, it's blocked on adding b to a and c to a. Requires two operations. If code laid out differently, what referecnees what, what dependencies between microops, you may get a significant degree of paralleism in the EE.
Integer arithemtic; add everything to same accumulator, CPU can't tell, need to be done sequentially. Pushed one at a time.
But what if you have multiple accumulators? Merge them later. Do the adds independently. Can do 4 executions per CPU cycle. HINT for problem1.
Throughput from CPU of 4 additions retired per CPU cycle.

Can also have bottleneck reading from RAM. Depends if memory bound. If everything running smoothly, throughput should be 4 adds/cycle.

So, split into 4 accumulators. Then add those up.
Rather than wait on the sequential add.

Oz: Utilising multiple execution ports on the machine. All can be used in Parallel.
4 have integer ALU's. Can do 4 additions per CPU cycle.
Need 4 independent additions.

Need to clearly give independent executions to the CPU.

Rather than one accumulator total, initialise 4.

```
int sum(int *nums, int n) {
    int t1=0,t2=0,t3=0,t4=0;
    for (int i=0, i <n, i += 4) {
        t1 += nums[i];
        t2 += nums[i+1];
        t3 += nums[i+2];
        t4 += nums[i+3];
    }
    return t1+t2+t3+t4
}
```

If perfectly bottlenecked by the sequential adds, could get a 4x speedup. However we'll be bottlenecked elsewhere.
It about halved except for the larger vrsion.

1m additions in 700 microseconds. Better than 1 addition per nanosecond

1000 additions in 700 nanoseconds

1 addition in 0.7 nanoseconds. Not 1 per cpu cycle yet.

Trying to get at; surprising speedup, convoluted, less readable. However hacks the microarchitecture

you can use the vector avx registers and do multiple additions at once.

can use intrinsics in c++ code to do it and get it right.

making assumption in this example that n // 4.

## Looking at the dis.

Edit the Makefile to -O2. Compiler improves on the baseline.Hectically. 1m in 300 microseconds.

`objdump` to see the disassembly
heaps of instructions here. differences between branch targets.
one op inside loop leads to a massive amount of work.

some interesting assembly instructions - simd ones, paddd; padded add of doubles. full xmm register (256bit) packed and added against another xmm register.
implicitly in that one op, does multiple integer adds.

movdqu into xmm0,1,2,3,4. then paddd.
unrolling into vector registers.

big ideas; use wider registers for pairwise vector additons and unroll
