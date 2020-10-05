import os
import tkinter as tk 
import json
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser


class Menubar:
    
    def __init__(self, parent):
        self._parent = parent
        font_specs = ('Droid Sans Fallback', 12)

        menubar = tk.Menu(parent.master, font=font_specs,
                          fg='#c9bebb', bg='#2e2724',
                          activebackground='#9c8383',
                          bd=0)
        parent.master.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label='New File',
                                   accelerator='Ctrl+N',
                                   command=parent.new_file)
        file_dropdown.add_command(label='Open File',
                                   accelerator='Ctrl+O',
                                   command=parent.open_file)
        file_dropdown.add_command(label='Save',
                                   accelerator='Ctrl+S',
                                   command=parent.save)
        file_dropdown.add_command(label='Save As',
                                   accelerator='Ctrl+Shift+S',
                                   command=parent.save_as)
        file_dropdown.add_command(label='Run File',
                                   accelerator='Ctrl+b',
                                   command=parent.run)
        file_dropdown.add_separator()
        file_dropdown.add_command(label='Exit',
                                  command=parent.master.destroy)
        
        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label='Release Notes',
                                   command=self.release_notes)
        about_dropdown.add_command(label='About',
                                   command=self.about_message)
        
        menubar.add_cascade(label='File', menu=file_dropdown)
        menubar.add_command(label='Settings', command=parent.open_settings_file)
        menubar.add_cascade(label='About', menu=about_dropdown)
        menubar.add_command(label='Hex Colors', command=self.open_color_picker)
        menubar.add_command(label='Quiet Mode')

    def open_color_picker(self):
        return colorchooser.askcolor(title='Hex Colors', initialcolor='white')[1]

    def about_message(self):
        box_title = 'About QuietTxt'
        box_message = 'A simple text editor for your Python needs.'
        messagebox.showinfo(box_title, box_message)

    def release_notes(self):
        box_title = 'Release Notes'
        box_message = 'Version 0.1 - Loud - this is the first version of QuietTxt'
        messagebox.showinfo(box_title, box_message)


class Statusbar:

    def __init__(self, parent):

        font_specs = ('Droid Sans Fallback', 12)

        self.status = tk.StringVar()
        self.status.set('QuietTxt - v0.1 Loud')

        label = tk.Label(parent.textarea, textvariable=self.status, fg='#c9bebb',
                         bg='#2e2724', anchor='sw', font=font_specs)
        label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_status(self, *args):
        if args[0] == 'saved':
            self.status.set('Your file has been saved!')
        elif args[0] == 'no file':
            self.status.set('Cannot run! No file selected.')
        else:
            self.status.set('QuietTxt - v0.1 Loud')

class QuietTxt:
    
    def __init__(self, master, settings):
        master.title('untitled - QuietTxt')
        master.geometry('1200x700')
        self.text_font = settings['text_font']
        self.bg_color = settings['bg_color']
        self.text_color = settings['text_color']
        
        self.master = master
        self.filename = None
        
        self.textarea = tk.Text(master, font=self.text_font)
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview,
                                   bg='#383030',troughcolor='#2e2724',
                                   bd=0, widt=8, highlightthickness=0,
                                   activebackground='#8a7575')

        self.textarea.configure(yscrollcommand=self.scroll.set,
                                bg=self.bg_color, fg=self.text_color,
                                highlightcolor='#332b2b',
                                highlightbackground='#4a3a39',
                                wrap='word', spacing1=1,
                                spacing3=1, selectbackground='#9c8383',
                                insertbackground='white', bd=0,
                                insertofftime=0, font=self.text_font,
                                undo=True, autoseparators=True, maxundo=-1)

        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)

        self.bind_shortcuts()

    def set_window_title(self, name=None):
        if name:
            self.master.title(f'{name} - QuietTxt')
        else:
            self.master.title('Untitled - QuietTxt')
    
    def new_file(self, *args):
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()
        
    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension='.txt',
            filetypes=[('All Files', '*.*'),
                       ('Text Files', '*.txt'),
                       ('Python Scripts', '*.py'),
                       ('Markdown Documents', '*.md'),
                       ('Javascript Files', '*.js'),
                       ('HTML Documents', '*.html'),
                       ('CSS Documents', '*.css')])
        if self.filename:
            self.textarea.delete(1.0, tk.END)
            with open(self.filename, 'r') as f:
                self.textarea.insert(1.0, f.read())
            self.set_window_title(name=self.filename)
        
    def save(self, *args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, 'w') as f:
                    f.write(textarea_content)
                self.statusbar.update_status('saved')
                if self.filename == 'settings.json':
                    with open(self.filename, 'r') as settings_json:
                        settings = json.load(settings_json)
                        text_font = settings['text_font']
                        bg_color = settings['bg_color']
                        text_color = settings['text_color']
                        self.textarea.configure(font=text_font, bg=bg_color,
                                                fg=text_color)
            except Exception as e:
                print(e)
        else:
            self.save_as()
    
    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile='untitled.txt',
                defaultextension='.txt',
                filetypes=[('All Files', '*.*'),
                           ('Text Files', '*.txt'),
                           ('Python Scripts', '*.py'),
                           ('Markdown Documents', '*.md'),
                           ('Javascript Files', '*.js'),
                           ('HTML Documents', '*.js'),
                       ('CSS Documents', '*.css')])
            textarea_content = self.textarea.get(1.0, tk.END)
            with open(new_file, 'w') as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
            self.statusbar.update_status('saved')
        except Exception as e:
            print(e)

    def run(self, *args):
        if self.filename:
            os.system(f"gnome-terminal -- bash -c python3 {self.filename}; exec bash")
        else:
            self.statusbar.update_status('no file')

    def open_settings_file(self):
        self.filename = 'settings.json'
        self.textarea.delete(1.0, tk.END)
        with open(self.filename, 'r') as f:
            self.textarea.insert(1.0, f.read())
        self.set_window_title(name=self.filename)

    def select_all_text(self, *args):
        self.textarea.tag_add(tk.SEL, '1.0', tk.END)
        self.textarea.mark_set(tk.INSERT, '1.0')
        self.textarea.see(tk.INSERT)
        return 'break'

    def apply_hex_color(self, key_event):
        new_color = self.menubar.open_color_picker()
        try:
            sel_start = self.textarea.index(tk.SEL_FIRST)
            sel_end = self.textarea.index(tk.SEL_LAST)
            self.textarea.delete(sel_start, sel_end)
            self.textarea.insert(sel_start, new_color)
        except tk.TclError:
            pass

    def bind_shortcuts(self, *args):
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
        self.textarea.bind('<Control-b>', self.run)
        self.textarea.bind('<Control-a>', self.select_all_text)
        self.textarea.bind('<Control-h>', self.apply_hex_color)
        self.textarea.bind('<Key>', self.statusbar.update_status)


if __name__ == '__main__':
    master = tk.Tk()
    master.tk_setPalette(background='#261e1b',
                         foreground='white',
                         activeForeground='white',
                         activeBackground='#9c8383',)
    with open('settings.json') as settings_json:
        settings = json.load(settings_json)
    pt = QuietTxt(master, settings)
    master.mainloop()
