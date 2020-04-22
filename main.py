import sys

interpreter = sys.executable.split('/')[-1]
if interpreter == 'python3':
	from tkinter import Frame, Label, CENTER
else:
	from Tkinter import Frame, Label, CENTER
from src.logics import GameLogics
import src.constants as const


class Game2048(Frame, GameLogics):

	# Frame (master) -> Frame (background) -> Frame (cells) -> Labels (text) [all visualized as grids)
	# 1. Create a master Frame (construct it from the object of Game2048) ( Frame is a widget )
	# 2. Visualize the created Frame as a Grid
	# 3. Bind the Frame with a functionality (i.e. if any key is pressed/event occurs, call a handle)
	# 4. Create a map of commands/keys that may cause an event (keys: function) (eg-> 'w': moveUp) 
	# 5. Maintain a grid_cells list.
	# 6. Create cells inside the grid (make UI)
	# 7. Initialize the board (with all 0's except two random locations which stores 2 in them)
	# 8. Update grid cells as per the content of board (modify UI based on the board state). 
	# 9. Run the mainloop()
	def __init__(self):

		Frame.__init__(self)			# <1>
		self.grid()						# <2>
		self.master.title("2048")		
		self.master.bind('<Key>', self.key_pressed)		# <3>

		self.commands = {	const.KEY_UP: self.moveUp, const.KEY_DOWN: self.moveDown, 
							const.KEY_LEFT: self.moveLeft, const.KEY_RIGHT: self.moveRight
						}				# <4>

		self.grid_cells = []			# <5>
		self.init_grid()				# <6>
		GameLogics.__init__(self)       # <7>
		self.update_grid_cells()		# <8>
		self.mainloop()					# <9>
		

	# This function adds cells to the grid
	# 1. Add another Frame (which acts as background) inside the master frame (self).
	# 2. Visualize this Frame too as a grid
	# 3. Add cells to the grid
	#	3.1 Create a frame inside the above frame (background frame)
	#	3.2 Visualize the frame as a grid adding it to ith row and jth column
	#	3.3 Inside this cell (this grid), add a label 
	#	3.4 Visualize the label as a grid too
	#	->  Now, the label covers the cell completely. A label is the only part that changes whereas
	#	->  the cells remain untouched. A label will represent any text (numbers) on it.
	#	3.5 Append the label to the row_cell[] (which stores labels in a row).
	#	3.6 After geting all the labels of a row in row_cell[], append row_cell[] to self.grid_cells[]
	# 4. Do <3> for all the rows (4 in our case)
	#
	# -> In the end, we'll have all the labels stored in self.grid_cells[]. To update the UI, we just
	#	 need to update the labels inside self.grid_cells[]
	def init_grid(self):
		background = Frame( self, bg = const.BACKGROUND_COLOR_GAME,
							width  = const.SIZE, 
							height = const.SIZE  ) 		# <1>
		background.grid()				# <2>

		for r in range(const.GRID_LEN):		# <3>
			row_cells = []
			for c in range(const.GRID_LEN):
				cell = Frame( background, bg = const.BACKGROUND_COLOR_CELL_EMPTY,
							  width  = (const.SIZE / const.GRID_LEN),
							  height = (const.SIZE / const.GRID_LEN) )	# <3.1>
				cell.grid( row = r, column = c,
						   padx = const.GRID_PADDING,
						   pady = const.GRID_PADDING )		# <3.2>
	
				label = Label( master = cell, text = '',
							   bg = const.BACKGROUND_COLOR_CELL_EMPTY,
							   justify = CENTER, font = const.FONT,
							   width = 5, height = 2 )		# <3.3>
				label.grid()		# <3.4>
				
				row_cells.append(label)		# <3.5>
		
			self.grid_cells.append(row_cells)		# <3.6>
		


	# This updates the UI as the logic changes the board state (via labels stored in self.grid_cells[]
	# 1. Iterate over all the labels (stored in self.grid_cells)
	# 2. Get values from self.board[i][j] and update/configure the labels accordingly.
	# 3. Labels are configured with text, background color (of cell) and foreground color (of text)
	# 4. Wait (don't return) until all configuration is done
	def update_grid_cells(self):
		
		for r in range(const.GRID_LEN):			# <1>
			for c in range(const.GRID_LEN):
				
				value = self.board[r][c]	# <2>
				if value == 0:
					self.grid_cells[r][c].configure( text = '',
													 bg = const.BACKGROUND_COLOR_CELL_EMPTY)		# <3>
				else:
					self.grid_cells[r][c].configure( text = str(value),
													 bg = const.BACKGROUND_COLOR_DICT[value],
													 fg = const.CELL_COLOR_DICT[value])
				
		self.update_idletasks()				# <4>


	# Defines the handler for the events registered via frame.bind().
	# Events here will be keys pressed. Define actions for events = 'w', 's', 'a', 'd'
	# 1. Get printable representation of the key pressed by player
	# 2. If key is either of 'w', 's', 'a' or 'd', then - 
	# 	2.1 Call the desired movement function and get the new board state 
	#	2.2 If the state of board is changed (i.e. any compression/merge is performed)
	#		2.2.1 Add two 2's on random locations on board
	#		2.2.2 update the UI (via update_grid_cells())
	#		2.2.3 update 'changed' to False (i.e. its default value)
	#		2.2.4 Check Game state
	#			2.2.4.1 If status is WON , write 'YOU WON' to the labels @ [1][1] and [2][2]
	#			2.2.4.2 If status is LOST, write 'YOU LOST' to the labels @ [1][1] and [2][2]
	def key_pressed(self, event):
		key = repr(event.char)		# <1>
	
		if key in self.commands: 	# <2>
			
			self.board, changed = self.commands[key](self.board)		# <2.1>
	
			if changed is True:
				self.placeRandom2()			# <2.2.1>
				self.update_grid_cells()		# <2.2.2>
				changed = False					# <2.2.3>

				game_state = self.getCurrentState()	# <2.2.4>
				if game_state == 'WON':					# <2.2.4.1>
					self.grid_cells[1][1].configure(text = 'YOU', 
													bg = const.BACKGROUND_COLOR_CELL_EMPTY) 
					self.grid_cells[2][2].configure(text = 'WON',
													bg = const.BACKGROUND_COLOR_CELL_EMPTY)

				if game_state == 'LOST':				# <2.2.4.2>
					self.grid_cells[1][1].configure(text = 'YOU', 
													bg = const.BACKGROUND_COLOR_CELL_EMPTY)
					self.grid_cells[2][2].configure(text = 'LOST',
													bg = const.BACKGROUND_COLOR_CELL_EMPTY)

game = Game2048()
	



