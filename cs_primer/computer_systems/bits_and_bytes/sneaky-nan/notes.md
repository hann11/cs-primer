ieee754 can encode many different nans.

if the exp is all 1's, and the mantissa is not all 0's, then it is a nan.

so we can encode a hidden message in the mantissa.

single precision float is 32bits, which is not enough.

64bit has a 52bit fraction, allowing 6bytes message. (6\*48)
other 4bits we will set at least one bit to 1, to deal with infinities.
other 3 bits we will encode the length of the message (in bytes)
let's do a utf8 encoding.

sign = 0
exp = 11 1's
