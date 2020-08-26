def search(rows, word, wrap=False):
	"""Search grid for word using specified wrap mode."""
	g = Grid(rows, wrap)
	return g.fullSearch(word)

class Grid(object):
	def __init__(self, rows, wrap):
		self.rows = rows
		self.wrap = wrap  # True/False
		self.N = len(rows)
		self.M = len(rows[0])

		self.letters = self.__letterHash()
		self.adjacent = self.__adjacentHash()

	def coordinates(self):
		"""Iterate through N by M grid from left to right, top to bottom."""
		for i in range(self.N):
			for j in range(self.M):
				yield i, j

	def __hashCoor(self, i, j):
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
			coor = self.__hashCoor(i,j)
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
		"""Return list of coordinates adjacent to (i,j).
		#NOTE: Output depends on wrap mode."""
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
			assert len(adjacent) == 8
		else:
			# remove coordinates that are outside of the grid
			adjacent = [coor for coor in possible if self.__isInsideGrid(*coor)]
		return [self.__hashCoor(*coor) for coor in  adjacent]

	def __adjacentHash(self):
		"""
		Return hash table with entries in format: {0-0: adjacent_coordinates1, 0-1: adjacent_coordinates2, ...} for all coordinates.
		"""
		h = {}
		for i,j in self.coordinates():
			adjacent_coordinates = self.__adjacent_coordinates(i, j)
			coor = self.__hashCoor(i,j)  # coordinates in string format
			h[coor] = adjacent_coordinates
		return h

	def find(self, word, idx=0, coor="0-0"):
		"""Recursive solution: check if given coordinates start match current word index."""
		if idx < len(word):  # search for idx-th char in word
			if self.letters[coor] == word[idx]:
				return any( self.find(word, idx+1, nextcoor) for nextcoor in self.adjacent[coor] )
			else:
				return False
		else:			   # found the last letter
			return True

	def fullSearch(self, word):
		"""Run the find method for every coordinate in the grid."""
		for i,j in self.coordinates():
			coor = self.__hashCoor(i, j)
			start_idx = 0
			if self.find(word, start_idx, coor):
				return True
		return False
