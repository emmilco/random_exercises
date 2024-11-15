You are going on a road trip, and would like to create a suitable music playlist. 
The trip will require N songs, though you only have M songs downloaded, 
where M < N. A valid playlist should select each song at least once, 
and guarantee a buffer of B songs between repeats.

Given N, M, and B, determine the number of valid playlists.

Playlist of length N
Unique song list of length M
Buffer of B

M songs (count the permutations)
But also they 
TIMES
M - N = remainder (M)^(M-N)

M = 1
N = 2


(A, B)

<!-- AAA 000 -->
AAB 001
ABA 010
ABB 011
BAA 100
BAB 101
BBA 110
<!-- BBB 111 -->

ABCXX -> if we can figure out how many permutations there are for ABCXX, and multiply it by the number of ways of populating each X (M^X) -> that gives us the no-buffer number of valid playlists


Step one: what are all the permutations of the unique set of songs
Step two: what are all the permutations of XX
Step three: what are all the permutations of 


N! / (N-M)! -> all the permutations of ABCXX
5! / (5-3)! -> 120 / 2 -> 60

M^(N-M) -> all the ways to populate the Xs
3^(5-3) -> 9

Total number of base playlists (without buffer) = 540

Buffer B has to be <= number of unique songs M


B = 2
M = 3
N = 5

[]_____
M choices
[_]____
M - 1 choices
[__]___
M - 2
_[__]__
M - 2
__[__]_
M - 2


suppose B = 1

[]_____
M choices
[_]____
M - 1 choices
_[_]___
M - 1
__[_]__
M - 1
__[__]_
M - 1

In the Xth place
there are M - B choices
But for X < B there are (M - (B - X)) choices
