import tkinter as tk
import tkinter.ttk as ttk
import os
from quiet_loaders import QuietLoaders


class FindWindow(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.loader = QuietLoaders()
        self.geometry('260x100')
        self.minsize(260, 100)
        self.maxsize(260, 100)
        self.quiet_icon_path = self.loader.resource_path(
            os.path.join('data', 'q.png'))
        self.icon = tk.PhotoImage(file=self.quiet_icon_path)
        self.iconphoto(False, self.icon)
        self.title('Search and Replace')
        self.transient(master)
        self.configure(bg=master.bg_color)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.bg_color = master.bg_color
        self.fg_color = master.fg_color
        self.active_fg = master.active_fg
        self.active_bg = master.active_bg

        self.text_to_find = tk.StringVar()
        self.text_to_replace_with = tk.StringVar()

        top_frame = tk.Frame(self, bg=self.bg_color)
        middle_frame = tk.Frame(self, bg=self.bg_color)
        bottom_frame = tk.Frame(self, bg=self.bg_color)

        self.style.configure(
            'editor.TLabel',
             background=self.bg_color,
             foreground=self.fg_color,)

        find_entry_label = ttk.Label(top_frame, text="Search: ", style="editor.TLabel")
        self.find_entry = ttk.Entry(top_frame, textvar=self.text_to_find)

        replace_entry_label = ttk.Label(middle_frame, text="Replace: ", style="editor.TLabel")
        self.replace_entry = ttk.Entry(middle_frame, textvar=self.text_to_replace_with)

        self.style.configure('editor.TButton',
                background=self.bg_color,
                foreground=self.fg_color,
                activeforeground=self.active_fg)

        self.style.map('editor.TButton',
                background=[('pressed', self.active_fg), ('active', self.active_bg)])

        self.find_button = ttk.Button(bottom_frame, text="Search", command=self.on_find, style="editor.TButton")
        self.replace_button = ttk.Button(bottom_frame, text="Replace", command=self.on_replace, style="editor.TButton")
        self.cancel_button = ttk.Button(bottom_frame, text="Cancel", command=self.on_cancel, style="editor.TButton")

        find_entry_label.pack(side=tk.LEFT, padx=(5, 12))
        self.find_entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=(0, 5))

        replace_entry_label.pack(side=tk.LEFT, padx=(5, 5))
        self.replace_entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=(0, 5))

        self.find_button.pack(side=tk.LEFT, padx=(5, 0))
        self.replace_button.pack(side=tk.LEFT, padx=(5, 0))
        self.cancel_button.pack(side=tk.LEFT, padx=(5, 5))

        top_frame.pack(side=tk.TOP, expand=1, fill=tk.X, padx=0)
        middle_frame.pack(side=tk.TOP, expand=1, fill=tk.X, padx=0)
        bottom_frame.pack(side=tk.TOP, expand=1, fill=tk.X)

        self.find_entry.focus_force()

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def on_find(self):
        self.master.find(self.text_to_find.get())

    def on_replace(self):
        self.master.replace_text(self.text_to_find.get(), self.text_to_replace_with.get())

    def on_cancel(self):
        self.master.cancel_find()
        self.destroy()






