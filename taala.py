#taala

from Tkinter import *
import threading
import time
import pygame

class BeatThread(threading.Thread):
	def __init__(self, tempo, playframe):
		threading.Thread.__init__(self)
		self.stopflag = False
		self.tempo = int(tempo)
		self.playframe = playframe
		
	def run(self):
		while not self.stopflag:
			self.playframe.beat()
			time.sleep(float(60)/ self.tempo)
			
	def setStopFlag(self):
		self.stopflag = True

class Tempo(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		
		self.button = Button(self, text="Tempo")
		self.button.pack(side=LEFT)
		
		self.plus = Button(self, text="+", command=self.increase)
		self.plus.pack(side=LEFT)
		
		self.minus = Button(self, text="-", command=self.decrease)
		self.minus.pack(side=LEFT)
		
		self.tempo = StringVar()
		self.tempo.set(40)
		
		self.entry = Entry(self, textvariable=self.tempo)
		self.entry.pack(side=TOP)
		
	def increase(self):
		self.tempo.set(int(self.tempo.get()) + 1)
	
	def decrease(self):
		self.tempo.set(int(self.tempo.get()) - 1)
		
class Start(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		
		self.button = Button(self, text="Start")
		self.button.pack()	
			
class Stop(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		
		self.button = Button(self, text="Stop")
		self.button.pack()		
		
class About(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		
		self.button = Button(self, text="Start")
		self.button.pack()				
		
class MenuFrame(Frame):
	def __init__(self, parent, app):
		Frame.__init__(self, parent)
		
		self.app = app
		
		self.taalas = ["Dhruva", "Matya", "Rupaka", "Jhampe", "Triputa", "Atta", "Eka"]
		self.jatis = ["Tishra", "Chatushra", "Khanda", "Mishra", "Sankeerna"]
		
		self.selectedTaala = IntVar()
		self.selectedJati = IntVar()
		
		self.options = Frame(self)
		self.options.pack()
		
		self.taalaOption = Frame(self.options)
		self.taalaOption.pack(side=LEFT)
		
		for t in self.taalas:
			Radiobutton(self.taalaOption, variable=self.selectedTaala, text=t, value=t, indicatoron=False, command= lambda arg=t: self.app.optionClicked(arg)).pack(fill=BOTH)
		
		self.jatiOption = Frame(self.options)
		self.jatiOption.pack(side=LEFT)
		
		for j in self.jatis:
			b = Radiobutton(self.jatiOption, variable=self.selectedJati, text=j, value=j, indicatoron=False, command= lambda arg=j: self.app.optionClicked(arg)).pack(fill=BOTH)
		
		self.tempo = Tempo(self)
		self.tempo.pack(fill=BOTH)
		
		self.start = Start(self)
		self.start.button.configure(command = self.app.start)
		self.start.pack(fill=BOTH)
		
class PlayFrame(Frame):
	def __init__(self, parent, app):
		Frame.__init__(self, parent)
		
		self.app = app
		
		self.infoframe = Frame(parent)
		self.infoframe.pack()
		
		self.taala = StringVar()
		self.taalalabel = Label(self.infoframe, textvariable = self.taala)
		self.taalalabel.pack()
		
		self.jati = StringVar()
		self.jatilabel = Label(self.infoframe, textvariable = self.jati)
		self.jatilabel.pack()
		
		self.display = Frame(parent)
		
		self.beats = []
		
		for i in range(29):
			l = Label(self.display, text=" ", bg="red")
			self.beats.append( l )
		
		self.stop = Stop(self)
		self.stop.button.configure(command = self.app.stop)
		self.stop.pack(fill=BOTH)
		
	def showLabels(self, parts):
		self.currentbeats = []
		
		self.display.pack()
		print "Beats:", parts	
		numparts = sum(parts)
		
		_row = 0
		ctr = 0
		
		for num in parts:
			col = 0
			thisline = []
			
			for i in range(num):
				self.beats[ctr].grid(row=_row, column=col, padx=2, pady=2, ipadx=4, ipady=2)
				thisline.append( self.beats[ctr] )
				col += 1
				ctr += 1	
				
			self.currentbeats.append(thisline)
			_row += 1
			
		self.currentline = len( self.currentbeats ) - 1
		self.currentbeat = 0	
			
	def hideLabels(self):
		for b in self.beats:
			b.configure(bg = "red")
			b.grid_forget()
		self.display.pack_forget()		
		
	def beat(self):
		self.currentbeats[self.currentline][self.currentbeat].configure(bg = "red")
		
		self.currentbeat += 1
		if self.currentbeat == len( self.currentbeats[self.currentline] ):
			self.currentbeat = 0
			self.currentline += 1
			
		if self.currentline == len( self.currentbeats ):
			self.currentline = 0	
			
		self.currentbeats[self.currentline][self.currentbeat].configure(bg = "green")	
			
class Taala:
	def __init__(self, root):
		self.taalas = {"Dhruva":"ldll",
					   "Matya":"ldl",
					   "Rupaka":"dl",
					   "Jhampe":"lad",
					   "Triputa":"ldd",
					   "Atta":"lldd",
					   "Eka":"l"}
		
		self.jatis = {"Tishra":3,
					  "Chatushra":4,
					  "Khanda":5,
					  "Mishra":7,
					  "Sankeerna":9}
		
		self.selectedTaala = None
		self.selectedJati = None
		
		self.root = root
		
		self.ctr = Frame(self.root)
		self.ctr.pack()
		
		self.menuframe = MenuFrame(self.ctr, self)
		self.menuframe.pack_propagate(True)
		self.menuframe.pack()
		
		self.playframe = PlayFrame(self.ctr, self)
		
	def optionClicked(self, text):
		if text in self.taalas:
			self.selectedTaala = text
			print "Selected Taala:", text
			self.playframe.taala.set("Taala: " + text)
		else:
			self.selectedJati = text
			print "Selected Jati:", text
			self.playframe.jati.set("Jati: " + text)
		
	def start(self):
		if self.selectedTaala and self.selectedJati:
			print "Starting"	
			print "Tempo:", self.menuframe.tempo.tempo.get()
			
			self.playframe.pack()
			self.menuframe.pack_forget()
			
			parts = self.taalas[self.selectedTaala]
			nums = ()
			
			for part in parts:
				if part == "l":
					nums += (self.jatis[self.selectedJati] ,)
				elif part == "d":
					nums += (2,)
				else:	
					nums += (1,)
					
			self.playframe.showLabels(nums)	
			
			self.bt = BeatThread(self.menuframe.tempo.tempo.get(), self.playframe)
			self.bt.start()
			
		else:
			print "Taala, Jati not selected!"
		
	def stop(self):
		print "Stopping"	
		
		self.bt.setStopFlag()
		self.menuframe.pack()
		self.playframe.hideLabels()
		self.playframe.pack_forget()

def main():
	pygame.init()
	pygame.mixer.init()

	root = Tk()
	root.title("Taala")
	taala = Taala(root)
	root.mainloop()

if __name__ == "__main__":
    main()
