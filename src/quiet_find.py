import tkinter as tk
import tkinter.ttk as ttk


class FindWindow(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)

        self.master = master

        self.geometry('330x100')
        self.title('Find and Replace')
        self.transient(self.master)
        self.configure(bg=self.master.bg_color)
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.text_to_find = tk.StringVar()
        self.text_to_replace_with = tk.StringVar()

        top_frame = tk.Frame(self, bg=self.master.bg_color)
        middle_frame = tk.Frame(self, bg=self.master.bg_color)
        bottom_frame = tk.Frame(self, bg=self.master.bg_color)

        self.style.configure('editor.TLabel',
                background=self.master.bg_color,
                foreground='#ffffff')

        find_entry_label = ttk.Label(top_frame, text="Find: ", style="editor.TLabel")
        self.find_entry = ttk.Entry(top_frame, textvar=self.text_to_find)

        replace_entry_label = ttk.Label(middle_frame, text="Replace: ", style="editor.TLabel")
        self.replace_entry = ttk.Entry(middle_frame, textvar=self.text_to_replace_with)

        self.style.configure('editor.TButton',
                background=self.master.bg_color,
                foreground='#ffffff')

        self.style.map('editor.TButton',
                background=[('pressed', '#3e4037'), ('active', '#3e4037')])

        self.find_button = ttk.Button(bottom_frame, text="Find", command=self.on_find, style="editor.TButton")
        self.replace_button = ttk.Button(bottom_frame, text="Replace", command=self.on_replace, style="editor.TButton")
        self.cancel_button = ttk.Button(bottom_frame, text="Cancel", command=self.on_cancel, style="editor.TButton")

        find_entry_label.pack(side=tk.LEFT, padx=(0, 23))
        self.find_entry.pack(side=tk.LEFT, fill=tk.X, expand=1)

        replace_entry_label.pack(side=tk.LEFT, padx=(3, 0))
        self.replace_entry.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.find_button.pack(side=tk.LEFT, padx=(5, 0))
        self.replace_button.pack(side=tk.LEFT, padx=(5, 0))
        self.cancel_button.pack(side=tk.LEFT, padx=(5, 5))

        top_frame.pack(side=tk.TOP, expand=1, fill=tk.X, padx=34)
        middle_frame.pack(side=tk.TOP, expand=1, fill=tk.X, padx=30)
        bottom_frame.pack(side=tk.TOP, expand=1, fill=tk.X)

        self.find_entry.focus_force()

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        self.minsize(330, 100)

    def on_find(self):
        self.master.find(self.text_to_find.get())

    def on_replace(self):
        self.master.replace_text(self.text_to_find.get(), self.text_to_replace_with.get())

    def on_cancel(self):
        self.master.cancel_find()
        self.destroy()





