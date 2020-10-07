import os
import tkinter as tk 
import tkinter.font as tk_font
import json
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser


class Menu(tk.Menu):
    # menu method and its initializatipn from settings.json
    def __init__(self, *args, **kwargs):
        with open('settings.json', 'r') as settings_json:
            settings = json.load(settings_json)
        super().__init__(bg=settings["menu_bg"],
                         activeforeground=settings['menu_active_fg'],
                         activebackground=settings['menu_active_bg'],
                         activeborderwidth=0,
                         *args, **kwargs)


class Menubar:

    # initialising the menu bar of editor
    def __init__(self, parent):
        self._parent = parent
        font_specs = ('Droid Sans Fallback', 12)

        # setting up basic features in menubar
        menubar = tk.Menu(parent.master, font=font_specs,
                          fg='#c9bebb', bg='#2e2724',
                          activebackground='#9c8383',
                          bd=0)

        parent.master.config(menu=menubar)
        self._menubar = menubar
        # adding features file dropdown in menubar
        file_dropdown = Menu(menubar, font=font_specs, tearoff=0)
        # new file creation feature
        file_dropdown.add_command(label='New File',
                                   accelerator='Ctrl+N',
                                   command=parent.new_file)
        # open file feature
        file_dropdown.add_command(label='Open File',
                                   accelerator='Ctrl+O',
                                   command=parent.open_file)
        # save file feature
        file_dropdown.add_command(label='Save',
                                   accelerator='Ctrl+S',
                                   command=parent.save)
        # Save as feature
        file_dropdown.add_command(label='Save As',
                                   accelerator='Ctrl+Shift+S',
                                   command=parent.save_as)
        # run file feature
        file_dropdown.add_command(label='Run File',
                                   accelerator='Ctrl+b',
                                   command=parent.run)
        # exit feature
        file_dropdown.add_separator()
        file_dropdown.add_command(label='Exit',
                                  command=parent.master.destroy)
        # adding featues to about dropdown in menubar
        about_dropdown = Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label='Release Notes',
                                   command=self.release_notes)
        # about command added
        about_dropdown.add_command(label='About',
                                   command=self.about_message)
        # adding featues to settings dropdown in menubar
        # Edit settings feature
        settings_dropdown = Menu(menubar, font=font_specs, tearoff=0)
        settings_dropdown.add_command(label='Edit Settings',
                                      command=parent.open_settings_file)
        # reset settings feature
        settings_dropdown.add_command(label='Reset Settings to Default',
                                      command=parent.reset_settings_file)

        # menubar add buttons
        menubar.add_cascade(label='File', menu=file_dropdown)
        menubar.add_cascade(label='Settings', menu=settings_dropdown)
        menubar.add_cascade(label='About', menu=about_dropdown)
        menubar.add_command(label='Hex Colors', command=self.open_color_picker)
        menubar.add_command(label='Quiet Mode', command=self.enter_quiet_mode)
        
        self.menu_fields = [field for field in (file_dropdown, about_dropdown, settings_dropdown)]

    # Settings reconfiguration function
    def reconfigure_settings(self):
        with open('settings.json', 'r') as settings_json:
            settings = json.load(settings_json)
        for field in self.menu_fields:
            field.configure(bg=settings['menu_bg'],
                            activeforeground=settings['menu_active_fg'],
                            activebackground=settings['menu_active_bg'],)

    # color to different text tye can be set here
    def open_color_picker(self):
        return colorchooser.askcolor(title='Hex Colors', initialcolor='white')[1]

    # quiet mode is defined here
    def enter_quiet_mode(self):
        self._parent.enter_quiet_mode()

    # hiding the menubar
    def hide_menu(self):
        empty_menu = tk.Menu(self._parent.master)
        self._parent.master.config(menu=empty_menu)

    # display the menubar
    def show_menu(self):
        self._parent.master.config(menu=self._menubar)

    # what to display on clicking about feature is defined here
    def about_message(self):
        box_title = 'About Quiet Text'
        box_message = 'A simple text editor for your Python needs.'
        messagebox.showinfo(box_title, box_message)

    def release_notes(self):
        box_title = 'Release Notes'
        box_message = 'Version 0.1 - Loud - this is the first version of Quiet Text'
        messagebox.showinfo(box_title, box_message)


class Statusbar:

    # initialising the status bar
    def __init__(self, parent):
        self._parent = parent

        # setting up the status bar
        font_specs = ('Droid Sans Fallback', 10)

        self.status = tk.StringVar()
        self.status.set('Quiet Text (v0.1)')

        label = tk.Label(parent.textarea, textvariable=self.status, fg='#c9bebb',
                         bg='#2e2724', anchor='sw', font=font_specs)
        label.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self._label = label

    # status update of the status bar
    def update_status(self, *args):
        if args[0] == 'saved':
            self.status.set('changes saved')
        elif args[0] == 'no file':
            self.status.set('Cannot run! No file selected.')
        else:
            self.status.set('Quiet Text (v0.1)')

    # hiding the status bar while in quiet mode
    def hide_status_bar(self):
        self._label.pack_forget()

    # display of the status bar
    def show_status_bar(self):
        self._label.pack(side=tk.BOTTOM, fill=tk.BOTH)


class QuietText:
    
    def __init__(self, master):
        master.title('untitled - Quiet Text')
        # defined size of the editer window
        master.geometry('1200x700')
        # defined editor basic bakground and looking
        master.tk_setPalette(background='#261e1b',
                     foreground='#c9bebb',
                     activeForeground='white',
                     activeBackground='#9c8383',)
        # start editor according to defined settings in settings.json
        with open('settings.json') as settings_json:
            settings = json.load(settings_json)

        self.text_font = settings['text_font']
        self.bg_color = settings['bg_color']
        self.text_color = settings['text_color']
        self.tab_size = settings['tab_size']
        self.font_style = tk_font.Font(family=self.text_font, size=settings['font_size'])
        
        self.master = master
        self.filename = None
        # defined editor scrollbar
        self.textarea = tk.Text(master, font=self.text_font)
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview,
                                   bg='#383030',troughcolor='#2e2724',
                                   bd=0, width=8, highlightthickness=0,
                                   activebackground='#8a7575')
        # configuring of the editor after scrolling
        self.textarea.configure(yscrollcommand=self.scroll.set,
                                bg=self.bg_color, fg=self.text_color,
                                wrap='word', spacing1=1, tabs=self.tab_size,
                                spacing3=1, selectbackground='#3d3430',
                                insertbackground='white', bd=0,
                                highlightthickness=0,
                                insertofftime=0, font=self.font_style,
                                undo=True, autoseparators=True, maxundo=-1)

        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)
        # setting right click menu bar
        self.right_click_menu = tk.Menu(master, font=self.text_font,
                                        fg='#c9bebb', bg='#2e2724',
                                        activebackground='#9c8383',
                                        bd=0, tearoff=0)

        self.right_click_menu.add_command(label='Cut',
                                          accelerator='Ctrl+X')
        self.right_click_menu.add_command(label='Copy',
                                          accelerator='Ctrl+C')
        self.right_click_menu.add_command(label='Paste',
                                          accelerator='Ctrl+V')

        self.bind_shortcuts()

    # editor basic settings can be altered here
    def reconfigure_settings(self, settings_path, overwrite=False):
            with open(settings_path, 'r') as settings_json:
                settings = json.load(settings_json)
            text_font = settings['text_font']
            bg_color = settings['bg_color']
            text_color = settings['text_color']
            tab_size = settings['tab_size']
            font_style = tk_font.Font(family=text_font, size=settings['font_size'])
            self.textarea.configure(font=font_style, bg=bg_color,
                                    fg=text_color, tabs=tab_size)
            if overwrite:
                MsgBox = tk.messagebox.askquestion('Reset Settings?',
                                                   'Are you sure you want to reset the editor settings to their default value?',
                                                   icon='warning')
                if MsgBox == 'yes':
                    with open('settings.json', 'w') as user_settings:
                        json.dump(settings, user_settings)
                else:
                    self.save('settings.json')

    # editor quiet mode calling which removes status bar and menu bar
    def enter_quiet_mode(self, *args):
        self.statusbar.hide_status_bar()
        self.menubar.hide_menu()

    # editor leaving quite enu to bring back status bar and menu bar
    def leave_quiet_mode(self, *args):
        self.statusbar.show_status_bar()
        self.menubar.show_menu()

    # setting up the editor title
    def set_window_title(self, name=None):
        if name:
            self.master.title(f'{name} - QuietText')
        else:
            self.master.title('Untitled - QuietText')

    # new file creating in the editor feature
    def new_file(self, *args):
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    # opening an existing file in the editor
    def open_file(self, *args):
        # various file types that editor can support
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

    # saving changes made in the file
    def save(self, *args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, 'w') as f:
                    f.write(textarea_content)
                self.statusbar.update_status('saved')
                if self.filename == 'settings.json':
                    self.reconfigure_settings(self.filename)
                    self.menubar.reconfigure_settings()
            except Exception as e:
                print(e)
        else:
            self.save_as()

    # saving file as a particular name
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

    # running the python file
    def run(self, *args):
        if self.filename:
            os.system(f"gnome-terminal -- python3.8 {self.filename}")
        else:
            self.statusbar.update_status('no file')

    # opens the main setting file of the editor
    def open_settings_file(self):
        self.filename = 'settings.json'
        self.textarea.delete(1.0, tk.END)
        with open(self.filename, 'r') as f:
            self.textarea.insert(1.0, f.read())
        self.set_window_title(name=self.filename)

    # reset the settings set by the user to the default settings
    def reset_settings_file(self):
        self.reconfigure_settings('settings-default.json', overwrite=True)

    # select all written text in the editor
    def select_all_text(self, *args):
        self.textarea.tag_add(tk.SEL, '1.0', tk.END)
        self.textarea.mark_set(tk.INSERT, '1.0')
        self.textarea.see(tk.INSERT)
        return 'break'

    # give hex colors to the file content for better understanding
    def apply_hex_color(self, key_event):
        new_color = self.menubar.open_color_picker()
        try:
            sel_start = self.textarea.index(tk.SEL_FIRST)
            sel_end = self.textarea.index(tk.SEL_LAST)
            self.textarea.delete(sel_start, sel_end)
            self.textarea.insert(sel_start, new_color)
        except tk.TclError:
            pass

    # Render the right click menu on right click
    def show_click_menu(self, key_event):
        try:
            self.right_click_menu.tk_popup(key_event.x_root, key_event.y_root)
        finally:
            self.right_click_menu.grab_release()

    # shortcut keys that the editor supports
    def bind_shortcuts(self, *args):
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
        self.textarea.bind('<Control-b>', self.run)
        self.textarea.bind('<Control-a>', self.select_all_text)
        self.textarea.bind('<Control-h>', self.apply_hex_color)
        self.textarea.bind('<Control-q>', self.enter_quiet_mode)
        self.textarea.bind('<Escape>', self.leave_quiet_mode)
        self.textarea.bind('<Key>', self.statusbar.update_status)
        self.textarea.bind('<Button-3>', self.show_click_menu)


if __name__ == '__main__':
    master = tk.Tk()
    qt = QuietText(master)
    master.mainloop()

