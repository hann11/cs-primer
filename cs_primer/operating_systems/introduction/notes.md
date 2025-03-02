# What is the kernel?

Functionality accessed via syscall interface; privileged operation required to be in kernel mode
Imperfect definition; virtual memory part of the kernel, but don't need syscall for it

Whats not the kernel; shell

Stallman wrote GNU. "Linux" is GNU + Linux.

Linux is "just" the kernel.
GNU; free version of Unix; cstandard lib, c compiler, cmd line utilities, shell, text editor.

Kernel; allocates machine resources to other programs

eople released versions of Linux, used Linux kernel + a lot of GNU stuff.

Kernel; code loaded when machine is turned on and loaded into mem. Mem virt/process scheduling needs to be run. That then starts user processes (terminal etc)

Kernel another defn; what's behind syscall interface. Need to be protected. Not every program can access disk.

# Early history of Unix

C and Unix tightly coupled

PDP11; teletypewriter. write a line of program, send to machine, getline of output to stdout (spool of paper) - legacy we now see!

KT and DR working on Multics; make a timesharing OS. Multics didn't work out, too complex. Too expensive to run.

Bell labs pulled out, KT and DR had a taste of Multics and wanted to maek another time sharing OS but weren't allowed.

KT was writing a game -lunar lander. very expensive machine to run. Shouldnt play games on it
Ported it to a PDP, a cheaper machine that was unused.

Wrote intricate IO control code to get around hard disk stuff

Importing game to PDP7, "few weeks away from an OS"

3 weeks; 1 week to text editor, assembler, shell. Knocked it out,in addition to IO control code

DR wasn't working on Unix, but he was working on C. thought a good fit for Unix.

Unix was re-written in C. Projects were both hacked together.

C was simple, fast, straightforward to write compiler. Wanted cheap fast projects.

C was very fast to assembly, so Unix could keep progressing.

# Flavours / lineage of Unix
