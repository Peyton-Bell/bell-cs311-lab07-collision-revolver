### Lab 07 Questions

## Question 1

When using linear probing the average probe length will start to increase sharply as a increases. The higher our a value, the more slots are filled in our hash table. For linear probing this can eventually become really slow because it could potentially go on some long probing runs to try and find an empty slot to store the value. For chaining though this doesn't really matter because it will store mutiple values in the same hash. Insert for chaining will always be O(1) the only problem occurs for lookup timing. If we have a really high a value that means most slots are filled and most of the vlaues we are inserting are going into hashes where there are already values. This could potentially create some long lists in hashes that we would have to iterate through in order to find the exact value we are looking for

## Question 2

Linear Probing:
Successful search: 13/6 = 2.16
Unsuccessful search: 109/18 = 6.06

Chaining:
Successful: 27/20 = 1.35
Unsuccessful: 7/10 = 0.7

For successful probes (the key does have a value) the chaining is faster by roughly 0.81 probes(1.6x faster). For unseccusseful probes (the key doesn't exist) chaining is faster by about 5.36probes (8.65x faster). So overall chaining in this case is faster in any scenario.

## Question 3:

Primary clustering in linear probing is when the values makes these clumps in the array and don't spread out because of the +1 increment nature of linear probing. Quadratic helps mitigate this at first by spreading out the values since it increments quadratically instead of linearly (1, 4, 9, 16, etc). Eventually though, as alpha increases this will still create clumps like linear probing does though.

Hash Table size 11, linear probing:
[-, -, -, -, -, -, -, -, -, -, -]

Insert A to hash index 5 (inserted directly):
[-, -, -, -, -, A, -, -, -, -, -]

Insert B to hash index 5 (collision with A -> probes to index 6 to insert):
[-, -, -, -, -, A, B, -, -, -, -]

Insert C, hashes to index 6 (This is a different original hash than A or B, but still collides becuase of the clustered data and has to probe to 7 to insert)
[-, -, -, -, -, A, B, C, -, -, -]

## Question 4:

As alpha approches 1 linear probing will diverge to infinity because of the 1(1 - alpha) part. Say alpha is 0.9 we will have 1/0.1 = 10. Now if alpha is 0.999 we will have 1/.001 = 1000. This number will continue to diverge closer to infinity as we make alpha closer to 1.

Now for chaining if alpha = 1 we get a 1 + alpha/2 = 1.5 probes. Which is a pretty close to out value from the first question of 1.35 when alpha is 0.7. This shows chaining stays relatively the same no matter the alpha value.

Now for open addressing tables need to resize before alpha = 1 because of the undefined problem we run into when alpha = 1 giving us 1/0. If every slot is full in open addressing then it will probe through the hash table on an infinite loop because there are no open slots to insert to. For chaining this isn't the case because it can insert multiple values to one hash number so even if every slot was full it would still be able to operate.
