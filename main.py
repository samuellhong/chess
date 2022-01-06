'''
Samuel Hong
Chess
Nov 24, 2020
'''

import tkinter as tk
import numpy as np
import pieces
from PIL import ImageTk, Image
from tkinter.scrolledtext import ScrolledText
import time


class board(object):

	def __init__(self):

		self.width = 8
		self.height = 8
		self.b1 = [] ##board where each spot either has a piece or blank piece
		self.imagelist = [] ##every turn create new list of images
		self.piecelist = []	##every turn create new list of pieces
		self.current_places = [] ##the list of current spaces a piece can traverse
		self.turn = 1 ##which player turn
		self.player1check = False
		self.player2check = False
		self.player1checkmate = False
		self.player2checkmate = False
		size = 100 ##length/width of each square
		for i in range(self.width):
			temp  = []
			for j in range(self.height):
				temp.append(pieces.piece(0,(i,j)))
			self.b1.append(temp)

		self.addStartRow(1,0)
		self.addStartRow(2,self.width-1)

		for i in range(self.width):
			self.b1[1][i] = pieces.pawn(1,(1,i),"P")
			self.b1[6][i] = pieces.pawn(2,(6,i),"P")

		self.window = tk.Tk()
		self.window.title("CHESS")
		self.window.geometry("800x900")
		self.window.resizable(0,0)
		self.b = tk.Canvas(self.window, width = 8*size, height = 8*size)
		self.b.pack(pady=0)
		self.backgroundlist = []
		
			
		color = 'white'
		for y in range(self.width):
			temp = []
			for x in range(self.height):
				x1 = x*size
				y1 = y*size
				x2 = x1+size
				y2 = y1+size
				sq = self.b.create_rectangle((x1,y1,x2,y2),fill = "white")
				temp.append(sq)

			self.backgroundlist.append(temp)
		self.draw_background()
		self.textlog = ScrolledText(self.window,width = 8*size, height = size,background = 'white',fg='black',font=("Helvetica", 20))
		self.textlog.pack(side = tk.BOTTOM )
		text = ""
		text += time.strftime("%H:%M:%S")
		self.textlog.insert('1.0',text+': Start Game (Player 1 Turn)\n')
		self.draw_board()


		self.window.mainloop()

	def print(self):
		temp = ""
		for i in range(8):
			for j in range(8):
				if self.b1[i][j].getId() == None:
					temp += "  "
				else:
					temp+= " " + self.b1[i][j].getId()
			temp += "\n"
		return temp

	def check_check(self,player):
		pass

	def check_checkmate(self,player):
		pass
	def draw_background(self):
		color = 'white'
		for y in range(self.width):
			temp = []
			for x in range(self.height):

				self.b.itemconfig(self.backgroundlist[y][x],fill=color)
				if color == 'white':
					color = 'grey'
				else:
					color = 'white'
			self.backgroundlist.append(temp)
			if color == 'white':
				color = 'grey'
			else:
				color = 'white'

	def draw_board(self):
		print(self.print())
		self.piecelist = []
		self.imagelist = []
		self.current_places = []
		self.draw_background()
		list_counter = 0
		for y in range(self.height):
			for x in range(self.width):
				status = True
				if(self.b1[y][x].getId() == 'R'):
					name = "pieces/rook"
				elif(self.b1[y][x].getId() == 'B'):
					name = "pieces/bishop"
				elif(self.b1[y][x].getId() == 'N'):
					name = "pieces/knight"
				elif(self.b1[y][x].getId() == 'K'):
					name = "pieces/king"
				elif(self.b1[y][x].getId() == 'Q'):
					name = "pieces/queen"
				elif(self.b1[y][x].getId() == 'P'):
					name = "pieces/pawn"
				else:
					status = False

				if status:
					if(self.b1[y][x].getColor() == "black"):
						name+="b.png"
					else:
						name+="w.png"
					self.piecelist.append(self.b1[y][x])
					list_counter+=1
					self.imagelist.append(ImageTk.PhotoImage(Image.open(name).resize((100,100))))
					t_x = self.b1[y][x].getPosition()[1]
					t_y = self.b1[y][x].getPosition()[0]
					my_image = self.b.create_image(50+100*t_x, 50+100*t_y, image=self.imagelist[list_counter-1]) 
					if(self.b1[y][x].getColor() == "black" and self.turn == 2):
						self.b.tag_bind(my_image,'<B1-Motion>', lambda event, i= name,x=list_counter-1: self.move(event,i,x))
						self.b.tag_bind(my_image, '<ButtonRelease-1>',lambda event, i= name,x=list_counter-1: self.drop(event,i,x))
					if(self.b1[y][x].getColor() == "white" and self.turn == 1):
						self.b.tag_bind(my_image,'<B1-Motion>', lambda event, i= name,x=list_counter-1: self.move(event,i,x))
						self.b.tag_bind(my_image, '<ButtonRelease-1>',lambda event, i= name,x=list_counter-1: self.drop(event,i,x))
		

	def move(self,e,i,x):

		self.imagelist[x] = ImageTk.PhotoImage(Image.open(i).resize((100,100)))
		my_image = self.b.create_image(e.x, e.y, image=self.imagelist[x]) 


		if not (self.player2check or self.player1check):
			start = self.piecelist[x].getPosition()
			
			if(self.piecelist[x].getId() == "P"):
				pawnc = self.piecelist[x].capturable()
				for j in range(len(pawnc)):
					if self.b1[pawnc[j][0]][pawnc[j][1]].getId() != None and self.b1[pawnc[j][0]][pawnc[j][1]].getColor() != self.piecelist[x].getColor():
						self.b.itemconfig(self.backgroundlist[pawnc[j][0]][pawnc[j][1]],fill='red')
						self.current_places.append((pawnc[j][0],pawnc[j][1]))

			spaces = self.piecelist[x].moveablespaces(self.b1)
			for i in range(len(spaces)):
				x1 = spaces[i][1]*100
				y1 = spaces[i][0]*100
				x2 = x1+100
				y2 = y1+100
				if(self.piecelist[x].getId() == "P"):
					if self.b1[spaces[i][0]][spaces[i][1]].getId() == None:
						self.b.itemconfig(self.backgroundlist[spaces[i][0]][spaces[i][1]],fill='green')
						self.current_places.append((spaces[i][0],spaces[i][1]))

				elif(self.b1[spaces[i][0]][spaces[i][1]].getId() == None):
					
					self.b.itemconfig(self.backgroundlist[spaces[i][0]][spaces[i][1]],fill='green')
					self.current_places.append((spaces[i][0],spaces[i][1]))

				elif(self.b1[spaces[i][0]][spaces[i][1]].getId() != None and self.b1[spaces[i][0]][spaces[i][1]].getColor() != self.piecelist[x].getColor()):
					self.b.itemconfig(self.backgroundlist[spaces[i][0]][spaces[i][1]],fill='red')
					self.current_places.append((spaces[i][0],spaces[i][1]))

		else:
			start = self.piecelist[x].getPosition()
			spaces = self.piecelist[x].moveablespaces(self.b1)
			if(self.piecelist[x].getId() == "K"):
				for i in range(len(spaces)):
					x1 = spaces[i][1]*100
					y1 = spaces[i][0]*100
					x2 = x1+100
					y2 = y1+100
					self.current_places.append((spaces[i][0],spaces[i][1]))

		

	def drop(self,e,i,x):
		self.imagelist[x] = ImageTk.PhotoImage(Image.open(i).resize((100,100)))

		start = self.piecelist[x].getPosition()
		x1 = int(e.y/100)
		y = int(e.x/100)
		if((x1,y) in self.current_places):
			self.piecelist[x].move(x1,y)
			self.b1[x1][y] = self.piecelist[x]
			self.b1[start[0]][start[1]] = pieces.piece(0,(start[0],start[1]))
			my_image = self.b.create_image(e.x-(e.x%100)+50, e.y-(e.y%100)+50, image=self.imagelist[x]) 
			text = ""
			text += time.strftime("%H:%M:%S")

			check_pieces = self.piecelist[x].moveablespaces(self.b1)
			print(self.b1[0][0].getId())
			for i in check_pieces:
				if self.b1[i[0]][i[1]].getId() == 'K' and self.piecelist[x].getPlayer() != self.b1[i[0]][i[1]].getPlayer():
					self.textlog.insert('1.0',text+': Check\n')
					if self.turn == 1:
						self.player2check = True
					else:
						self.player1check = True
					break		

			if self.turn == 1:
				self.turn = 2
				self.textlog.insert('1.0',text+': Player 2 Turn\n')
			else:
				self.turn = 1
				self.textlog.insert('1.0',text+': Player 1 Turn\n')


		else:
			my_image = self.b.create_image((start[0]*100)+50, (start[1]*100)+50, image=self.imagelist[x]) 

		print("Dropped", str(self.piecelist[x].getId()),"at:",x1,":",y)
		
		
		self.draw_board()

	def addStartRow(self,player,i):
		self.b1[i][0] = pieces.rook(player,(i,0),"R")
		self.b1[i][1] = pieces.knight(player,(i,1),"N")
		self.b1[i][2] = pieces.bishop(player,(i,2),"B")
		self.b1[i][3] = pieces.king(player,(i,3),"K")
		self.b1[i][4] = pieces.queen(player,(i,4),"Q")
		self.b1[i][5] = pieces.bishop(player,(i,5),"B")
		self.b1[i][6] = pieces.knight(player,(i,6),"N")
		self.b1[i][7] = pieces.rook(player,(i,7),"R")


def main():

	game = board()



if __name__ == "__main__":
	main()