#!c:/SDK/Anaconda2/python.exe
import sys
if sys.version_info.major == 3:
	from tkinter import *
else:
	from Tkinter import * 
from PIL import Image, ImageTk, ImageFilter# , ImageEnhance
import os
from pydebugger.debug import debug
import glob

class Application(Frame):
	def __init__(self, master, title="ScreenShot Viewer", images_dir = "temp"):
		Frame.__init__(self, master)
		self.master = master
		if not title:
			title = image1
		if not title:
			title = "No Image"
		if title:
			master.iconbitmap(os.path.join(os.path.dirname(__file__), 'favicon.png'))
		else:
			master.iconbitmap(os.path.join(os.path.dirname(__file__), 'nofavicon.ico'))
		self.image = glob.glob(images_dir + "\*")
		debug(self_image = self.image)
		self.size = (0, 0)
		
		master.wm_title(title)
		self.pack()
		# self.createWidgets(image1)
		master.resizable(0,0)
		if self.image:
			self.showImage1()
			self.showNextButton()
		else:
			self.showNoImage(master)
		
		self.n = 0
		self.binder(master)
		
		self.first_center()
		self.center()

	def first_center(self, final_width=None, final_height=None):
		all_size_width = [self.size[0], 0, 0]
		all_size_height = [self.size[1], 0, 0]
		self.master.geometry("%sx%s+30+30"%(str(max(all_size_width)), str(max(all_size_height))))
		
	def center(self):
		"""
		centers a tkinter window
		:param win: the root or Toplevel window to center
		"""
		self.master.update_idletasks()
		width = self.master.winfo_width()
		frm_width = self.master.winfo_rootx() - self.master.winfo_x()
		win_width = width + 2 * frm_width
		height = self.master.winfo_height()
		titlebar_height = self.master.winfo_rooty() - self.master.winfo_y()
		win_height = height + titlebar_height + frm_width
		x = self.master.winfo_screenwidth() // 2 - win_width // 2
		y = self.master.winfo_screenheight() // 2 - win_height // 2
		self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
		self.master.deiconify()

	def quitX(self, event=None):
		self.destroy()
		sys.exit()

	def binder(self, master):
		master.bind("n", self.run)
		master.bind("p", self.previous)
		master.bind("q", self.quitX)

	def showNoImage(self, master):
		master.iconbitmap(os.path.join(os.path.dirname(__file__), 'nofavicon.ico'))
		self.label1 = Label(self, text="No Image", relief=SUNKEN, width=20, height=10, font='Consolas 28 bold')
		self.label1.grid(row=0, column=0, padx=5, pady=5, rowspan=10)

	def showImage1(self, event=None):
		img = Image.open(self.image[0])
		self.size = img.size
		debug(setsize = self.setSize(img))
		all_size_width = [self.setSize(img)[0], 0, 0]
		all_size_height = [self.setSize(img)[1], 0, 0]
		final_width = sum(all_size_width[:-1]) + 70
		final_height = sum(all_size_height[1:]) + 40
		self.first_center(final_width, final_height)
		
		self.photo2 = ImageTk.PhotoImage(img.convert("RGB"))
		self.label2 = Label(self, image=self.photo2)
		self.label2.grid(row=0, column=0, padx=5, pady=5, rowspan=10)

	def run(self, event = None):
		self.showImage()
		self.n += 1
		
	def previous(self, event = None):
		self.n = self.n - 2
		self.showImage()
		self.n += 1
		
	def setSize(self, im):
		screen_width = self.master.winfo_screenwidth()
		screen_height = self.master.winfo_screenheight()
		if screen_width < im.size[0]:
			x = screen_width / 1.1
			y = screen_height / 1.1
		else:
			x = im.size[0] /  1.03
			y = im.size[1] / 1.03
	
		im.thumbnail((x, y), Image.ANTIALIAS)
		return x, y
		
	def showImage(self):
		try:
			images = self.image[self.n]
			debug(images = images)
			if images:
				img = Image.open(images)
				self.size = img.size
				debug(self_size = self.size)
				all_size_width = [self.setSize(img)[0], 0, 0]
				all_size_height = [self.setSize(img)[1], 0, 0]
				final_width = sum(all_size_width) + 70
				final_height = sum(all_size_height) + 40
				debug(final_width = final_width)
				debug(final_height = final_height)
				self.first_center(final_width, final_height)
				self.photo2 = ImageTk.PhotoImage(img.convert("RGB"))
				self.label2 = Label(self, image=self.photo2)
				self.label2.grid(rowspan=1)		
				self.label2.grid(row=0, column=0, padx=5, pady=5, rowspan=10)
			else:
				self.showNoImage(self.master)
		except:
			self.showNoImage(self.master)
		self.center()

	def showNextButton(self):
		button5 = Button(self, text="Next", command=self.run)
		button5.grid(row=4, column= 2, sticky = N)

	def sharpen(self):
		img2 = self.img.filter(ImageFilter.SHARPEN)
		self.photo2 = ImageTk.PhotoImage(img2)
		self.label2 = Label(self, image=self.photo2)
		self.label2.grid(row=0, column=1, padx=5, pady=5, rowspan=10)

	def showOther(self, event=None):
		self.label2.grid(rowspan=1)
		img = Image.open(self.image2)
		self.photo2 = ImageTk.PhotoImage(img)
		self.label2 = Label(self, image=self.photo3)
		self.label2.grid(row=0, column=0, padx=5, pady=5, rowspan=10)
		
def center(toplevel):
	"""
	centers a tkinter window
	:param win: the root or Toplevel window to center
	"""

	toplevel.update_idletasks()
	width = toplevel.winfo_width()
	frm_width = toplevel.winfo_rootx() - toplevel.winfo_x()
	win_width = width + 2 * frm_width
	height = toplevel.winfo_height()
	titlebar_height = toplevel.winfo_rooty() - toplevel.winfo_y()
	win_height = height + titlebar_height + frm_width
	x = toplevel.winfo_screenwidth() // 2 - win_width // 2
	y = toplevel.winfo_screenheight() // 2 - win_height // 2
	toplevel.geometry('{}x{}+{}+{}'.format(width, height, x, y))
	toplevel.deiconify()

def main(images_dir):
	root = Tk()
	#root = Toplevel(root1)
	#root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
	center(root)
	c = Application(root, images_dir = images_dir)
	c.mainloop()

if __name__ == '__main__':
	main(sys.argv[1])
