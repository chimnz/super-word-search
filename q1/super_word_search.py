def search(rows, word, wrap=False):
	"""Search grid for word using specified wrap mode."""
	g = Grid(rows, wrap)
	return g.fullSearch(word)

class Grid(object):
	def __init__(self, rows, wrap):
		self.rows = rows
		self.N = len(rows)    # max value of i
		self.M = len(rows[0]) # max value of j
		self.wrap = wrap      # True/False

		hash_tables = self.__computeHashTables()
		self.coordinates = hash_tables['coordinates'] # position => (i,j)
		self.letters = hash_tables['letters']         # position => letter
		self.adjacent = hash_tables['adjacent']       # position => adjacent_positions

	def iter(self):
		"""Iterate through coordinates in N by M grid from left to right, top to bottom."""
		for i in range(self.N):
			for j in range(self.M):
				yield i, j

	def __position(self, i, j):
		"""Convert coordinates into string of format "{i}{j}" which
		represents position within grid (flattened along axis 0)."""
		pos = '{}-{}'.format(i, j)  # "{i}-{j}"
		return pos	# position, key for both self.letters and self.adjacent

	def __computeHashTables(self):
		coordinates = {}  # pos: (i,j)
		letters = {}   # pos: letter
		adjacent = {}  # pos: [adj_pos1, adj_pos2, ...]
		for i,j in self.iter():
			pos = self.__position(i,j)
			coordinates[pos] = i,j
			letters[pos] = self.rows[i][j]  # letter at pos
			adjacent[pos] = self.__adjacent_positions(i, j)  # positions adjacent to pos
		return { "coordinates": coordinates, "letters": letters, "adjacent": adjacent }

	def __isInsideGrid(self, i, j):
		"""Check whether (i,j) is inside the grid."""
		if 0 <= i < self.N and 0 <= j < self.M:
			return True
		return False

	def __wrapTransform(self, i, j):
		"""Convert out-of-grid coordinates into their wrapped counterparts."""
		if self.__isInsideGrid(i, j):
			return i, j
		else:
			if i == -1:        # out-left
				i = self.N-1   # rightmost
			elif i == self.N:  # out-right
				i = 0          # leftmost
			
			if j == -1:        # out-top
				j = self.M-1   # bottommost
			elif j == self.M:  # out-bottom
				j = 0          # topmost

		assert self.__isInsideGrid(i, j)  # i,j should now be inside grid
		return i, j

	def __adjacent_positions(self, i, j):
		"""Return list of positions (hashed coordinates) adjacent to (i,j).
		#NOTE: Output depends on wrap mode."""
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

	def find(self, word, pos, idx=0, bucket=None, checked=None, stack=None):
		"""
		Recursively find letter matches: check if word[idx] is the char (letter) at the specified position.
		bucket: empty list defined in outer scope; records word matches if any
		checked: empty hash table defined in outer scope; tracks previously checked positions, so no repeat positions
		stack: empty list defined in outer scope; records positions with matching letters
		"""
		if idx < len(word):  # search for idx-th char in word
			if self.letters[pos] == word[idx] and not checked.get(pos):
				stack.append( self.coordinates[pos] )  # append coordinates of current position
				checked[pos] = True
				return any( self.find(word, nextpos, idx+1, bucket, checked, stack) for nextpos in self.adjacent[pos] )
			return False
		# found the last letter
		bucket.append( stack )  # every time a word is found, add it to bucket
		return True

	def fullSearch(self, word):
		"""Run the find method for every position in the grid.
		Return bucket of found words and their constituent positions."""
		bucket = []       # words found, [(word, [pos1_1, pos_2_1, ...]), (word, [pos1_2, pos_2_2)]
		for i,j in self.iter():
			checked = {}  # checked positions, {pos1: True, pos2: True, ...}
			stack = []    # chars found, [pos1, pos2, ...]
			pos = self.__position(i, j)
			self.find(word, pos, bucket=bucket, checked=checked, stack=stack)
		if len(bucket) > 0:
			return bucket
		return None