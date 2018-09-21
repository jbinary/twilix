TwiLiX
=======

TwiLiX is a XMPP library on top of twisted.words. It utilizes an idea of ORM approach
to build and parse XML stanzas.

Changelog
----------
master — allow successors of the Component class to define which dispatcher
class to use

0.1.4 — make it possible to send keepalive packets to the stream to make sure
the connection is not being interrupted by any kind of timeout

0.1.3 — stanzas with parentClass are now looked in all the possible children
elements of the parent element
