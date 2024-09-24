Protobuf encoding: https://protobuf.dev/programming-guides/encoding/#varints

very little encoded in text; mostly bytes and other encodings, binary encodings.

protocol encoding; variable width. here we deal with variable width integers

note (realisation): given variable width, we need a way to know when the integer ends, using most significant bits (1 or 0), we store 7 bits at a time.

wire format; encoding of bytes transmitted across a network, even avro, can encode schemas, encode/decode fast. json not designed for this.

fixed width doesnt make sense for small numbers, variables a bit nicer

the files `.uint64` are unsigned 64bit big endian integers. think in hex (0-9, a-f)

2 hex digits is one byte
one byte: 2^8 = 256
hex (base 16) = 16^2 = 256

to do:
encode integers into protobuf base 128 varints

### files

note, can't read the files as they are not text-encoded. they are bytes! read as a hexdump.

### hex

9 6 = 9\*16 + 6 = 150 (arithemtic hex)
9 = 1 0 0 1
6 = 0 1 1 0
9 6 = 1 0 0 1 0 1 1 0
