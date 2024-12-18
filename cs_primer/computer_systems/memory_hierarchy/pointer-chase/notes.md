pointer chasing is detrimental for cache utilisation

Optimise the speed. Not a matter of line profiling/cache misses. Hard to do that in Python, because performance overhead is from the VM itself.

Big Idea; Pointer Chasing is detrimental to cache utilisation.

can we get better cache utilisation than not pointer chasing?

```
class User:
    adress: Address -> Pointer to PyObject address
    payments: Payment -> Pointer to Payment

class Payment:
    amount: DollarAmount -> Pointer to PyObject dollaramount
```

User -> Payment -> Dollar amount; chasing pointers.

Baseline:
Data Loading: 2.777s
Computation: 1.605s

Tried collapsing address into the User object with address_line and zip_code, but no benefit - data loading still similar.

Average_age computation takes 0.004s, the rest is 1.6s. Attempt to reduce that.

Next: Collapse DollarAmount into Payment object

Data Loading drops to 2.045s and Computation to 1.1s

Next try collapsing payments to the User
User:
payments: list[Payment]

What about list[list[int, int, time]]

Data load: 1.64
Computation: 0.92

Next, consider struct of arrays, rather than array of structs.

class Users:
list user_id
list list payments etc.

Data: 1.5
Comp: 0.6

convert User to id, age, payments

Data Loading: 1.271
Comp: 1.1

Drop float conversion in stddev and average,, do in loading
Data: 1.36
Comp: 0.769

Turn payment into list of one float not 2
Comp 0.526

Turn payment into just a float, no list
Data 1.042
0.157s

Drop mean from stddev calc
0.122

Diudnt see this as point of the exercise, but can drop relational model altogether:

Just need list of ages, and list of payments. Dont care who did it, for our analytics.

Data: 0.724
Comp: 0.058

Yu can go alot faster, but didnt think was the point. Just iterate through csv rows once and do aggs in there.

tuple; pyobjects; dereference in there too.

Need to understand a bit more how Python fully works, but this is good to start peeling back. Tons of tuples, pointers, etc.

Trying numpy:
0.002s

Oz further notes:

Assertons pass and get order of magnitude imporvement, rather than having ds that ref objects
that ref objects that ref ds
avoid references, get as much as possible to the values to compute over.

Python array; can pack objects with values instead of PyObjects

Can try shorts instead of ints aswell to majorly utilise cache line

Takeaway; think of access patterns. If iterating over like data, should be stored together.
OOP not good for this.
