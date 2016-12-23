import random
import operator, time

class Solver:
	# Initialize board and make conflicts dictionary
	def __init__(self, numRow=8, numCol=8, numQueen=8):
		self.rows = numRow
		self.cols = numCol
		self.numQueen = numQueen
		self.board = []
		self.conflicts = {}
		# Populate the board with tuples for each square
		for r in range(self.rows):
			for c in range(self.cols):
				self.board.append((r, c))
				self.conflicts[(r, c)] = 0
		self.queen_squares = self.randomQueens()
		self.update_conflicts()

	# Place one queen on each row
	def randomQueens(self):
		queen_squares = []
		for col in range(self.cols):
			row = random.randint(0, self.rows - 1)
			queen_squares.append((row, col))
		print queen_squares
		return queen_squares
	
	# Get all the squares a queen on 'square' hits
	def get_neighbors(self, square):
		row, col = square[0], square[1]
		neighbors = []
		for r in range(self.rows):
			for c in range(self.cols):
				try:
					slope = (row - r)*1.0 / (col - c)
					if slope == 1 or slope == -1 or slope == 0:
						neighbors.append((r, c))
				except ZeroDivisionError:
					neighbors.append((r, c))
		return neighbors

	# update the conflicts dictionary
	def update_conflicts(self):
		self.conflicts = dict.fromkeys(self.conflicts.iterkeys(), 0)
		for queen in self.queen_squares:
			neighbors = self.get_neighbors(queen)
			for neighbor in neighbors:
				self.conflicts[neighbor] += 1

	# with probaility (1 - alpha), move a random queen to the min conflict square
	# with probability (alpha), move a random queen to a random unoccupied square

	def update(self, alpha = 0.05):
		index = random.randint(0, self.numQueen - 1)
		used_square = self.queen_squares.pop(index)
		self.update_conflicts()
		sample = random.random()
		if sample >= alpha:
			i = 0
			square = sorted(self.conflicts.items(), key=lambda x: x[1])[i][0]
			while square in self.queen_squares or square == used_square:
				i += 1
				square = sorted(self.conflicts.items(), key=lambda x: x[1])[i][0]
			self.queen_squares.append(square)
		else:
			print "ALPHA EVENT"
			square = self.queen_squares[0]
			while square in self.queen_squares or square == used_square:
				row = random.randint(0, self.rows - 1)
				col = random.randint(0, self.cols - 1)
				square = (row, col)
			self.queen_squares.append(square)
		self.update_conflicts()

	# Checks if the board is currently solved.
	def isSolved(self):
		for queen in self.queen_squares:
			if self.conflicts[queen] != 1:
				return False
		return True

	# update and keep running until solved.
	def run(self):
		iteration = 0
		while(not self.isSolved()):
			self.update()
			conflicts = []
			for r in range(self.rows):
				string = ""
				for c in range(self.cols):
					if (r, c) in self.queen_squares:
						string += "Q"
						conflicts.append(self.conflicts[(r,c)])
					else:
						string += "X"
				print string
			print conflicts
			iteration += 1
			print "Iteration: " + str(iteration)
			print
		print "SOLVED: " + str(self.queen_squares)

solver = Solver()
solver.run()
