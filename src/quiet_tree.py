import tkinter as tk
import tkinter.ttk as ttk
import os

class FileTree(tk.Toplevel):
	def __init__(self, master, **kwargs):
		super().__init__(**kwargs)

		self.style = ttk.Style()
		self.theme = self.style.theme_use('clam')
		self.geometry('200x400')
		self.title('File Tree')
		self.transient(master)
		self.tree=ttk.Treeview(
			self,
			height=20,
			selectmode='browse',
			show='tree',
			style=self.theme)
		self.minsize(200,125)
		self.maxsize(500, 400)

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
					folder_name=self.tree.insert(location, count, text=folder)
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
				self.tree.insert(location, count + summ, text=file)
			summ += 1

		folder_mania(master.dirname)
		self.tree.pack(side=tk.TOP,fill=tk.BOTH)
