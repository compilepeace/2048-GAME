# Author: Abhinav Thakur
# Email : compilepeace@gmail.com
# Description: This module contains all the logics involved in 2048-game

import random


class GameLogics:
	
	# Initializes the board with two random locations storing 2
	def __init__(self):
		self.board = [[0 for j in range(4)] for i in range(4)]
		self.placeRandom2()
		self.placeRandom2()


	def placeRandom2(self):
		# get random [row][column] and check if it is vacant
		while True:
			row = random.randint(0, 3)
			col = random.randint(0, 3)
		
			if self.board[row][col] == 0:
				self.board[row][col] = 2
				break
		return

	
	# Returns a compressed matrix and a flag which denotes whether or not 
	# any compression has been performed (True/False)
	def __compressLeft(self, board):
		# Create a new matrix to store left compressed board
		new_matrix       = [[0 for j in range(4)] for i in range(4)]
		CHANGED_FLAG = False
		
		for r in range(4):
			pos = 0
			# Store all values (not 0) into the new_matrix (remaining places are already 0)
			for c in range(4):
				if board[r][c] != 0:
					new_matrix[r][pos] = board[r][c]
					if pos != c:
						CHANGED_FLAG = True		# compression is done only when pos != c
					pos += 1
		
		return new_matrix, CHANGED_FLAG


	# Returns the orginal board (provided as input) with values merged and a FLAG denoting whether
	# or not the board state has been changed (True/False) 
	def __mergeLeft(self, board):
		
		CHANGED_FLAG = False
		for r in range(4):
			for c in range(3):
				if board[r][c] == board[r][c+1]:
					board[r][c] *= 2 
					board[r][c+1] = 0
					CHANGED_FLAG = True
		
		return board, CHANGED_FLAG


	# Returns a reversed matrix
	def __reverse(self, board):
		new_matrix = [[0 for j in range(4)] for i in range(4)]

		for r in range(4):
			pos = 0
			for c in range(4):	
				new_matrix[r][ 3 - c ] = board[r][c]

		return new_matrix


	# Returns a Transposed matrix
	def __transpose(self, board):
		new_matrix = [[0 for j in range(4)] for i in range(4)]

		for r in range(4):
			for c in range(4):
				new_matrix[c][r] = board[r][c]

		return new_matrix


	# Returns a matrix (with the left move performed) and a FLAG denoting whether or not the board
	# state has been changed (True/False)
	def moveLeft(self, board):
	
		# 'changed' stores True if board state changes during compression and merging	
		# CompressLeft -> Merge -> CompressLeft
		new_matrix, changed1 = self.__compressLeft(board)
		new_matrix, changed2 = self.__mergeLeft(new_matrix)	
		changed              = changed1 or changed2	
		new_matrix, ignore   = self.__compressLeft(new_matrix)
		
		return new_matrix, changed 

	
	# Returns a matrix (with the right move performed) and a FLAG denoting whether or not the board
	# state has been changed (True/False)
	def moveRight(self, board):
		
		# 'changed' stores True if board state changes during compression and merging
		# Reverse -> CompressLeft -> Merge -> CompressLeft -> Reverse
		new_matrix           = self.__reverse(board)
		new_matrix, changed1 = self.__compressLeft(new_matrix)
		new_matrix, changed2 = self.__mergeLeft(new_matrix)
		changed              = changed1 or changed2
		new_matrix, ignore   = self.__compressLeft(new_matrix)
		new_matrix           = self.__reverse(new_matrix)

		return new_matrix, changed
		

	# Returns a matrix (with the up move performed) and a FLAG denoting whether or not the board
	# state has been changed (True/False)
	def moveUp(self, board):

		# Transpose -> CompressLeft -> Merge -> CompressLeft -> Transpose
		new_matrix           = self.__transpose(board)
		new_matrix, changed1 = self.__compressLeft(new_matrix)
		new_matrix, changed2 = self.__mergeLeft(new_matrix)
		changed              = changed1 or changed2
		new_matrix, ignore   = self.__compressLeft(new_matrix)
		new_matrix           = self.__transpose(new_matrix)

		return new_matrix, changed

	# Returns a matrix (with the down move performed) and a FLAG denoting whether or not the board
	# state has been changed (True/False)
	def moveDown(self, board):
	
		# Transpose -> [Reverse -> CompressLeft -> Merge -> CompressLeft -> Reverse]  -> Transpose
		# Transpose -> moveRight -> Transpose (basically)
		new_matrix           = self.__transpose(board)
		new_matrix           = self.__reverse(new_matrix)
		new_matrix, changed1 = self.__compressLeft(new_matrix)
		new_matrix, changed2 = self.__mergeLeft(new_matrix)
		changed              = changed1 or changed2
		new_matrix, ignore   = self.__compressLeft(new_matrix)
		new_matrix           = self.__reverse(new_matrix)
		new_matrix           = self.__transpose(new_matrix)

		return new_matrix, changed


	# Returs 'WIN', 'NOT YET OVER' and 'GAME OVER' 
	def getCurrentState(self):
		
		# If any block on the board has 2048, player 'WIN'
		for r in range(4):
			for c in range(4):
				if self.board[r][c] == 2048:
					return 'WON'

		# If any block has a 0 on it,
		for r in range(4):
			for c in range(4):
				if self.board[r][c] == 0:
					return 'NOT YET OVER'

		# check for all rows and cols except last one.
		for r in range(3):
			for c in range(3):
				if self.board[r][c] == self.board[r][c+1] or self.board[r][c] == self.board[r+1][c]:
					return 'NOT YET OVER'

		# check each column for last row
		for c in range(3):
			if self.board[3][c] == self.board[3][c+1]:
				return 'NOT YET OVER'
	
		# check each row for last column
		for r in range(3):
			if self.board[r][3] == self.board[r+1][3]:
				return 'NOT YET OVER'

		return 'LOST'

