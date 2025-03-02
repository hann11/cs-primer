# Understanding CPU Caches

CPU clock speeds have gone up A lot - up to 4GHz (4 billion operatons per second) - Moores' Law
RAM Latency hardly gone up.

Fit more transistors on a chip, get more clokc speed, up to an equilibrium. More transistors per unit distance.
Although now it's horizontally scaling cores.

2005-2010 plateu around 4GHz
Add two numbrs together; quarter of a nanosecond
1GHz; 1 operation per nanosecond

back n the 90s, around 100 nanosecond per operation.

Modern DRAM chip (Main memory - RAM) - 100 ns to retrieve 1byte latency.

In 1990, could retrieve 2 integers and add them together in same-ish speed to compute.

Compute gotten insanely fast compared. 500x faster Compute
RAM latency not improved as much.
if retrieving data and compuitng over, going to ram over and over would bottleneck a program.

## Example:

Problmem; add a bunch of integers together.

nums = [ ..]

```
total = 0
nums = [xxx]
for n in nums:
    total += n
return total
```

What's the disassembly look like?
Conditional branch in the loop: are we at the end of array? Incremement an index.
Got a `mov` instruction; data from register into ram. then an `add`.
`add` might be 25% of the time spent here.

1 branch to check if loop end, 1 inc, 1 mov, 1 add.

given a 4GHz machine. Hertz; time per second. Giga; billion
Add a 0.25ns operation.
Branch: 0.25ns with good branc prediction
Inc 0.25ns
Mov: 100ns without CPU caches.

What if, by looking at an integer, the CPU could get surrounding data and populate cache near the CPU with these?

Given 64 byte cache line. 4 byte integers. 16 integers per cache line.

Perf improvements would be bloody good. Reduce 16 100ns memory accesses.
Assume in C/Go, the numbers are laid out contiguously in memory.

Every cache miss, a cache line is pulled in to cache.
Cache lines are on the Chip (integrated circuit) - same piece of silicon as the registers and ALU.
Main memory - CPU cache. Faster lookup in CPU CAche.

given an L1 Cache latency of 4 cpu cycles (1 ns)

1 cache miss pulls in cache line; surrounding 64 bytes

Assume RAM is ordered in 64 byte chunks, 0 - 63, 64-127. Whatever byte the addressable object cache line belongs to, it'll pull in that cache line from memory to L1.

15 hits per miss. Cost of looking up 16 integers is 100 ns for the cache miss, 15 ns for the other 15 cache hits.

Mov becomes avg 7 ns. (100+15)/16

Big IDea; Likely that data surrounding what you've accessed will be accessed again.

Common access patterns like sequential iteration, it works a lot. Good cache utilisation.

Can't control what gets pulled in. No API to it. Happens automatically. CPU does it. Not the OS.

## Implicatons:

What if numbers are 16 bit integers and not 32 bit integers. Does perfomrance improve? YES!
rather than 16 ints per cache line, get 32 2 byte shorts per cache line.

Space IS time here.

If something fits in cache better, takes less time.

Register
CPU Cache
DRAM (main mem)
Disk
Network

Space is time. Extends all teh way through.

NEural net; 4bit floats. FASTER.

## IMplication 2

Struct

```
User {
    age
    name
    address
    ...
}
```

THink of dataclasses/Databases that accumulate this stuff over time.

Lot of fields in Struct. Imagine you have array of structs. C/Go/Rust - nicely packed structs. Laid out sequentially for constant time lookups on Users[5].age

Imagine a scenario with a large array of users and you only care about the age.
What goes into the cache line?
Every time a cache miss and pull in User struct, you'll iterate, new cache line new user.

Ages together; a lot faster.

Data not laid out in the optimal way.

Array of Structs vs Struct of Arrays.

People consider users as the entity. Iterate through the users.

Can invert thinking into one Struct

```
UserData {
    ages
    names
    addresses
    ...
}
```

In this setup, if doing avg age, user with name, get better cache utilisation as iterating and filling cache lines with useful info.

For agg style operation, this makes sense.
One user at a time, not so much cache utilistaion required.

Databases; Column Store - When doing analytics, look at one/many fields. DB should store columnar.
When go to disk and retrieve a block from disk, populate a lot of ages together.
Better IO utilisation.

### Pointer Chasing

Consider a user Object

```
class User:
    x
    y
    z
    address: Address: POINTER

class Address:
    payment: POINTER
```

Object to object to object.

Relational DB: Relations. Model table as object; pointer to pointer to pointer.

Everytime dereference a pointer; new location in memory.
NOT in a cache line likely.

If you do the sum thing in Python, the list type and Array type in Ruby; interpreted languages to accomodate dynamic types
Instantiate list, append whatever.

l = [1, ... ]
1 is an object in Python that points to other integers.

Same with dicts. It's nice to be able to do that.

How does implementation work? l[2] - constant lookup.

How can you have constant lookup with variable length elements?

Basic idea; under the hood, this list is a C array of pyobject pointers.
All are 64bit (8 bytes)

Interpreter follows pointer to PyObject, look up the dtype.

Consider now array of pointers to py numbers.
[p1,p2,p3]

Whats on a cache line? 8 py number pointers.
1 cache miss; 7 free py number pointers.
Fast to find value. But we don't want the pointer.
How do you get the integer? Follow into a memory location, likely not on the cache line.

Each number lookup can be a cache miss.

Python has an optimisation that will preconstruct small numbers fro you up to a threshold in size; so you don't keep construct, deconstruct, deallocate small numbers.

Python isnt slow because of interpreter although adds overehead.

Data structures are heterogenous so use pointers as unifrom interface to diff types, get pointer chasing, cache gets mauled.
Numpy uses C. Need to give a type.
Sequentially allocated.

Cache utilisation can really speed up different algorithms too.
Hashmap implementations; two ways to do conflict resolution. ONe way is to use chaining, if a collision, follow a linked list.
Open addressing; collission, put it nearby. Open addressing allows collision to use better cache utilisation.

Naively used linked list; val and pointer to another node. If data layed out as such, pointer chasing is a cache miss. Most popular in the 1990s before speed of CPU.

Contiguous array a lot faster for speed.

There is a hierarchy of CPU Caches. L1 top layer.
Trade-off capacity for latency

# Cache Hierarchy

Consider 1 cpu cycle is 0.25 ns

L1 cache split into Data and instruction
Data; values accessed from RAM
Instruction; specifically for running instructions. Cache instructions of the program as frequently branch/recently re-do instructions

l1 Cache (Skylake i7-6700)
32 KB = 512 cache lines on a 64 byte line machine
Latency to Data; 4 cycles (1ns) to access

Note; ALU needs to read to and from registers all within 0.25ns.

L1 cache "same substance" as CPU, implemented as SRAM, just a bit further away and more complex lookup

L2 Cache: 256KB, 12 cycles (3ns)
A bit slower, a bit further away, but can store more and take up more space.

L1/L2 are dedicated per CPU core.

Given a 2 CPU core machine, both have ALU, all on the one integrated circuit (system on chip)
both have L1 and L2 and the L3 is shared in this particular architecture.

L3 is much bigger; 8MB.
8MB; 2 million 4 byte integers.
It's onboard/ondie/onCPU memory. 42 cycles

RAM Latency; 42 cycles + 51 ns.

Consider a multi-threaded application, threads in the same address space. Can utilise same Cache L3.

Imagine selling furniture. Consider the SF Bay Area.
It'd be nice to have a showroom on valencia st - right in fanceist part of town where people buy expensive furniture
Must be small bc realestate is expensive.

Maybe create a warehouse in Oakland across the Bay.

Color of sofa not in shworoom, can get from warehouse, takes a day.

Warehouse huge bc cheaper realestate.

Warehouse still somewhat expensive.

Creaet a much larger centre further out. 3 days to get to Oakland warehouse / 4 days to SF showroom.

No one perfect place to tradeoff latency/cost/size.

L1 is prime realestate on the chip.

Takes not only time to get sofa to SF. Warehouse takes longer to lookup as its bigger than showroom, as gets bigger harder to search.

Consider how many cache lines into L1, is it shared with CPU cores, etc.
More compact data, more to fit closer in, better it is.

A cache miss results in ALL levels being populated.

If miss L1, L2, L3
wherever the hit will populate everything on the way back.
