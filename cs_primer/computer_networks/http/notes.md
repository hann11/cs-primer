## proxies, gateways, and tunnels

https://www.rfc-editor.org/rfc/rfc9110.html

A "proxy" is a message-forwarding agent that is chosen by the client, usually via local configuration rules, to receive requests for some type(s) of absolute URI and attempt to satisfy those requests via translation through the HTTP interface. Some translations are minimal, such as for proxy requests for "http" URIs, whereas other requests might require translation to and from entirely different application-level protocols. Proxies are often used to group an organization's HTTP requests through a common intermediary for the sake of security services, annotation services, or shared caching. Some proxies are designed to apply transformations to selected messages or content while they are being forwarded, as described in Section 7.7.

A "gateway" (a.k.a. "reverse proxy") is an intermediary that acts as an origin server for the outbound connection but translates received requests and forwards them inbound to another server or servers. Gateways are often used to encapsulate legacy or untrusted information services, to improve server performance through "accelerator" caching, and to enable partitioning or load balancing of HTTP services across multiple machines.

All HTTP requirements applicable to an origin server also apply to the outbound communication of a gateway. A gateway communicates with inbound servers using any protocol that it desires, including private extensions to HTTP that are outside the scope of this specification. However, an HTTP-to-HTTP gateway that wishes to interoperate with third-party HTTP servers needs to conform to user agent requirements on the gateway's inbound connection.

A "tunnel" acts as a blind relay between two connections without changing the messages. Once active, a tunnel is not considered a party to the HTTP communication, though the tunnel might have been initiated by an HTTP request. A tunnel ceases to exist when both ends of the relayed connection are closed. Tunnels are used to extend a virtual connection through an intermediary, such as when Transport Layer Security (TLS, [TLS13]) is used to establish confidential communication through a shared firewall proxy.

The above categories for intermediary only consider those acting as participants in the HTTP communication. There are also intermediaries that can act on lower layers of the network protocol stack, filtering or redirecting HTTP traffic without the knowledge or permission of message senders. Network intermediaries are indistinguishable (at a protocol level) from an on-path attacker, often introducing security flaws or interoperability problems due to mistakenly violating HTTP semantics.

## http persistent connections

rather than close the connection after each request, after tcp connection is established, the client can send multiple requests on the same connection. the server can respond to each request in turn. this is called a persistent connection. the server can also close the connection after a certain amount of time has passed, or after a certain number of requests have been made.
better than syn ack syn ack over and over again.
http header: Connection: keep-alive, according to the spec for http/1.1, the default is to keep the connection alive.

## http and browser history

tim berners lee had the idea at cern to have linked pages to academic like papers, browsers could navigate and surface this context, marc andreesen and a few others proposed ways to do things like surface images according to protocol everyone can agree on.

## http headers to answer own questions

run netcat to example.com port 80:

```
nc example.com 80

GET / HTTP/1.1
```

returns a 400 bad request. this is because the server is expecting a host header. the host header is required for http/1.1. the host header is the domain name of the server. the server uses this to determine which virtual host to serve the request from. the host header is not required for http/1.0. the host header is not required for http/2.0.

```
nc example.com 80

GET / HTTP/1.1
Host: example.com
```

returns the html of the example.com homepage.

```
HTTP/1.1 200 OK
Accept-Ranges: bytes
Age: 51371
Cache-Control: max-age=604800
Content-Type: text/html; charset=UTF-8
Date: Fri, 04 Oct 2024 09:00:08 GMT
Etag: "3147526947"
Expires: Fri, 11 Oct 2024 09:00:08 GMT
Last-Modified: Thu, 17 Oct 2019 07:18:26 GMT
Server: ECAcc (lac/55C4)
Vary: Accept-Encoding
X-Cache: HIT
Content-Length: 1256

<!doctype html>
<html>
<head>
```

the connection is closed after the response is sent. the server can also send a keep alive header to keep the connection open.

```
nc example.com 80

GET / HTTP/1.1
Host: example.com
Connection: keep-alive
```

one can open a server on port 80, and send requests from the browser to the server. the server can then print the headers of the request. this is useful for understanding how the browser works.

```
nc -l 80
```

open chrome and go to localhost:80. the server will print the headers of the request.

we receive:

```
GET / HTTP/1.1
Host: localhost
Connection: keep-alive
Cache-Control: max-age=0
sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
```

now, we can respond according to the http spec, and send random headers
one can also send the content length header which is the length of the body of the response. the browser will wait for the response to be the length of the content length header before rendering the page.

```
HTTP/1.1 200 OK
tag: "3147526947"
tag2: "3147526947"
Content-Length: 10

hello world HELLO
```

as the content length is 10, the browser will wait for 10 bytes before rendering the page. if the content length is 0, the browser will render the page immediately.

in browser it shows:
`hello worl` (10 bytes, or 10 ascii characters)

note the netcat connection terminated.. even though we received a keep alive.

COOKIES: a server can send back a set-cookie header to set a cookie on the client, which the client will send back on subsequent calls, stored in the browser cookies

For example:

```
nc -l 80
```

receive from browser:

```
GET / HTTP/1.1
Host: localhost
Connection: keep-alive
Cache-Control: max-age=0
sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
```

respond with:

```
HTTP/1.1 200 OK
tag: "3147526947"
tag2: "3147526947"
Content-Length: 10
Set-Cookie: name=hello

hello world HELLO
```

the browser will store the cookie and send it back on subsequent requests.

browser sends:

```
GET / HTTP/1.1
Host: localhost:8492
Connection: keep-alive
Cache-Control: max-age=0
sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Cookie: name=hello
```

sending utf8 stuff:

```
HTTP/1.1 200 OK
tag: "3147526947"
tag2: "3147526947"
Content-Length: 10
Content-Type: text/html; charset=utf-8

😍
```

appears in the browser. instead if we don't send the content type header, the browser will render the utf8 as ascii.

```
HTTP/1.1 200 OK
tag: "3147526947"
tag2: "3147526947"

😍
```

renders the emoji as ðŸ˜upon ctrl-c, note the browser kept waiting because no content length was sent.
