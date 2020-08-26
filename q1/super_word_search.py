def search(rows, word, wrap=False):
	"""Search grid for word using specified wrap mode."""
	g = Grid(rows, wrap)
	return g.fullSearch(word)

class Grid(object):
	def __init__(self, rows, wrap):
		self.rows = rows
		self.N, self.M = len(rows), len(rows[0])
		self.wrap = wrap  # True/False

		hash_tables = self.__computeHashTables()
		self.letters = hash_tables["letters"]    # position => letter
		self.adjacent = hash_tables["adjacent"]  # position => adjacent_positions

	def coordinates(self):
		"""Iterate through N by M grid from left to right, top to bottom."""
		for i in range(self.N):
			for j in range(self.M):
				yield i, j

	def __position(self, i, j):
		"""Convert coordinates into string of format "{i}{j}" which
		represents position within grid (flattened along axis 0)."""
		pos = str(i) + str(j)  # "{i}{j}"
		return pos	# position, key for both self.letters and self.adjacent

	def __computeHashTables(self):
		letters = {}   # "pos": "{letter}"
		adjacent = {}  # "pos": [adj_pos1, adj_pos2, ...]
		for i, j in self.coordinates():
			pos = self.__position(i,j)
			letters[pos] = self.rows[i][j]  # letter at pos
			adjacent[pos] = self.__adjacent_positions(i, j)  # positions adjacent to pos
		return { "letters": letters, "adjacent": adjacent }

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
		else:
			if i == -1:        # out-left
				i = self.M-1   # rightmost
			elif i == self.M:  # out-right
				i = 0          # leftmost
			
			if j == -1:        # out-top
				j = self.N-1   # bottommost
			elif j == self.N:  # out-bottom
				j = 0          # topmost

		assert self.__isInsideGrid(i, j)  # i,j should now be inside grid
		return i, j

	def __adjacent_positions(self, i, j):
		"""Return list of positions (hashed coordinates) adjacent to (i,j). #NOTE: Output depends on wrap mode."""
		# possible adjacent coordinates form square ring (8 positions) around (i,j)
		possible = [
			(i-1, j-1), (i-1, j), (i-1, j+1),
			(i, j-1), (i, j+1),
			(i+1, j-1), (i+1, j), (i+1, j+1)
		]

		if self.wrap:
			# transform coordinates that are outside the grid into
			# their corresponding inside-grid, wrap-obeying counterparts
			adjacent_coordinates = [self.__wrapTransform(*coor) for coor in possible]
			assert len(adjacent_coordinates) == 8  # wrapping forces max number of adjacent positions
		else:
			# filter out coordinates that are outside of the grid
			adjacent_coordinates = [coor for coor in possible if self.__isInsideGrid(*coor)]

		return [ self.__position(*coor) for coor in  adjacent_coordinates ]  # NOTE: return positions, not coordinates

	def find(self, word, pos, idx=0):
		"""Recursively find letter matches: check if word[idx] is the char (letter) at the specified position."""
		if idx < len(word):  # search for idx-th char in word
			if self.letters[pos] == word[idx]:
				return any( self.find(word, nextpos, idx+1) for nextpos in self.adjacent[pos] )
			else:
				return False
		else:			     # found the last letter
			return True

	def fullSearch(self, word):
		"""Run the find method for every coordinate in the grid until a word match is found."""
		for i,j in self.coordinates():
			pos = self.__position(i, j)
			if self.find(word, pos):
				return True
		return False