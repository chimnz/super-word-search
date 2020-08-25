def coordinates(grid):
	"""Iterate through N by M grid from left to right, top to bottom."""
	N, M = len(grid), len(grid[0])
	for i in range(N):
		for j in range(M):
			coor = (i, j)
			yield coor

def _letterHash(grid):
	"""
	Return hash table with entries in format:
	{0-0: letter1, 0-1: letter2, ...} for all coordinates in grid.
	"""
	h = {}
	for coor in coordinates(grid):
		i, j = coor
		# tuple cannot be hashed (used as key)
		hashable_coor = '-'.join(str(idx) for idx in coor)
		h[hashable_coor] = grid[i][j]
	return h

def search(grid, word, wrap=False):
	"""Search grid for word using specified wrap mode."""
	return _letterHash(grid)