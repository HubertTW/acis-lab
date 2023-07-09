# One-way hash chain
One-way hash chain can be used a lightweight authentication protocol.
For example, one can generate h0, h1, ..., hn that satisfy hi = H(hi − 1),
where H is a one-way function. The user can announce hn in the first
transmission and hn−1 in the next transmission and so on. Others can be
sure that all transmissions belong to the same transaction by checking if
hi = H(hi−1). The reason is that only the hi−1 holder can generate hi
. This
authentication is lightweight because it only needs Hash operation which
is usually faster than the public key encryption. So the only message needs
to be authenticated is hn. This lightweight authentication mechanism is
suitable for the IoT environment.
Suppose there is a video stream server. It wants to authenticate the
movie it sends. So the server uses the following mechanism:

In this project, we use SHA256 as the one way function. Each video
block is 1KB. Of course, the last block may be shorter than 1KB. Please
develop a program to derive Hn. I will give you one video for verification.
The video can be downloaded from my website.