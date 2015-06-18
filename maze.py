#COMP SCI 1XA3 Project
#main.py
#Pasindu Gunasekara
#1412155

#The Recursive explore function requires the recursion depth to be set higher as the maze size gets larger, this can be changed in the main function.
#Since the Start, end, and key positions are random, there may sometimes be overlap on their positions.

#Both the start, end, and key are picked randomly.

from graphics import *
import random


class MyStack():
	def __init__(self):
		self.stack = []
	def push(self,item,S):
		return S + [item]
	def pop(self,S):
		return S.pop()
	def isEmpty(self,S):
		if(len(S) == 0):
			return True
		else:
			return False
	def size(self,S):
		return len(S)

class Maze():
	def __init__(self,n):
		self.maze = [[[[0],[0],[0,0,0,0],[1,1,1,1]] for i in range(n + 2)] for j in range(n+2)]
		self.size = n+2
		self.cellStack = []
		self.exploreStack = MyStack()
		self.first = True

		#Set Outer Border
		for i in range(1,n+1): #y value
			for j in range(1,n+1): #x value
				#At the top row
				if(i==1):
					self.maze[i][j][2][3] = 1
				#Bottom
				if(i==(n)):
					self.maze[i][j][2][1] = 1

				#Right
				if(j==1):
					self.maze[i][j][2][0] = 1

				#Left
				if(j==(n)):
					self.maze[i][j][2][2] = 1


#---------------------------------------------------------------GENERATE MAZE---------------------------------------------------------------#
	def findNeighbours(self,x,y):
		#Find a cell with all walls up
		locations = [0,0,0,0]
		#North
		#All walls are up, and no border to the north of the current Cell
		if((self.maze[y-1][x][3] == [1,1,1,1]) and (self.maze[y][x][2][3] != 1)):
			locations[3] = 1

		#South
		if((self.maze[y+1][x][3] == [1,1,1,1]) and (self.maze[y][x][2][1] != 1)):
			locations[1] = 1

		#West
		if((self.maze[y][x-1][3] == [1,1,1,1]) and (self.maze[y][x][2][0] != 1)):
			locations[0] = 1

		#East
		if((self.maze[y][x+1][3] == [1,1,1,1]) and (self.maze[y][x][2][2] != 1)):
			locations[2] = 1

		return locations

	def generate(self):
		self.stack = MyStack()
		cellStack = []

		totalCells = (self.size-2) * (self.size-2)
		
		#CurrentCell
		x = random.randint(2,self.size-2)
		y = random.randint(2,self.size-2)
		currentCell = (y,x)

		self.start = (x,y)
		self.key = (random.randint(2,self.size-2),random.randint(2,self.size-2))
		self.end = (random.randint(2,self.size-2),random.randint(2,self.size-2))

		visitedCells = 1

		while(visitedCells < totalCells):
			#Find indices of all neighbours
			neighbours = self.findNeighbours(x,y)

			if(sum(neighbours)>=1):
				neighbours = [neighbours for neighbours, l in enumerate(neighbours) if l == 1]
				#Choose Random Neighbour
				
				neighbour = random.choice(neighbours)

				#Knock down wall between neighbour and current cell
				self.maze[y][x][3][neighbour] = 0

				#Move Current Cell into cellStack
				cellStack = self.stack.push((y,x),cellStack)

				#Change current Cell to new neighbour cell
				#Change the y and x values
				#Knock down wall from neighbour cell
				if(neighbour == 0):
					#Move West
					x = x-1
					self.maze[y][x][3][2] = 0
				elif(neighbour == 1):
					#Move South
					y = y+1
					self.maze[y][x][3][3] = 0
				elif(neighbour == 2):
					#Move East
					x = x+1
					self.maze[y][x][3][0] = 0
				elif(neighbour == 3):
					#Move North
					y = y-1
					self.maze[y][x][3][1] = 0

				#Increment VisitedCells by 1
				visitedCells = visitedCells+1

			else:
				#Pop the most recent cell entry
				currentCell = self.stack.pop(cellStack)
				#Popped item becomes the new current cell x/y values
				y = currentCell[0]
				x = currentCell[1]

		#Pick end point at the edges of the maze
		#X = 1 or Y = 2
#----------------------------------------------------END GENERATE----------------------------------------------------#

#------------------------------------------------------SOLUTION------------------------------------------------------#
	def findVisitableNeighbours(self,x,y):
		w = [0,0,0,0]
		#    W,S,E,N
		#North
		#Check if visited, not a border/wall
		if(self.maze[y-1][x][0] == [0] and (self.maze[y][x][2][3] != 1) and (self.maze[y][x][3][3] != 1)):
			w[3] = 1

		#South
		if(self.maze[y+1][x][0] == [0] and (self.maze[y][x][2][1] != 1) and (self.maze[y][x][3][1] != 1)):
			w[1] = 1

		#East	
		if(self.maze[y][x+1][0] == [0] and (self.maze[y][x][2][2] != 1) and (self.maze[y][x][3][2] != 1)):
			w[2] = 1

		#West
		if(self.maze[y][x-1][0] == [0] and (self.maze[y][x][2][0] != 1) and (self.maze[y][x][3][0] != 1)):
			w[0] = 1
		return w



	def explore(self,x,y,ex,ey):
		#Check Which neighbours don't have backtracks on them
		#W,S,E,N
		back = self.findVisitableNeighbours(x,y)

		#Base Case
		if(x == ex and y == ey):
			#stop Exploring
			#Return final cellStack to stop loop
			return self.cellStack
		else:
			if(sum(back) >= 1):
				#If no wall to north/unvisited

				#Pick random direction
				back = [back for back, l in enumerate(back) if l == 1]
				neighbour = random.choice(back)

				#Push current cell into self.cellStack
				if(neighbour == 3):
					#Mark Current Cell with backtrack and next cell with backtrack
					self.cellStack = self.exploreStack.push((x,y),self.cellStack)
					self.maze[y][x][0] = [1]
					if(self.first == False):
						self.maze[y-1][x][0] = [1]
					self.first = False

					#Recursively explore neighbours
					self.explore(x,y-1,ex,ey)

				#If no wall East/univisited
				if(neighbour == 2):
					self.cellStack = self.exploreStack.push((x,y),self.cellStack)
					#Mark Backtrack Cells
					self.maze[y][x][0] = [1]
					if(self.first == False):
						self.maze[y][x+1][0] = [1]
					self.first = False

					self.explore(x+1,y,ex,ey)

				#If no wall South/Unvisited
				if(neighbour == 1):
					self.cellStack = self.exploreStack.push((x,y),self.cellStack)
					#Mark Backtrack Cells
					self.maze[y][x][0] = [1]
					if(self.first == False):
						self.maze[y+1][x][0] = [1]
					self.first = False

					self.explore(x,y+1,ex,ey)

				#If no wall West/unvisited
				if(neighbour == 0):
					self.cellStack = self.exploreStack.push((x,y),self.cellStack)
					#Mark Backtrack Cells
					self.maze[y][x][0] = [1]

					if(self.first == False):
						self.maze[y][x-1][0] = [1]
					self.first = False

					self.explore(x-1,y,ex,ey)

			else:
				#If there is nowhere else to go, backtrack
				backtrackCell = self.exploreStack.pop(self.cellStack)
				#print("Pop")
				self.explore(backtrackCell[0],backtrackCell[1],ex,ey)


	def setSolution(self,stack,num):
		#Use for loops with the cellStack to change the bits on solution
		#from 0 to 1
		#Modify self.maze
		for i in stack:
			#print("sol")
			if(self.maze[i[1]][i[0]][1] == [1]):
				self.maze[i[1]][i[0]][1] = [3]
			else:
				self.maze[i[1]][i[0]][1] = num



	def draw(self):
		win = GraphWin("Maze - Pasindu Gunasekara 1412155",self.size*25,self.size*25)
		win.setBackground('White')

		for i in range(1,self.size-1):
			for j in range(1,self.size-1):
				start = Point(i*25, j*25)
				end = Point(i*25 + 25, j*25 + 25)
				grid = Rectangle(start, end)
				grid.draw(win)


		for i in range(0,self.size): #x - value
			for j in range(0,self.size): #y - value
				#NORTH WALL
				if(self.maze[i][j][3][3] == 0):
					start = Point(j*25, i*25)
					end = Point((j*25) + 25, i*25)
					northSouth = Line(start, end)
					northSouth.setFill('white')
					northSouth.draw(win)

				#WESTERN WALL
				if(self.maze[i][j][3][2] == 0):
					start = Point(j*25 + 25, i*25)
					end = Point(j*25+25, i*25 + 25)
					eastWest = Line(start, end)
					eastWest.setFill('white')
					eastWest.draw(win)

		#Draw Solution
		for i in range(1,self.size-1):
			for j in range(1,self.size-1):
				if(self.maze[j][i][1] == [1]):
					start = Point(i*25 + 4, j*25 + 4)
					end = Point(i*25 + 21, j*25 + 21)
					sol = Rectangle(start, end)
					sol.setFill('orange')
					sol.draw(win)
				if(self.maze[j][i][1] == [2]):
					start = Point(i*25 + 6, j*25 + 6)
					end = Point(i*25 + 19, j*25 + 19)
					sol = Rectangle(start, end)
					sol.setFill('cyan')
					sol.draw(win)

				if(self.maze[j][i][1] == [3]):
					start = Point(i*25 + 4, j*25 + 4)
					end = Point(i*25 + 21, j*25 + 21)
					sol = Rectangle(start, end)
					sol.setFill('orange')
					sol.draw(win)

					start = Point(i*25 + 6, j*25 + 6)
					end = Point(i*25 + 19, j*25 + 19)
					sol = Rectangle(start, end)
					sol.setFill('cyan')
					sol.draw(win)
				

		#Draw initial position
		start = Point(int(self.start[0])*25 + 4, int(self.start[1])*25 + 4)
		end = Point(int(self.start[0])*25 + 21, int(self.start[1])*25 + 21)
		initial = Rectangle(start,end)
		initial.setFill('red')
		initial.draw(win)

		#Draw finial position
		start1 = Point(self.end[0]*25 + 4, self.end[1]*25 + 4)
		end1 = Point(self.end[0] *25 + 21, self.end[1]*25 + 21)
		last = Rectangle(start1,end1)
		last.setFill('green')
		last.draw(win)

		#Draw Key
		start2 = Point(self.key[0]*25 + 4, self.key[1]*25 + 4)
		end2 = Point(self.key[0] *25 + 21, self.key[1]*25 + 21)
		key = Rectangle(start2,end2)
		key.setFill('yellow')
		key.draw(win)

		#Keep Window open till the close button is pressed
		win.mainloop()



def main(n):
	#n = eval(input("Enter a maze size: "))
	#n = 25
	#Increases recursion limit for larger mazes so that the explore function will not fail
	sys.setrecursionlimit(20000)
	myMaze = Maze(n)
	myMaze.generate()

	#Find a solution from self.start to self.end
	#Startx, Starty, endX, endY
	myMaze.explore(myMaze.start[0],myMaze.start[1],myMaze.key[0],myMaze.key[1])

	#Copy stack to draw it in different colour
	stack1 = myMaze.cellStack
	myMaze.setSolution(stack1, [1])

	#Add a key
	"""To add a key self.cellStack needs to be reset, and start point needs
	to be the key"""
	#Reset cellStack
	myMaze.cellStack = []

	#Clear backtrack
	#Set Outer Border
	for i in range(1,n+1): #y value
		for j in range(1,n+1): #x value
			#At the top row
			myMaze.maze[j][i][0] = [0]

	#Find a solution from self.start to self.end
	myMaze.explore(myMaze.key[0],myMaze.key[1],myMaze.end[0],myMaze.end[1])
	#print(myMaze.cellStack)

	#Set solution in self.maze using self.cellStack
	myMaze.setSolution(myMaze.cellStack,[2])

	#Legend for different colours on the maze
	print("INITIAL POSITION: RED at", myMaze.start, "\nKEY: YELLOW at", myMaze.key,"\nFINAL POSTION: GREEN at", myMaze.end,"\nSTART TO KEY: ORANGE\nKEY TO FINAL: CYAN")
	print("Start to Key:", stack1 + [myMaze.key])
	print("Key to End:", myMaze.cellStack+[myMaze.end])

	myMaze.draw()

main(35)