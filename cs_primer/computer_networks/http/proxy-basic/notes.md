Interestingly, when you host an index.html page and it has "links" to other parts of content, the browser makes multiple HTTP request to get that content.

I made the mistake of only allowing one connection then the program exited, not allowing more HTTP request. Although this would be solved with persistent connections.
