# explainers

## what does it mean for a value to be a certain number of bits?

https://csprimer.com/watch/fixed-width/

fixed-width (16bit integer, 32bit floats)

consider 4bit integers, \_ \_ \_ \_ (0 or 1), only positive integers.

you can have 2^4 combinations, 1 1 1 1 is 15, 0 0 0 0 is 0.
add 1 to 15, you get overflow, can't store it. will become 0 mostly as only space for 4bits

at 4bill transactions postgres breaks, 2^32 is around 4bill

runescape: 2^32 / 2 = 2147M max cash, signed integers (both pos and neg)

bit shift in code languages:
`1 << 65`: shift 1 65 bits, causes overflow in node

`1 << 1` is 2, `1 << 2` is 4, 8, 16 etc.

python stores integer in parts, combines many single machine additions together, so won't overflow easily, can handle massive numbers, if take it crazy get `MemoryError`.

## big and little endian (byte ordering)

https://csprimer.com/watch/byte-ordering/

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

https://csprimer.com/watch/bit-shifting/
1 << 3
0 0 0 1 (1)
1 0 0 0 (8)

6 << 1
0 1 1 0 (6)
1 1 0 0 (12)

shifting right is a floor division by 2
32 bit becomes 16, 16 8 etc.

## byte operations faster than integer arithmetic

https://csprimer.com/watch/bitwise-efficiency/

- is integer addition on binary
  | is bitwise or can achieve something similar

shift by n bits faster than multiplying by 2^n?

look at the intel coffee lake docs: latency is cpu cycles
reciprocal throughput; independent instructions done together
0.25 throughput, if can do 4 at once, 0.25 each

shifting had more throughput than multiplication

comparing cpu cycles/throughput for arithmetic vs. bit shifting

## what is a byte

https://csprimer.com/watch/what-is-a-byte/
unit of addressable memory
what you get back from an address in ram gives 1 byte

8 bits is an octet (sequence of 8bits)

## why are bytes 0-255?

https://csprimer.com/watch/byte-range/
1byte fits 256 possibilities (0-255)
8 bits for 0 or 1
2^8 = 256

binary 1 1 0
1 _ 2^2 + 1 _ 2^1 + 1 \* 2^0

## stdin, stdout (unix)

https://csprimer.com/watch/stdio/
simplify reading from input and sending to output
interact with program in unix shell

## what are file descriptors 0, 1, 2?

https://csprimer.com/watch/stdin-fds/

0: stdin
1: stdout
2: stderr

curl example.com: returns html to stdout
curl -v example.com: verbose, shows headers, goes to stderr

curl -v example.com 2> /dev/null: send stderr to null
curl -v example.com > /dev/null: send stdout to null ONLY. stderr still goes to terminal

## why does one byte correspond to 2 hex digits?

https://csprimer.com/watch/hex-byte/

hexadecimal is base 16, 0-9, a-f
2^8 = 256, 16^2 = 256

## what is a file descriptor?

https://csprimer.com/watch/fds/

usually just an integer that indicates to the operating system what file you want to interact with

## unicode vs utf8

https://csprimer.com/watch/unicode-v-utf8/

unicode is a standard, utf8 is a way to encode unicode characters into bits (and hence bytes)

## what is hexadecmial?

https://csprimer.com/watch/what-is-hexadecimal/
its a base 16 number system, 0-9, a-f
its not really good for storing data, but good for representing bytes for humans

## signed and unsigned integers

https://csprimer.com/watch/signed-integers/

basically, allow for negative numbers, unsigned don't

## remembering powers of two

https://csprimer.com/watch/powers-of-two/

memorise up to 2^10, then can calculate the rest
2^10 = 1024 ~= 1000

2^16 = 2^10 \* 2^6 =~ 1000 \* 64 = 65536

## bitwise operations (and, or, xor, not)

https://csprimer.com/watch/bitwise-ops/

AND (&)

1 0 1 1
0 1 1 0

if both bits are 1, then 1, else 0

0 0 1 0

good use for a bitmask. if want the lowest order 3 bits, you'd and with 0b111
1 0 1 1
0 1 1 1 (mask 0b111)

0 0 1 1

OR (|)
if either bit is 1, then 1, else 0

1 1 0 1
0 1 1 0
1 1 1 1

useful for setting bits, if want to set the 3rd bit, or with 0b100, always turn on

0 0 1 1 0 1 0
if you want the msb on
1 0 0 0 0 0 0

1 0 1 1 0 1 0

bits to represent permissions, e.g. user and admin

user can
0 0 1 0 1 1

admin can
1 0 0 0 0 1

user | admin
1 0 1 0 1 1

XOR (^)

if bits are different, then 1, else 0

1 0 1 1
0 1 1 0

1 1 0 1

when its useful: if doing encryption, you have plaintext to encrypt in bits

and you have a key

1 0 1 1 0 1 1 0 is the data

1 1 0 0 1 1 0 1 is the key

take xor

0 1 1 1 1 0 1 1 is the ciphertext

if you have the key, you can decrypt the ciphertext

0 1 1 1 1 0 1 1
1 1 0 0 1 1 0 1

1 0 1 1 0 1 1 0

NOT (~) - unary operator
flip the bits

0 1 1 0
1 0 0 1

permission bits vs. what you cant do

## why masking low order bits is like modulos of 2^n

https://csprimer.com/watch/haziq-mod/

## why do I sometimes see the sequence "\r\n" for a newline?

https://csprimer.com/watch/crlf/

ascii 10 is newline, 13 is carriage return

typewrites have a carriage, carriage return moves the carriage to the left, newline moves the paper up

when you press return, you want to move the carriage to the left and move the paper up

we don't noramlly need to overwrite the line, so we just move the paper up by \n

we don't need line feed by itself as we don't have a carriage to move back

unix has carraige return implicit in newline

best not to split on \n as you might miss \r\n and get trailing \r

http server mandates \r\n but be tolerant of \n

## how to read a hexdump

https://csprimer.com/watch/reading-hexdump/

hexdump -C file

it shows the bytes in hex, then the ascii representation

## whats the point of floating point?

https://csprimer.com/watch/floats/

essentially trade off precision for a wider range

it's good for scientific computing, where you have a wide range of numbers

but for currency, you want precision, so use integers

## why do we care about teletype machines?

https://csprimer.com/watch/teletype-machines/

unix created around the time of teletype, its a legacy thing

unix wanted compatibility between machines between unix

terminal emulates teletype

## what does it mean to flush a buffer?

https://csprimer.com/watch/flush-buffer/

buffer is like a queue of bytes

flush: take off the bytes in the buffer and send them to the output

touch /tmp/flush
tail -f /tmp/flush

tail will wait for the file to change, so you can write to the file and see it in the terminal

f.write("hello\n") returns a file descriptor, so you can write to it
however it doesn't write to the file, it writes to the buffer

f.flush() writes the buffer to the file

flushing is an expensive operation, so you don't want to do it too often, thats why its good to have a buffer

## utf8, utf16, utf32

https://csprimer.com/watch/utf8-utf16-utf32/

utf8 is variable width, 1-4 bytes

utf16 is 2 or 4 bytes

utf32 is 4 bytes

## how does utf8 encode characters?

https://csprimer.com/watch/utf8/

1byte ascii is 1byte utf8

it should also be able to encode unicode characters

utf8 is variable width, 1-4 bytes

grapheme cluster: a single character, can be multiple code points

ascii character: start with leading 0 (127 possible characters), leading bit is zero

a with accent: 2 bytes 110xxxxx 10xxxxxx

3 bytes 1110xxxx 10xxxxxx 10xxxxxx

4 bytes 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx

## how is ieee754 floating point encoded?

https://csprimer.com/watch/ieee754-encoding/

sign bit, exponent, mantissa

sign bit: 0 is positive, 1 is negative

exponent: 8 bits, 127 bias, 0 is -126, 255 is 127

mantissa: ?

9.75: 1001.11

2^3 + 2^0 + 2^-1 + 2^-2 (2^-1 is 0.5, 2^-2 is 0.25)

1.00111 \* 2^3

exp: 3 + 127 = 130 = 10000010

mantissa: 00111

sign: 0

float: 0 10000010 00111000000000000000000 in 32 bits

nan is all 1s in exponent, mantiassa is not all 0s

0.1 + 0.2 != 0.3 in floating point because of rounding errors, explicitly we can't represent 0.1 in binary and 0.2 in binary so we get a rounding error in the sum
