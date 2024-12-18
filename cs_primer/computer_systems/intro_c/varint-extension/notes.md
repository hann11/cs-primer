using interpreted/dynamic easy language like python, as interface to some higher performance subsystems written in C/C++
write python to implement business logic/features, rely upon libraries like numpy for the heavy lifting, written in C.

some engs write python, others take it and make it faster.

in this problem; write c extension, implement python module, invoke in python.

interact b/w python and C.

work with large existing C codebase (python).

navigate and read cpython to solve this problem, in particular https://docs.python.org/3/extending/extending.html
expected interface of the interpreter

implement two c functions; encode and decode, can probably just re-write the python logic across

dont care about C syntax for this problem;

solved; now video notes:

## video notes

```
static PyObject *cvarint_encode(PyObject *self, PyObject *args) {
```

everything is a PyObject POINTER.

Cpython uses PyObject as a universal interface to things thatshow up alot, have reference count, type, etc.

we'll receive and return python objects

as this is a fn, self is the module itself, notpassing anything. args we will get the argument from (n).
Invoke with a python integer. It can grow as large as necessary. Need to pass into a C datatype.
protobuf goes up to uint64.

return pyobject is a bytes object; python interpreter constructs a bytes object, we'll do it in C.

Parsing the arguments; refer to the example docs
ParseTuple; need to pass a reference to moddify implace (&input)

want 64bit unsinged integer (K - unsigned long long)

args, "K", &n - pointer to the integer n.

Pyparse tuple will parse and give back the n.

return a bytes object. docs had PyLong_fFromLong - pytohn object int from a Clong.

can just return a character array. char out [10];

C implementation of varint, pretty simple extension just using the array pointer here rather than the list abstraction.

want to return pybytes; so search the docs somewhere for this.
check the cpython source code, find a function that does it, quite good
cpython/objects/bytesobject.c

Pybytes_fromstring needs a null terminator
Fromstringandsize doesnt need null! nice

looks like it does a memcpy - memory copy into loc
