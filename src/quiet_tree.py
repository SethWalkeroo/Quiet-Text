import tkinter as tk
import tkinter.ttk as ttk
import os

class FileTree(tk.Toplevel):
	def __init__(self, master, **kwargs):
		tk.Toplevel.__init__(
     		self,
			bd=0,
			bg=master.bg_color,
			highlightbackground=master.bg_color)
		self.master = master
		self.font_specs = ('Droid Sans Fallback', 12)
		self.style = ttk.Style()
		self.style.theme_use('clam')
		self.style.configure(
      		'Treeview',
			font=self.font_specs,
            foreground=master.menu_fg,
            background=master.bg_color,
            highlightthickness=0,
            bd=0)
		self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
		self.geometry('200x400')
		self.title('File Tree')
		self.transient(master)
		self.tree=ttk.Treeview(
			self,
			height=20,
			selectmode='browse',
			show='tree',
			style='Treeview')
		self.minsize(200,125)
		self.maxsize(1000, 1000)
		#This may look like a horrible mess to you, but I am so f***ing proud of this function.
		#I understand this is kind of inefficient because it generates files for folders the user hasn't opened.
		def folder_mania(path, location=""):
			try:
				starting_content = os.listdir(master.dirname)
			except (NotADirectoryError, FileNotFoundError, PermissionError) as e:
				print(e)
			if path == master.dirname:
				location = ""
				files = [file for file in starting_content if '.' in file]
				folders = [folder for folder in starting_content if '.' not in folder]
			else:
				new_content = os.listdir(path)
				files = [file for file in new_content if '.' in file]
				folders = [folder for folder in new_content if '.' not in folder]
			summ = 0
			for count, folder in enumerate(folders, 1):
				if folder:
					folder_name=self.tree.insert(location, count, text=folder, values=[folder])
					new_path = path + '/' + folder
					try:
						if len(os.listdir(new_path)) > 0:
							folder_mania(new_path, location=folder_name)
					except (NotADirectoryError, FileNotFoundError):
						pass
					except PermissionError as e:
						print(e)
						break
			for count, file in enumerate(files, 1):
				adjusted_count = count + summ
				if adjusted_count % 2 == 0:
					tag = 'odd'
				else:
					tag = 'even'
				self.tree.insert(location, adjusted_count, text=file, tags=(tag,), values=[location])
			summ += 1

		folder_mania(master.dirname)
		self.tree_bindings()
		# self.tree.tag_configure('odd', background=self.master.bg_color)
		# self.tree.tag_configure('even', background=self.master.menubar_active_bg)
		self.tree.pack(side=tk.TOP,fill=tk.BOTH)
  
	def OnDoubleClick(self, event):
		self.master.filename = self.master.dirname
		item = self.tree.identify("item", event.x, event.y)
		folder_id = self.tree.parent(item)
		folder = ''
		while True:
			try:
				folder_path = self.tree.item(folder_id)["values"][0]
				folder = folder_path + '/' + folder
				folder_id = self.tree.parent(folder_id)
			except IndexError:
				break
		filename = self.tree.item(item)["text"]
		file_path = folder + filename if folder else filename
		if '.' in file_path:
			try:
				self.master.filename += '/' + file_path
				self.master.initialize_syntax()
			except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
				self.master.filename = os.getcwd()
		self.master.set_window_title(self.master.filename)

  
	def tree_bindings(self):
		self.tree.bind('<Double-Button-1>', self.OnDoubleClick)
