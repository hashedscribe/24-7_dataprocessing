# Binary File Architecture
The file will start with a 16-bit integer to index the file number. Should be 0 indexed. We only need 13 bits of the header to denote up to 8000 indices, so, we can use the other 3 for further information.

Each block is stored as a 16-bit integer. From right to left, the representation is as follows:

| \# (by shift, 1-indexed) | Mask (applied to raw block) | Representation                                          | Notes                                                                                                                         |
| ------------------------ | --------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 1                        | `0x01`                      | Marks if the block has been allocated/set or not        | Makes sure that even if categories are 0-indexed that it will be accurate                                                     |
| 2                        | `0x02`                      | Marks if the block has a note attached to it            | #flag/revisit if there is a note, how do we point to where it is? is there just another file that stores all the notes?       |
| 3, 4, 5, 6, 7, 8         | `0xFC`                      | Index of the category it should be mapped to            | From 6 bits, there are 64 indices where which should be enough for general usage                                              |
| 9 - 16                   | `^0xFF`                     | Index of the block in relation to the header file index | Stores up to 256 blocks (5 days perfectly). Requires that there is a header at the top of the file to denote the file number. |

Since not every block needs to know where it comes from, if we had a header to the file to denote the file number in the sequence. Then, to get the full index, we can just do the multiplication. That should get us to using a 16-bit where the other 8 bits are used to denote the index within the file.