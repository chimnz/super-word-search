# super-word-search

I created a `Grid` class to encapsulate the data that I would be working with.
I computed hash tables with key `pos` for every "position" on the board.
The position hashes were computed using the `__position` method,
and they had the form `"{i}-{j}"`, where (i, j) are the position coordinates in
the 2D array, `rows`, which represents the grid.
With hash tables for `coordinates`, `letters`, and `adjacent_positions`, I
wrote a recursive `find` method which I ran for every position on the grid.