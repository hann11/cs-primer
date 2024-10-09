Want to construct a DNS query according to RFC1035.

Plan:

Construct a query message.

    +---------------------+
    |        Header       |
    +---------------------+
    |       Question      | the question for the name server
    +---------------------+
    |        Answer       | RRs answering the question
    +---------------------+
    |      Authority      | RRs pointing toward an authority
    +---------------------+
    |      Additional     | RRs holding additional information
    +---------------------+

Here, just require the Header and Question.

Header:
16 bit ID
Flags (16 bit), we only need RD = 1 for recursive desired.

                                 1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

QR: 0 for question
Opcode: 0 for standard query
AA: Auth Answer, 0 for query
TC: Trunc 0
RD: Recursion Desired: TRue 1
RA: For answer only 0
Z: reserved 0
Rcode: response code. 0

So we then have the 16 bit sequence
0 0000 0 0 1 0 000 000

Which is equivalent to 0x0100 in hex.

QUESTION

                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                     QNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QTYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QCLASS                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

QNAME is the domain name, a sequence of labels, separate by the .
Each label has a length octet then has that number of octets (bytes). Domain name terminates with 0 length octet.

E.g. google.com

google -> ascii 6 bytes
com -> ascii 3 bytes
zero length byte

e.g.

qname = empty byte string
qname += len(google)
qname += google.encode ascii
qname += len(com)
qname += com.encode ascii

qname + 0x00

qtype: type of query, a valid TYPE field
3.2.2. TYPE values

TYPE fields are used in resource records. Note that these types are a
subset of QTYPEs.

TYPE value and meaning

A 1 a host address

NS 2 an authoritative name server

MD 3 a mail destination (Obsolete - use MX)

we use 1

qclass: the claass of query (IN) for internet).

3.2.4. CLASS values

CLASS fields appear in resource records. The following CLASS mnemonics
and values are defined:

IN 1 the Internet

CS 2 the CSNET class (Obsolete - used only for examples in
some obsolete RFCs)

CH 3 the CHAOS class

HS 4 Hesiod [Dyer 87]

we use 1

so construct the query.

## return an answer

on return from the dns server, we need to parse the answer.

DNS returns the Header, Question, Answer, maybe Auth and Add.

Parse out the Header, first 12 bytes.
Parse out the Question, depending on the length of the question.
Then, can get the Answer information.

answer is a Resource Record, same as Authority and Additional.

RR Format:

                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                                               /
    /                      NAME                     /
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     CLASS                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TTL                      |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                   RDLENGTH                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--|
    /                     RDATA                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

It appears the name is variable length, it will terminate with a null byte.

So get the length, and then struct unpack type, class, TTL, rdlength.

Get rdata from length parsing.

IP will just be byte separated information.
