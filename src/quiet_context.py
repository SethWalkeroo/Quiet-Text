import tkinter as tk
import tkinter.font as tk_font
import os

class ContextMenu(tk.Listbox):

    def __init__(self, parent, *args, **kwargs):
        tk.Listbox.__init__(self, parent, *args, **kwargs)

        self.settings = parent.loader.load_settings_data()
        self.font_family = self.settings['font_family']
        self.parent = parent

        # setting tk.RIGHT click menu bar
        self.right_click_menu = tk.Menu(parent,
                                        font=self.font_family,
                                        fg='#d5c4a1',
                                        bg='#2e2724',
                                        activebackground='#9c8383',
                                        bd=0,
                                        tearoff=0)

        self.right_click_menu.add_command(label='Cut',
                                          accelerator='Ctrl+X',
                                          command=self.cut)

        self.right_click_menu.add_command(label='Copy',
                                          accelerator='Ctrl+C',
                                          command=self.copy)

        self.right_click_menu.add_command(label='Paste',
                                          accelerator='Ctrl+V',
                                          command=self.paste)

        self.right_click_menu.add_command(label='Bold',
                                          accelerator='Ctrl+B',
                                          command=self.bold)

        self.right_click_menu.add_command(label='Highlight',
                                          accelerator='Ctrl+H',
                                          command=self.hightlight)

    def popup(self, event):
        try:
            self.right_click_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.right_click_menu.grab_release()

            # shortcut keys that the editor supports
    def copy(self, event=None):
        try:
            self.parent.textarea.clipboard_clear()
            text=self.parent.textarea.get("sel.first", "sel.last")
            self.parent.textarea.clipboard_append(text)
        except tk.TclError:
            pass

    def cut(self,event=None):
        try:
            self.copy()
            self.parent.textarea.delete("sel.first", "sel.last")
        except tk.TclError:
            pass

    def paste(self, *args):
        try:
            text = self.parent.textarea.selection_get(selection='CLIPBOARD')
            self.parent.syntax_highlighter.initial_highlight()
        except tk.TclError:
            pass
        return 'break'

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
                        self.textarea.tag_remove("bold", "sel.first", "sel.last")
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
                    self.parent.textarea.tag_config(f"highlight_{new_color}", font = highlight_font, foreground = "black", background = new_color)
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

