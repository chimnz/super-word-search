def search(rows, word, wrap=False):
	"""Search grid for word using specified wrap mode."""
	g = Grid(rows, wrap)
	return g.find(word)

class Grid(object):
	def __init__(self, rows, wrap):
		self.rows = rows
		self.wrap = wrap  # True/False
		self.N = len(rows)
		self.M = len(rows[0])

	def coordinates(self):
		"""Iterate through N by M grid from left to right, top to bottom."""
		for i in range(self.N):
			for j in range(self.M):
				yield i, j

	def __hashCoor(i, j):
		"""Convert index tuple into string of format "{i}-{j}"."""
		coor = i,j  # tuple
		hashable_coor = '-'.join(str(idx) for idx in coor)  # string
		return hashable_coor

	def __letterHash(self):
		"""
		Return hash table with entries in format: {0-0: letter1, 0-1: letter2, ...} for all coordinates.
		"""
		h = {}  # "{i}-{j}": "LETTER"
		for i, j in self.coordinates():
			letter = self.rows[i][j]
			coor = __hashCoor(i,j)
			h[coor] = letter
		return h

	def __isInsideGrid(self, i, j):
		"""Check whether (i,j) is inside the grid."""
		if 0 <= i < self.N:
			if 0 <= j < self.M:
				return True
		return False

	def __wrapTransform(self, i, j):
		"""Convert out-of-grid coordinates into their wrapped counterparts."""
		if self.__isInsideGrid(i, j):
			return i, j

		if i == -1:        # out-left
			i = self.M-1   # rightmost
		elif i == self.M:  # out-right
			i = 0          # leftmost
		
		if j == -1:        # out-top
			j = self.N-1   # bottommost
		elif j == self.N:  # out-bottom
			j = 0          # topmost

		# i,j should now be inside grid
		assert self.__isInsideGrid(i, j)
		return i, j

	def __adjacent_coordinates(self, i, j):
		"""Return list of coordinates adjacent to (i,j). Output depends on wrap mode."""
		# possible adjacent coordinates form square ring around (i,j)
		possible = [
			(i-1, j-1), (i-1, j), (i-1, j+1),
			(i, j-1), (i, j+1),
			(i+1, j-1), (i+1, j), (i+1, j+1)
		]

		if self.wrap:
			# transform coordinates that are outside the grid into
			# their corresponding inside-grid, wrap-obeying counterparts
			adjacent = [self.__wrapTransform(*coor) for coor in possible]
		else:
			# remove coordinates that are outside of the grid
			adjacent = [coor for coor in possible if __isInsideGrid(*coor)]
		return adjacent

	def __adjacentHash(self):
		"""
		Return hash table with entries in format: {0-0: adjacent_coordinates1, 0-1: adjacent_coordinates2, ...} for all coordinates.
		"""
		h = {}
		for i,j in coordinates(grid):
			adjacent_coordinates = _getAdjacentCoordinates(*coor)
			coor = __hashCoor(i,j)
			h[coor] = adjacent_coordinates
		return h

	def find(self, word):
		return self.__wrapTransform(-1, 2)