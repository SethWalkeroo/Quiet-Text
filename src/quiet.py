import os
import time
import yaml
import tkinter as tk 
import tkinter.font as tk_font
from tkinter import (filedialog, messagebox, colorchooser, END,
                    BOTH, LEFT, RIGHT, BOTTOM, Y, ttk)


class Menu(tk.Menu):
    # menu method and its initializatipn from settings.yaml
    def __init__(self, *args, **kwargs):
        with open('settings.yaml', 'r') as settings_yaml:
            settings = yaml.load(settings_yaml, Loader=yaml.FullLoader)
        super().__init__(bg=settings["menu_bg"],
                         activeforeground=settings['menu_active_fg'],
                         activebackground=settings['menu_active_bg'],
                         foreground='#d5c4a1',
                         activeborderwidth=0,
                         relief='sunken',
                         bd=0,
                         *args, **kwargs)


class Menubar:

    # initialising the menu bar of editor
    def __init__(self, parent):
        self._parent = parent
        font_specs = ('Droid Sans Fallback', 12)

        # setting up basic features in menubar
        menubar = tk.Menu(parent.master,
                          font=font_specs,
                          fg='#ebdbb2',
                          bg='#181816',
                          activeforeground='#d5c4a1',
                          activebackground='#38342b',
                          activeborderwidth=0,
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
                                   accelerator='Ctrl+Shift+S
                                   command=parent.save_as)
        # run file feature
        file_dropdown.add_command(label='Run File',
                                   accelerator='Ctrl+R',
                                   command=parent.run)
        # exit feature
        file_dropdown.add_separator()
        file_dropdown.add_command(label='Exit',
                                  command=parent.on_closing)
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

        view_dropdown = Menu(menubar, font=font_specs, tearoff=0)
        view_dropdown.add_command(label='Hide Menu Bar',
                                  command=self.hide_menu)
        view_dropdown.add_command(label='Hide Status Bar',
                                  command=parent.hide_status_bar)

        # menubar add buttons
        menubar.add_cascade(label='File', menu=file_dropdown)
        menubar.add_cascade(label='Settings', menu=settings_dropdown)
        menubar.add_cascade(label='View', menu=view_dropdown)
        menubar.add_command(label='Color Menu', command=self.open_color_picker)
        menubar.add_command(label='Quiet Mode', command=self.enter_quiet_mode)
        menubar.add_cascade(label='About', menu=about_dropdown)
        
        self.menu_fields = [field for field in (file_dropdown, about_dropdown, settings_dropdown)]

    # Settings reconfiguration function
    def reconfigure_settings(self):
        with open('settings.yaml', 'r') as settings_yaml:
            settings = yaml.load(settings_yaml, Loader=yaml.FullLoader)
        for field in self.menu_fields:
            field.configure(bg=settings['menu_bg'],
                            activeforeground=settings['menu_active_fg'],
                            activebackground=settings['menu_active_bg'],)

    # color to different text tye can be set here
    def open_color_picker(self):
        return colorchooser.askcolor(title='Color Menu', initialcolor='#d5c4a1')[1]

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
        box_message = 'A simple text editor for your Python and notetaking needs.'
        messagebox.showinfo(box_title, box_message)

    def release_notes(self):
        box_title = 'Release Notes'
        box_message = 'Version 0.1'
        messagebox.showinfo(box_title, box_message)


class Statusbar:

    # initialising the status bar
    def __init__(self, parent):
        self._parent = parent

        # setting up the status bar
        font_specs = ('Droid Sans Fallback', 10)

        self.status = tk.StringVar()

        label = tk.Label(parent.textarea,
                         textvariable=self.status,
                         fg='#fbf1c7',
                         bg='#38342b',
                         anchor='se',
                         font=font_specs)

        label.pack(side=BOTTOM)
        self._label = label

    # status update of the status bar
    def update_status(self, event):
        if event == 'saved':
            self.display_status_message('changes saved!', msg_type='save')
        elif event == 'no file run':
            self.display_status_message('Cannot run! No Python file selected.')
        elif event == 'no file':
            self.display_status_message('No file detected. Create or open a file.')
        elif event == 'no python':
            self.display_status_message('You can only run Python files.')
        elif event == 'no txt bold':
            self.display_status_message('You can only bold text in text files.')
        elif event == 'no txt high':
            self.display_status_message('You can only highlight text in text files.')
        elif event == 'quiet':
            self.display_status_message('You can leave quiet mode by pressing "escape"', msg_type='hint')
        else:
            self.hide_status_bar()

    def display_status_message(self, message, msg_type='error'):
        self.show_status_bar()
        self.status.set(message)
        if msg_type == 'save':
            self.save_color()
        elif msg_type == 'hint':
            self.hint_color()
        else:
            self.error_color()

    def error_color(self):
        self._label.config(bg='#522628')

    def save_color(self):
        self._label.config(bg='#47632b')

    def hint_color(self):
        self._label.config(bg='#38342b', fg='#d5c4a1')

    # hiding the status bar while in quiet mode
    def hide_status_bar(self):
        self._label.pack_forget()

    # display of the status bar
    def show_status_bar(self):
        self._label.pack(side=BOTTOM)

   
class TextLineNumbers(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self._text_font = parent.settings['font_family']
        self._parent = parent
        self.textwidget = parent.textarea

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete('all')
        self.config(width=(self._parent.font_size * 3))

        i = self.textwidget.index('@0,0')
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split('.')[0]
            self.create_text(2, y, anchor='nw',
                             text=linenum,
                             font=(self._text_font, self._parent.font_size),
                             fill='#d5c4a1')
            i = self.textwidget.index('%s+1line' % i)


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self.isControlPressed = False
        self._orig = self._w + '_orig'
        self.tk.call('rename', self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        try:
            cmd = (self._orig,) + args
            result = ''
            if not self.isControlPressed:
                # if command is not present, execute the event
                result = self.tk.call(cmd)
            else:
                # Suppress y-scroll and x-scroll when control is pressed
                if args[0:2] not in [('yview', 'scroll'), ('xview', 'scroll')]:
                    result = self.tk.call(cmd)
        except tk.TclError:
            result = ''

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ('insert', 'replace', 'delete') or 
            args[0:3] == ('mark', 'set', 'insert') or
            args[0:2] == ('xview', 'moveto') or
            args[0:2] == ('xview', 'scroll') or
            args[0:2] == ('yview', 'moveto') or
            args[0:2] == ('yview', 'scroll')
        ):
            self.event_generate('<<Change>>', when='tail')

        # return what the actual widget returned
        return result   


class QuietText(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        master.title('untitled - Quiet Text')
        # defined size of the editer window
        master.geometry('1920x1080')

        # defined editor basic bakground and looking
        master.tk_setPalette(background='#261e1b',
                             foreground='black',
                             activeForeground='white',
                             activeBackground='#9c8383',)

        # start editor according to defined settings in settings.yaml
        with open('settings.yaml') as settings_yaml:
            self.settings = yaml.load(settings_yaml, Loader=yaml.FullLoader)

        master.tk_setPalette(background='#181816', foreground='#8f3f71')

        self.font_family = self.settings['font_family']
        self.bg_color = self.settings['bg_color']
        self.font_color = self.settings['font_color']
        self.tab_size = self.settings['tab_size']
        self.font_size = int(self.settings['font_size'])
        self.top_spacing = self.settings['top_spacing']
        self.bottom_spacing = self.settings['bottom_spacing']
        self.padding_x = self.settings['padding_x']
        self.padding_y = self.settings['padding_y']
        self.insertion_blink = 300 if self.settings['insertion_blink'] else 0
        self.insertion_color = self.settings['insertion_color']
        self.tab_size_spaces = self.settings['tab_size']
        self.text_wrap = self.settings['text_wrap']

        self.font_style = tk_font.Font(family=self.font_family,
                                       size=self.settings['font_size'])

        #configuration of the file dialog text colors.
        self.style = ttk.Style(master)
        self.style.configure('TLabel', foreground='black')
        self.style.configure('TEntry', foreground='black')
        self.style.configure('TMenubutton', foreground='black')
        self.style.configure('TButton', foreground='black')

        self.master = master
        self.filename = None
                                
        self.textarea = CustomText(self)

        self.scrolly = tk.Scrollbar(master,
                                    command=self.textarea.yview,
                                    bg='#383030',
                                    troughcolor='#2e2724',
                                    bd=0,
                                    width=8,
                                    highlightthickness=0,
                                    activebackground='#8a7575',
                                    orient='vertical')

        self.scrollx = tk.Scrollbar(master,
                                    command=self.textarea.xview,
                                    bg='#383030',
                                    troughcolor='#2e2724',
                                    bd=0,
                                    width=8,
                                    highlightthickness=0,
                                    activebackground='#8a7575',
                                    orient='horizontal')

        self.textarea.configure(yscrollcommand=self.scrolly.set,
                                xscrollcommand=self.scrollx.set,
                                bg=self.bg_color,
                                fg=self.font_color,
                                wrap= self.text_wrap,
                                spacing1=self.top_spacing, 
                                spacing3=self.bottom_spacing,
                                selectbackground='#7a7666',
                                insertbackground=self.insertion_color,
                                insertofftime=self.insertion_blink,
                                bd=0,
                                highlightthickness=0,
                                font=self.font_family,
                                undo=True,
                                autoseparators=True,
                                maxundo=-1,
                                padx=self.padding_x,
                                pady=self.padding_y)

        #retrieving the font from the text area and setting a tab width
        self._font = tk_font.Font(font=self.textarea['font'])
        self._tab_width = self._font.measure(' ' * self.tab_size_spaces)
        self.textarea.config(tabs=(self._tab_width,))

        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)
        self.linenumbers = TextLineNumbers(self)

        self.linenumbers.attach(self.textarea)
        self.scrolly.pack(side=RIGHT, fill=Y)
        self.scrollx.pack(side=BOTTOM, fill=BOTH)
        self.linenumbers.pack(side=LEFT, fill=Y)
        self.textarea.pack(side=RIGHT, fill=BOTH, expand=True)

        # setting right click menu bar
        self.right_click_menu = tk.Menu(master,
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
                                          accelerator='Ctrl+G',
                                          command=self.hightlight)

        
        #calling function to bind hotkeys.
        self.bind_shortcuts()
        self.control_key = False


    def load_settings_data(self, settings_path):
        settings_path = settings_path
        with open(settings_path, 'r') as settings_yaml:
            _settings = yaml.load(settings_yaml, Loader=yaml.FullLoader)
            return _settings

    def store_settings_data(self, information):
        with open('settings.yaml', 'w') as user_settings:
            yaml.dump(information, user_settings)

    def clear_and_replace_textarea(self):
            self.textarea.delete(1.0, END)
            try:
                with open(self.filename, 'r') as f:
                    self.textarea.insert(1.0, f.read())
            except TypeError:
                pass

    #reconfigure the tab_width depending on changes.
    def set_new_tab_width(self, tab_spaces = 'default'):
        if tab_spaces == 'default':
            space_count = self.tab_size_spaces
        else:
            space_count = tab_spaces
        _font = tk_font.Font(font=self.textarea['font'])
        _tab_width = _font.measure(' ' * int(space_count))
        self.textarea.config(tabs=(_tab_width,))

    # editor basic settings can be altered here
    #function used to reload settings after the user changes in settings.yaml
    def reconfigure_settings(self, settings_path, overwrite=False):
            _settings = self.load_settings_data(settings_path)
            font_family = _settings['font_family']
            bg_color = _settings['bg_color']
            font_color = _settings['font_color']
            top_spacing = _settings['top_spacing']
            bottom_spacing = _settings['bottom_spacing']
            insertion_blink = 300 if _settings['insertion_blink'] else 0
            insertion_color = _settings['insertion_color']
            tab_size_spaces = _settings['tab_size']
            padding_x = _settings['padding_x']
            padding_y = _settings['padding_y']
            text_wrap = _settings['text_wrap']

            font_style = tk_font.Font(family=font_family,
                                      size=_settings['font_size'])

            self.textarea.configure(font=font_style,
                                    bg=bg_color,
                                    pady=padding_y,
                                    padx=padding_x,
                                    fg=font_color,
                                    spacing1=top_spacing,
                                    spacing3=bottom_spacing,
                                    insertbackground=insertion_color,
                                    insertofftime=insertion_blink,
                                    wrap=text_wrap)

            self.set_new_tab_width(tab_size_spaces)

            if overwrite:
                MsgBox = tk.messagebox.askquestion('Reset Settings?',
                                                   'Are you sure you want to reset the editor settings to their default value?',
                                                    icon='warning')
                if MsgBox == 'yes':
                    self.store_settings_data(_settings)
                else:
                    self.save('settings.yaml')

    # editor quiet mode calling which removes status bar and menu bar
    def enter_quiet_mode(self, *args):
        self.statusbar.hide_status_bar()
        self.menubar.hide_menu()
        self.scrollx.configure(width=0)
        self.scrolly.configure(width=0)
        self.statusbar.update_status('quiet')

    # editor leaving quite enu to bring back status bar and menu bar
    def leave_quiet_mode(self, *args):
        self.statusbar.show_status_bar()
        self.menubar.show_menu()
        self.scrollx.configure(width=8)
        self.scrolly.configure(width=8)
        self.statusbar.update_status('hide')

    #hide status bar for text class so it can be used in menu class
    def hide_status_bar(self, *args):
        self.statusbar.hide_status_bar()


    # setting up the editor title
    #Renames the window title bar to the name of the current file.
    def set_window_title(self, name=None):
        if name:
            self.master.title(f'{name} - QuietText')
        else:
            self.master.title('Untitled - QuietText')

    # new file creating in the editor feature
    #Deletes all of the text in the current area and sets window title to default.
    def new_file(self, *args):
        self.textarea.delete(1.0, END)
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
            self.clear_and_replace_textarea()
            self.set_window_title(name=self.filename)

    # saving changes made in the file
    def save(self,*args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, END)
                with open(self.filename, 'w') as f:
                    f.write(textarea_content)
                self.statusbar.update_status('saved')
                if self.filename == 'settings.yaml':
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

            textarea_content = self.textarea.get(1.0, END)
            with open(new_file, 'w') as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
            self.statusbar.update_status('saved')
        except Exception as e:
            print(e)
            
    #On exiting the Program
    def quit_save(self):
        try:
            os.path.isfile(self.filename)
            self.save()          
            
        except:
            self.save_as()
        quit()
                        

    def on_closing(self):
        message = messagebox.askyesnocancel("Save On Close", "Do you want to save the changes before closing?")

        if message == True:
            self.quit_save()
            
        elif message == False:
            quit()

        else:
            return

    # running the python file
    def run(self, *args):
        try:
            if self.filename[-3:] == '.py':
                os.system(f"gnome-terminal -- python3.8 {self.filename}")
            else:
                self.statusbar.update_status('no python')
        except TypeError:
            self.statusbar.update_status('no file run')

    # opens the main setting file of the editor
    def open_settings_file(self):
        self.filename = 'settings.yaml'
        self.textarea.delete(1.0, END)
        with open(self.filename, 'r') as f:
            self.textarea.insert(1.0, f.read())
        self.set_window_title(name=self.filename)

    # reset the settings set by the user to the default settings
    def reset_settings_file(self):
        self.reconfigure_settings('settings-default.yaml', overwrite=True)
        self.clear_and_replace_textarea()

    # select all written text in the editor
    def select_all_text(self, *args):
        self.textarea.tag_add(tk.SEL, '1.0', END)
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
        self.right_click_menu.tk_popup(key_event.x_root, key_event.y_root)

    # shortcut keys that the editor supports
    def copy(self, event=None):
        try:
            self.textarea.clipboard_clear()
            text=self.textarea.get("sel.first", "sel.last")
            self.textarea.clipboard_append(text)
        except tk.TclError:
            pass

    def cut(self,event=None):
        try:
            self.copy()
            self.textarea.delete("sel.first", "sel.last")
        except tk.TclError:
            pass

    def paste(self, event=None):
        try:
            text = self.textarea.selection_get(selection='CLIPBOARD')
            self.textarea.insert('insert',text)
        except tk.TclError:
            pass

    # Setting the selected text to be bold
    def bold(self, event=None):
        if self.filename:
            try:
                if(os.path.splitext(self.filename)[1][1:] == "txt"):
                    current_tags = self.textarea.tag_names("sel.first")
                    bold_font = tk_font.Font(self.textarea, self.textarea.cget("font"))
                    bold_font.configure(weight = "bold")
                    self.textarea.tag_configure("bold", font = bold_font)
                    if "bold" in current_tags:
                        self.textarea.tag_remove("bold", "sel.first", "sel.last")
                    else:
                        self.textarea.tag_add("bold", "sel.first", "sel.last")
                else: 
                    self.statusbar.update_status('no txt bold')
            except tk.TclError:
                pass
        else:
            self.statusbar.update_status('no file')

    def hightlight(self, event=None):
        if self.filename:
            try:
                if(os.path.splitext(self.filename)[1][1:] == "txt"):
                    new_color = self.menubar.open_color_picker()
                    current_tags = self.textarea.tag_names("sel.first")
                    highlight_font = tk_font.Font(self.textarea, self.textarea.cget("font"))
                    self.textarea.tag_configure("highlight", font = highlight_font, foreground = "black", background = new_color)
                    if "highlight" in current_tags:
                        self.textarea.tag_remove("highlight", "sel.first", "sel.last")
                    else:
                        self.textarea.tag_add("highlight", "sel.first", "sel.last")
                else:
                    self.statusbar.update_status('no txt high')
            except tk.TclError:
                pass
        else:
            self.statusbar.update_status('no file')
            
          
    def _on_change(self, key_event):
        self.linenumbers.redraw()

    def _on_mousewheel(self, event):
        if self.control_key:
            self.change_font_size(1 if event.delta > 0 else -1)

    def _on_linux_scroll_up(self, _):
        if self.control_key:
            self.change_font_size(1)

    def _on_linux_scroll_down(self, _):
        if self.control_key:
            self.change_font_size(-1)

    def change_font_size(self, delta):
        self.font_size = self.font_size + delta
        min_font_size = 6
        self.font_size = min_font_size if self.font_size < min_font_size else self.font_size
        self.font_style = tk_font.Font(family=self.font_style,
                                       size=self.font_size)
        self.textarea.configure(font=self.font_style)

        self.set_new_tab_width()
        _settings = self.load_settings_data('settings.yaml')
        _settings['font_size'] = self.font_size
        self.store_settings_data(_settings)

        if self.filename == 'settings.yaml':
            self.clear_and_replace_textarea()


    # control_l = 37
    # control_r = 109
    # mac_control = 262401 #control key in mac keyboard
    # mac_control_l = 270336 #left control key in mac os with normal keyboard
    # mac_control_r = 262145 #right control key in mac os with normal keyboard
    def _on_keydown(self, event):
        if event.keycode in [37, 109, 262401, 270336, 262145]:
            self.control_key = True
            self.textarea.isControlPressed = True
        else:
            self.statusbar.update_status('hide')

    def _on_keyup(self, event):
        if event.keycode in [37, 109, 262401, 270336, 262145]:
            self.control_key = False
            self.textarea.isControlPressed = False

    def bind_shortcuts(self, *args):
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
        self.textarea.bind('<Control-b>', self.bold)
        self.textarea.bind('<Control-h>', self.hightlight)
        self.textarea.bind('<Control-a>', self.select_all_text)
        self.textarea.bind('<Control-m>', self.apply_hex_color)
        self.textarea.bind('<Control-r>', self.run)
        self.textarea.bind('<Control-q>', self.enter_quiet_mode)
        self.textarea.bind('<Escape>', self.leave_quiet_mode)
        self.textarea.bind('<<Change>>', self._on_change)
        self.textarea.bind('<Configure>', self._on_change)
        self.textarea.bind('<Button-3>', self.show_click_menu)
        self.textarea.bind('<MouseWheel>', self._on_mousewheel)
        self.textarea.bind('<Button-4>', self._on_linux_scroll_up)
        self.textarea.bind('<Button-5>', self._on_linux_scroll_down)
        self.textarea.bind('<Key>', self._on_keydown)
        self.textarea.bind('<KeyRelease>', self._on_keyup)


if __name__ == '__main__':
    master = tk.Tk()
    try:
        p1 = tk.PhotoImage(file='../images/q.png')
        master.iconphoto(False, p1)
    except Exception as e:
        print(e)
    qt = QuietText(master)
    qt.pack(side='top', fill='both', expand=True)
    master.protocol("WM_DELETE_WINDOW", qt.on_closing)
    master.mainloop()







