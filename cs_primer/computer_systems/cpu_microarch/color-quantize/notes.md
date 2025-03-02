top so question;
why processing sorted array faster than unsorted?
leaking of the microarch?

can be to do with branch prediction
given size of pipelines on CPU, substantal penalty for branch mis-prediction

try to write branchless code where you can, if the compiler cant find a branchless approach / where branch predictor not setup for success.

problem:
given a bitmap file, outputs an 8bit quantized version
bmp; each pixel encoded uses 24bits, 8bits for rgb channels

8bit; 3-3-2 bit RGB channels. get 256 possible colours
3r,3g,2b.

program outputs 8bit version of bmp

given in the files; 2 bmp files to play with.

core work in quantize.c won't need to change other files to do teh exercise

fix the quantize function. super branchy

given r,g,b byte values (3 bytes separately) return 1 byte value

convert.c will invoke quantize on the color channel bytes

Google Benchmark doesn't seem to work locally for me, so can run
`make convert`
`./convert filepath outpath`

timer
`time ./convert teapots.bmp teapots_out.bmp`

think about how you're actually making improvements, how to extend it etc.

consider branch misprediction on sprinkles.bmp

pen and paper, figured all it requires is bit shifting

blue: < 0x40 goes to 0, < 0x80 goes to 1

can shift to the right by 6 bits to get that

red: < 0x20 to 0, <0x40 to 0x20. requires dropping all bits but the top one
alternatively, we want to get back 2 \* 16 of how many bits past 5 are on
so shr 5 and shl 5

green: 0x20 to 0, 0x40 to 4, 0x60 to 8
shr 5, then shl 2

just some bit manipulation, takes a bit to get head around, but removes all branch conditions / flow control

## video notes

first look at disaseembly, compiler will try find sequential instructions where it can.
tries to avoid branching.

`objdump -S quantize`
heaps of cmp and jmp. problem constructed as such. branch heavy.

modern branch predictors are good. a predictable pattern will work
intel doesnt publish details on branch predictors
revese eng to figure it

generally if you can predict it, branch can.

if same branch repeatedly taken, should figure it.

oz benchmark: synthetic bench: runs quantize with random bytes

cant use prior results to hlp; 10% branch miss rate.

loop termination; branch predictor is good at.

number close to 10% is an opportunity for improvement.

sprinkles; worked hard to find where colours change frequently. branch predictor worse than where colors uniform.

simple BP; take previous computed outcome. same color, will do well. frequent changes, poorer.

perf on teapot:
1.53% branch misses
high branching code, but blocks of consistent color allows branch predictor to be nice.

perf on sprinkles:
9.77% misses!

benhcmark a bit contrived, but good to improve the code regardless.

took oz 10h to find a problem.. branch predictors are just so good.
bp's are good, compilers are good. good to understand the microarch regardless.

does some similar bit maniulation stuff, but uses bitmask rather than shifts on red and green.

now running through perf:
benhcmark: 9.58% and 90ms to 12ms.
if a branch mispredict costs 15-20 cycles, get rate of mispredicting to get 6x improvement (napkin math)
0.08% branch.

sprinkles:
0.83% branches. fkn good. (trivially small)

What if we couldn't just split easily on the bitshifts?
Non-uniform bucket sizes.

if you had a full 256 lookup table;
mapping to random buckets.
can replace branch with a lookup, deterministic.
better than branch/misprediction?
depends on the branch misprediction rate

if the lookup fits in cpu cache, can do in 5 cpu cyclers in a modern macine
barnch mispredict; 15-20 cycles

Modern branch predictors good. Sometimes microarch leaks in a problem like this.
Random info in an unsorted array, very hard to predict branch.
Faster to process a sorted array.

Compiler may replace branch with a branchless form (gotcha) in disassembly
