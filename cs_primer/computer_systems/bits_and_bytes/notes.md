# explainers

## certain number of bits

fixed-width (16bit integer, 32bit floats)

consider 4bit integers, \_ \_ \_ \_ (0 or 1), only positive integers.

you can have 2^4 combinations, 1 1 1 1 is 15, 0 0 0 0 is 0.
add 1 to 15, you get overflow, can't store it. will become 0 mostly as only space for 4bits

at 4bill transactions postgres breaks, 2^32 is around 4bill

rs: 2^32 / 2 = 2147M max cash, signed integers (both pos and neg)

bit shift in code languages:
`1 << 65`: shift 1 65 bits, causes overflow in node

`1 << 1` is 2, `1 << 2` is 4, 8, 16 etc.

python stores integer in parts, combines many single machine additions together, so won't overflow easily, can handle massive numbers, if take it crazy get `MemoryError`.

## big and little endian (byte ordering)

123 is one hundred and twenty three (higher placed value on the left)

how to hold bytes in multi-byte value?
tcp port; value in 0 to 2^16, 65536

can consider left as high or right as high

big endian; 123
little endian; 123 is three hundred and twenty one

little endian; low order on the left.

intel machines are little endian
amd machine is big endian

## shifting bits

1 << 3
0 0 0 1 (1)
1 0 0 0 (8)

6 << 1
0 1 1 0 (6)
1 1 0 0 (12)

shifting right is a floor division by 2
32 bit becomes 16, 16 8 etc.
