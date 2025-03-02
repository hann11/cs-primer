Oz developing in MacOS, execute in VM running Ubuntu 22
Shouldn't get many diffs as both are Unix like

Ubuntu; Linux GNU
Macos: BSD Unix

Running VM on 2 CPU cores. Can setup an EC2 running Ubuntu.

Runs; float muls. Measures real time, user time, sys time (kernel)
user space math for float
malloc has a bit more sys time. can expand malloc abit more.
sleeping; neither user or kernel

find PID as first goal. CPU core stretch goal. Think of process as running instance of a program.

& - run together
&& - run first left hand then once completed run right hand side

try run multiple more then CPU cores and check parallelism

Oz goals;

- research needed syscalls / library functions
- print process ID for running process
- determine elapsed real time (wall clock)
- determine elapsed time on CPU (user and system)
- refactor, cpuid

You can search online for stuff. But want a reliable answer. History of these OS is you might get a false positive between different OS.

Read man pages

Research 2-4 and figure what to do.

Know that ps can get process ID; how does it do it?
can use a tool like apropos pid, searching man pages

Diff ways to deal with man pages. 1 or 2 (maybe more)?

man time; gives you execution an times a utility. writes to stderr
man 2 time; doesnt work on macos? why?

getpid is a syscall ?
man 2 is syscalls.

linux man pages; sec1; user commands
sec2; syscalls

how to get time? check sections 2 3 in apropos.

macos in bsd has worse apropos. cant filter by sections.

linux/ubuntu, lot of diff time stuff.
