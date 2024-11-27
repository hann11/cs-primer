using interpreted/dynamic easy language like python, as interface to some higher performance subsystems written in C/C++
write python to implement business logic/features, rely upon libraries like numpy for the heavy lifting, written in C.

some engs write python, others take it and make it faster.

in this problem; write c extension, implement python module, invoke in python.

interact b/w python and C.

work with large existing C codebase (python).

navigate and read cpython to solve this problem, in particular https://docs.python.org/3/extending/extending.html
expected interface of the interpreter

implement two c functions; encode and decode, can probably just re-write the python logic across
