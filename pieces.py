from tkinter import *
from PIL import ImageTk, Image

class piece(object):
	def __init__(self,player,position,pieceId=None):
		self.player = player
		self.color = "black"
		self.player = player
		if player == 1:
			self.color = "white"
		if pieceId == None:
			self.color = "grey"
		self.id = pieceId
		self.position = position
	def getPlayer(self):
		return self.player

	def getId(self):
		return self.id

	def getColor(self):
		return self.color

	def getPosition(self):
		return self.position

	def move(self,x,y):
		self.position = (x,y)


class pawn(piece):

	def __init__(self,player,position,pieceId):
		super().__init__(player,position,pieceId)
		self.value = 1


	def moveablespaces(self,b1):
		spaces = []
		if self.color == "white":
			for i in range(1,3):
				if(b1[self.position[0]+i][self.position[1]].getId()!= None):
					break
				else:
					spaces.append((self.position[0]+i,self.position[1]))
			
		if self.color == "black":
			for i in range(1,3):
				if(b1[self.position[0]-i][self.position[1]].getId()!= None):
					break
				else:
					spaces.append((self.position[0]-i,self.position[1]))

		return spaces

	def capturable(self):
		spaces = []
		if self.color == "white":
			if self.position[0]+1 <= 7 and self.position[1]+1 <= 7:
				spaces.append((self.position[0]+1,self.position[1]+1))
			if self.position[0]+1<= 7 and self.position[1]-1 >=0:
				spaces.append((self.position[0]+1,self.position[1]-1))
		if self.color == "black":
			if self.position[0]-1 >= 0 and self.position[1]+1 <= 7:
				spaces.append((self.position[0]-1,self.position[1]+1))
			if self.position[1]-1 >= 0 and  self.position[0]-1 >= 0:
				spaces.append((self.position[0]-1,self.position[1]-1))
		return spaces

class knight(piece):

	def __init__(self,player,position,pieceId):
		super().__init__(player,position,pieceId)
		self.value = 3

	def moveablespaces(self,b1):
		spaces = []
		t = [1,2,-1,-2,1,2,-1,-2]
		s = [2,1,2,1,-2,-1,-2,-1]
		for i in range(len(t)):
			if self.position[0]+t[i]>=0 and self.position[0]+t[i] <=7 and self.position[1]+s[i] >=0 and self.position[1]+s[i]<=7:
				spaces.append((self.position[0]+t[i],self.position[1]+s[i]))
		return spaces

class rook(piece):

	def __init__(self,player,position,pieceId):
		super().__init__(player,position,pieceId)
		self.value = 5

	

	def moveablespaces(self,b1):
		spaces = []
		## Go Vertically positive direction
		for i in range(self.position[0]+1,8):
			if b1[i][self.position[1]].getId() != None:
				if b1[i][self.position[1]].getColor() == self.color:
					break
				else:
					spaces.append((i,self.position[1]))
					break
			else:
				spaces.append((i,self.position[1]))

		## Go Vertically negative direction
		for i in range(self.position[0]-1,-1,-1):
			if b1[i][self.position[1]].getId() != None:
				if b1[i][self.position[1]].getColor() == self.color:
					break
				else:
					spaces.append((i,self.position[1]))
					break
			else:
				spaces.append((i,self.position[1]))


		## Go Horizontally positive direction
		for j in range(self.position[1]+1,8):
			if b1[self.position[0]][j].getId() != None:
				if b1[self.position[0]][j].getColor() == self.color:
					break
				else:
					spaces.append((self.position[0],j))
					break
			else:
				spaces.append((self.position[0],j))

		## Go Horizontally negative direction
		for j in range(self.position[1]-1,-1,-1):
			if b1[self.position[0]][j].getId() != None:
				if b1[self.position[0]][j].getColor() == self.color:
					break
				else:
					spaces.append((self.position[0],j))
					break
			else:
				spaces.append((self.position[0],j))
		return spaces

class bishop(piece):

	def __init__(self,player,position,pieceId):
		super().__init__(player,position,pieceId)
		self.value = 3

	def moveablespaces(self,b1):
		spaces = []

		## SE direction
		for i in range(1,8):
			if self.position[0]+i<= 7 and self.position[1]+i<=7:
				if b1[self.position[0]+i][self.position[1]+i].getId() != None:
					if b1[self.position[0]+i][self.position[1]+i].getColor() == self.color:
						break
					else:
						spaces.append((self.position[0]+i,self.position[1]+i))
						break
				else:
					spaces.append((self.position[0]+i,self.position[1]+i))

		## NW direction
		for i in range(1,8):
			if self.position[0]-i>= 0 and self.position[1]-i>=0:
				if b1[self.position[0]-i][self.position[1]-i].getId() != None:
					if b1[self.position[0]-i][self.position[1]-i].getColor() == self.color:
						break
					else:
						spaces.append((self.position[0]-i,self.position[1]-i))
						break
				else:
					spaces.append((self.position[0]-i,self.position[1]-i))
		#SW direction
		for i in range(1,8):
			if self.position[0]+i<= 7 and self.position[1]-i>=0:
				if b1[self.position[0]+i][self.position[1]-i].getId() != None:
					if b1[self.position[0]-i][self.position[1]-i].getColor() == self.color:
						break
					else:
						spaces.append((self.position[0]+i,self.position[1]-i))
						break
				else:
					spaces.append((self.position[0]+i,self.position[1]-i))
		#NE direction
		for i in range(1,8):
			if self.position[0]-i>= 0 and self.position[1]+i<=7:
				if b1[self.position[0]-i][self.position[1]+i].getId() != None:
					if b1[self.position[0]-i][self.position[1]+i].getColor() == self.color:
						break
					else:
						spaces.append((self.position[0]-i,self.position[1]+i))
						break
				else:
					spaces.append((self.position[0]-i,self.position[1]+i))
		

		return spaces

class queen(piece):

	def __init__(self,player,position,pieceId):
		super().__init__(player,position,pieceId)
		self.value = 9

	def moveablespaces(self,b1):

		spaces = []

		## SE direction
		for i in range(1,8):
			if self.position[0]+i<= 7 and self.position[1]+i<=7:
				if b1[self.position[0]+i][self.position[1]+i].getId() != None:
					if b1[self.position[0]+i][self.position[1]+i].getColor() == self.color:
						break
					else:
						spaces.append((self.position[0]+i,self.position[1]+i))
						break
				else:
					spaces.append((self.position[0]+i,self.position[1]+i))

		## NW direction
		for i in range(1,8):
			if self.position[0]-i>= 0 and self.position[1]-i>=0:
				if b1[self.position[0]-i][self.position[1]-i].getId() != None:
					if b1[self.position[0]-i][self.position[1]-i].getColor() == self.color:
						break
					else:
						spaces.append((self.position[0]-i,self.position[1]-i))
						break
				else:
					spaces.append((self.position[0]-i,self.position[1]-i))
		#SW direction
		for i in range(1,8):
			if self.position[0]+i<= 7 and self.position[1]-i>=0:
				if b1[self.position[0]+i][self.position[1]-i].getId() != None:
					if b1[self.position[0]-i][self.position[1]-i].getColor() == self.color:
						break
					else:
						spaces.append((self.position[0]+i,self.position[1]-i))
						break
				else:
					spaces.append((self.position[0]+i,self.position[1]-i))
		#NE direction
		for i in range(1,8):
			if self.position[0]-i>= 0 and self.position[1]+i<=7:
				if b1[self.position[0]-i][self.position[1]+i].getId() != None:
					if b1[self.position[0]-i][self.position[1]+i].getColor() == self.color:
						break
					else:
						spaces.append((self.position[0]-i,self.position[1]+i))
						break
				else:
					spaces.append((self.position[0]-i,self.position[1]+i))

		for i in range(self.position[0]+1,8):
			if b1[i][self.position[1]].getId() != None:
				if b1[i][self.position[1]].getColor() == self.color:
					break
				else:
					spaces.append((i,self.position[1]))
					break
			else:
				spaces.append((i,self.position[1]))

		## Go Vertically negative direction
		for i in range(self.position[0]-1,-1,-1):
			if b1[i][self.position[1]].getId() != None:
				if b1[i][self.position[1]].getColor() == self.color:
					break
				else:
					spaces.append((i,self.position[1]))
					break
			else:
				spaces.append((i,self.position[1]))


		## Go Horizontally positive direction
		for j in range(self.position[1]+1,8):
			if b1[self.position[0]][j].getId() != None:
				if b1[self.position[0]][j].getColor() == self.color:
					break
				else:
					spaces.append((self.position[0],j))
					break
			else:
				spaces.append((self.position[0],j))

		## Go Horizontally negative direction
		for j in range(self.position[1]-1,-1,-1):
			if b1[self.position[0]][j].getId() != None:
				if b1[self.position[0]][j].getColor() == self.color:
					break
				else:
					spaces.append((self.position[0],j))
					break
			else:
				spaces.append((self.position[0],j))
		return spaces

class king(piece):

	def __init__(self,player,position,pieceId):
		super().__init__(player,position,pieceId)
		self.can_castle = True
		self.value = 7


	def move(self,x,y):
		self.position = (x,y)
		self.can_castle = False

	def moveablespaces(self,b1):
		spaces = []
		t = [1,1,1,-1,-1,-1,0,0]
		s = [0,1,-1,0,1,-1,1,-1]
		for i in range(len(t)):
			if self.position[0]+t[i]>=0 and self.position[0]+t[i]<=7 and self.position[1]+s[i]>=0 and self.position[1]+s[i]<=7:
				spaces.append((self.position[0]+t[i],self.position[1]+s[i]))
		return spaces












