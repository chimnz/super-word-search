def _hashGrid(grid, wrap):
	"""Return hash table with entries
	in format: {0-0: letter1, 0-1: letter2, ...}
	for all coordinates in the grid."""
	h = {}
	N, M = len(grid), len(grid[0])
	for i in range(N):
		for j in range(M):
			coor = (i, j)
			hashable_coor = '-'.join(str(idx) for idx in coor)  # tuple cannot be hashed (used as key)
			h[hashable_coor] = grid[i][j]
	return h

def search(grid, word, wrap=False):
	"""Search grid for word using specified
	wrap mode. Return boolean."""
	coor = _hashGrid(grid=grid, wrap=wrap)
	return coor