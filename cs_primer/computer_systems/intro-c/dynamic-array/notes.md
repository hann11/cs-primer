# dynamic array

implement equiv of python list; grow as needed, constant time indexing, items of any type. storage must grow.

C array;
int arr[3];
each int 4 bytes long - 12 bytes

5,7,42
arr[2]: constant time lookup, needs to issue a mov instruction that references that locaton
how to figure that location?
knows, start of arr + index x size of the type.
can be done in a single instruction.

its a result of the size being fixed.

how to have fixed size constant time indexing allocation? use the word reference (hint).

data must reside somewhere, of a fixed size. cant allocate too many arrays unnecessarily

ideally use some amount of space, storage will need to grow if we push.

use an underlying c array
make adjustment to it in order to accomodate everything
step 1; just support integers.

struct da will have underlying c array and some other stuff too.

video notes
C doesnt have classes.
C++ has classes (C with classes)

structs arent that far off classes, holding state.

need to understand: void pointer, structs, malloc.

thinking: struct should have a length (number of items in the array) and an array of length length, that has void ** in it -> void \* is a pointer to anything, I guess void ** is an "anything" too. ora pointer to a pointer.

struct DA {
void\*\* items;
int length;
int capacity;
}

int capacity will be starting capacity.

```
DA* DA_new (void) {
    DA* da = malloc(sizeof(DA));
    da->items = malloc(STARTING_CAPACITY * sizeof(void*));
    da->length = 0
    da->capacity = STARTING_CAPACITY
}

int DA_size(DA *da) {
    return da->length
}

void DA_free (DA *da) {
    free(da->items)
    free(da)
}
```

the struct is pretty straightforward, has capacity, length, items.
DA_new, need to malloc for the sizeof a DA. this will just hold Pointer info, and 2 ints. Won't need another of these.
da->items however, need a constant re-alloc; malloc how much capacity we want.

length 0 to start.
capacity the starting capacity.

DA_size, easy just return the length.

DA_free, need to free the items malloc and the da malloc.

DA_push; takes an argument which is a void pointer - can be anything
add to items at the length so DA.items[length] = \*x
add to length, length += 1
do a capacity check too. if length == capacity, add more memory.how? get a new DA? idk.

DA_pop;
return &DA.items[length]
doens't reutrn anything; soo just drop the length.
if length == 0 say can;'t pop.

DA_set;
try DA.items[i] = \*x

DA_get;
return &DA.items[i]

the above somehow worked with some tweaks like datatype returns and pointer dereferences. it's not super complex;

## video notes

part1; DA_new, DA_size, struct typedef

C doesn't have classes and objects; DA class might make more sense, but can stil get something similar in C.
Struct with fields and values for state. Functions (methods) take in a reference to a DA...
whats the diff between a classdef? inheritance, but its really similar.

struct will have items. they can be ANYTHING. its an underlying C array. we don't know length at compile time so dont do items[20];.

we need a pointer.... but we dont know the type...

void** ; pointer to ANYTHING. pointer to a starting location of a sequence of pointers to anything.
void pointer type, void**. pointer to the starting location of a sequence of pointers to anything

it's hwo we get cst time indexing. void pointer is 8bytes as of now, fixed size. can go to the nth thing / ith thing in constant time.

hwo to know the type when we get there? might end up with a python objct type. every object has a type field.

DA_size is easy, just return the lenght. because da is a pointer, can use the arrow syntax `da->length`.

DA_new; allocate a DA. it's going to be a malloc, which gives you a memory address, and hence a pointer.

`DA\* da = malloc(sizeof(DA)))`;
malloc gives int, int, 8byte void pointer.4 +4 + 8 = 16 bytes

but we want space for the items themselves; not just the reference void\*\* items, but the items themselves

`da->items = malloc(STARTING_CAPACITY _ sizeof(void_))`;

malloc api is number of bytes to allocate. returns void ptr.

DA_free is simple; free up the da->items and free up da. it will keep the same bytes there but the memory could be allocated elsewhere.

push,pop, set and get:

push; da->items[da->length] = x; makes sense
da->length++;
push receives an address (void\* x). cant do with values, values are a copy!
void pointer otherwise need functions for every type.

pop; returns from da->items[da->length-1], or just pre-decrement
da->items[--da->length] - decrements.

note in C you can index below 0 or above capacity; it will give whatever happens to be there in memory, crazy.

NULL in C is a null pointer,not a valid address (address 0)

set: like push, indewx into items. will be at given i.

get: return it.. and check i is valid and bounded.

RESIZING
when need to grow it, what do we do?

- could grow by 1. what if there is stuff beyond where the array is allocated? will clobber it.
- need to copy n items in array proportional to n time to copy the items. if pay the cost of copying n thing, should be able to do alot of pushes.
  n copys, then can do n pushes for free.

in a realtime system, probably dont care about average case, moreso the worst case.

justification to grow the array 2x.

c standard lib function: realloc; attempts to change size at allocated pointer inlpace. if not room, copys if necessary to a new spot. cst time to grow inplace.

pythons list: listobject.h
PyObject \*\*ob_item; undelying C array of PyObject pointers. when dereferenced, theres a reference count and object type etc.

size / len comes from ob_size.
allocated; amt of capacity / allocated space
similar to what we defined

py list resize; takes ref to PyListObject and newsize intended.
rather than just doubling, it has a nice growth pattern using some bit fiddling. doubles early then grows by 12ish.
attempts to deal with a poorly performing realloc

oz capacity add; only matters for a push. check if the length has reached capacity.

da->capacity <<= 1; same as 2x
