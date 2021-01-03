import tkinter as tk
import tkinter.font as tk_font
import os
from tkinter import ttk

class ContextMenu(tk.Listbox):

    def __init__(self, parent, *args, **kwargs):
        tk.Listbox.__init__(self, parent, *args, **kwargs)

        self.font_family = parent.font_family
        self.font_color = parent.menu_fg
        self.bg_color = parent.bg_color
        self.active_bg = parent.menubar_bg_active
        self.active_fg = parent.menubar_fg_active
        self.parent = parent

        self.changes = [""]
        self.steps = int()

        # setting tk.RIGHT click menu bar
        self.right_click_menu = tk.Menu(
            parent,
            font='DroidSansFallback',
            fg=self.font_color,
            bg=self.bg_color,
            activebackground=self.active_bg,
            activeforeground=self.active_fg,
            bd=0,
            tearoff=0)

        self.right_click_menu.add_command(
            label='Cut',
            command=self.parent.textarea.event_generate('<<Cut>>'))

        self.right_click_menu.add_command(
            label='Copy',
            command=self.parent.textarea.event_generate('<<Copy>>'))

        self.right_click_menu.add_command(
            label='Paste',
            command=self.parent.textarea.event_generate('<<Paste>>'))

        self.right_click_menu.add_command(
            label='Bold',
            command=self.bold)

        self.right_click_menu.add_command(
            label='Highlight',
            command=self.hightlight)

    def popup(self, event):
        try:
            self.right_click_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.right_click_menu.grab_release()

    def undo(self, event=None):
        if self.steps != 0:
            self.steps -= 1
            self.parent.textarea.delete(0, tk.END)
            self.parent.textarea.insert(tk.END, self.changes[self.steps])

    def redo(self, event=None):
        if self.steps < len(self.changes):
            self.parent.textarea.delete(0, tk.END)
            self.parent.textarea.insert(tk.END, self.changes[self.steps])
            self.steps += 1

    def add_changes(self, event=None):
        if self.parent.textarea.get() != self.changes[-1]:
            self.changes.append(self.parent.textarea.get())
            self.steps += 1

    # Setting the selected text to be bold
    def bold(self, event=None):
        if self.parent.filename:
            try:
                if(os.path.splitext(self.parent.filename)[1][1:] == "txt"):
                    current_tags = self.parent.textarea.tag_names("sel.first")
                    bold_font = tk_font.Font(self.parent.textarea, self.parent.textarea.cget("font"))
                    bold_font.configure(weight = "bold")
                    self.parent.textarea.tag_config("bold", font = bold_font)
                    if "bold" in current_tags:
                        self.parent.textarea.tag_remove("bold", "sel.first", "sel.last")
                    else:
                        self.parent.textarea.tag_add("bold", "sel.first", "sel.last")
                else: 
                    self.parent.statusbar.update_status('no txt bold')
            except tk.TclError:
                pass
        else:
            self.parent.statusbar.update_status('no file')

    def hightlight(self, event=None):
        if self.parent.filename:
            try:
                if(os.path.splitext(self.parent.filename)[1][1:] == "txt"):
                    new_color = self.parent.menubar.open_color_picker()
                    current_tags = self.parent.textarea.tag_names("sel.first")
                    highlight_font = tk_font.Font(self.parent.textarea, self.parent.textarea.cget("font"))
                    self.parent.textarea.tag_config(
                        f"highlight_{new_color}",
                        font = highlight_font,
                        foreground = "black",
                        background = new_color)
                    if "highlight" in current_tags:
                        for tag in current_tags:
                            if "highlight" in tag:
                                print(tag)
                                self.parent.textarea.tag_remove(tag, "sel.first", "sel.last")
                    else:
                        self.parent.textarea.tag_add("highlight", "sel.first", "sel.last")
                        self.parent.textarea.tag_add(f"highlight_{new_color}","sel.first", "sel.last")
                else:
                    self.parent.statusbar.update_status('no txt high')
            except tk.TclError:
                pass
        else:
            self.parent.statusbar.update_status('no file')

