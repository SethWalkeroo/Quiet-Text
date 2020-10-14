import os
import sys
import time
import yaml
import tkinter as tk 
import tkinter.font as tk_font
import re

from tkinter import (filedialog, messagebox, ttk)
from quiet_syntax_highlighting import SyntaxHighlighting
from quiet_menubar import Menu, Menubar
from quiet_statusbar import Statusbar
from quiet_linenumbers import TextLineNumbers
from quiet_textarea import CustomText
from quiet_find import FindWindow
from quiet_context import ContextMenu
from quiet_loaders import QuietLoaders

class QuietText(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        master.title('untitled - Quiet Text')
        # defined size of the editer window
        master.geometry('1920x1080')
        self.loader = QuietLoaders()

        # start editor according to defined settings in settings.yaml
        self.settings = self.loader.load_settings_data()
        self.default_theme = self.loader.load_default_theme()

        self.settings['font_color'] = self.default_theme['font_color']
        self.settings['textarea_background_color'] = self.default_theme['bg_color']
        self.settings['menubar_active_bg'] = self.default_theme['menu_bg_active']
        self.settings['menubar_active_fg'] = self.default_theme['menu_fg_active']  
        self.settings['menu_active_bg'] = self.default_theme['menu_bg_active']
        self.settings['menu_active_fg'] = self.default_theme['menu_fg_active']

        self.font_family = self.settings['font_family']
        self.bg_color = self.settings['textarea_background_color']
        self.font_color = self.settings['font_color']
        self.tab_size = self.settings['tab_size']
        self.font_size = int(self.settings['font_size'])
        self.top_spacing = self.settings['text_top_lineheight']
        self.bottom_spacing = self.settings['text_bottom_lineheight']
        self.padding_x = self.settings['textarea_padding_x']
        self.padding_y = self.settings['textarea_padding_y']
        self.insertion_blink = 300 if self.settings['insertion_blink'] else 0
        self.insertion_color = self.settings['insertion_color']
        self.tab_size_spaces = self.settings['tab_size']
        self.text_wrap = self.settings['text_wrap']
        self.autoclose_parens = self.settings['autoclose_parentheses']
        self.autoclose_curlybraces = self.settings['autoclose_curlybraces']
        self.autoclose_squarebrackets = self.settings['autoclose_squarebrackets']
        self.autoclose_singlequotes = self.settings['autoclose_singlequotes']
        self.autoclose_doublequotes = self.settings['autoclose_doublequotes']
        self.border = self.settings['textarea_border']
        self.text_selection_bg = self.settings['text_selection_bg']
        self.scrollx_clr = self.settings['horizontal_scrollbar_color']
        self.troughx_clr = self.settings['horizontal_scrollbar_trough_color']
        self.scrollx_width = self.settings['horizontal_scrollbar_width']
        self.scrollx_active_bg = self.settings['horizontal_scrollbar_active_bg']
        self.scrolly_clr = self.settings['vertical_scrollbar_color']
        self.troughy_clr = self.settings['vertical_scrollbar_trough_color']
        self.scrolly_width = self.settings['vertical_scrollbar_width']
        self.scrolly_active_bg = self.settings['vertical_scrollbar_active_bg']
        self.menu_fg = self.settings['menu_fg']
        self.menu_bg = self.settings['menu_bg']



        master.tk_setPalette(background=self.bg_color, foreground='black')
        self.font_style = tk_font.Font(family=self.font_family,
                                       size=self.settings['font_size'])

        #configuration of the file dialog text colors.

        self.italics = tk_font.Font(family=self.font_family, slant='italic')
        self.master = master
        self.filename = None
                                
        self.textarea = CustomText(self)

        self.scrolly = tk.Scrollbar(master,
                                    command=self.textarea.yview,
                                    bg=self.scrolly_clr,
                                    troughcolor=self.troughy_clr,
                                    bd=0,
                                    width=self.scrolly_width,
                                    highlightthickness=0,
                                    activebackground=self.scrolly_active_bg,
                                    orient='vertical')

        self.scrollx = tk.Scrollbar(master,
                                    command=self.textarea.xview,
                                    bg=self.scrollx_clr,
                                    troughcolor=self.troughx_clr,
                                    bd=0,
                                    width=self.scrollx_width,
                                    highlightthickness=0,
                                    activebackground=self.scrollx_active_bg,
                                    orient='horizontal')

        self.textarea.configure(yscrollcommand=self.scrolly.set,
                                xscrollcommand=self.scrollx.set,
                                bg=self.bg_color,
                                fg=self.font_color,
                                wrap= self.text_wrap,
                                spacing1=self.top_spacing, 
                                spacing3=self.bottom_spacing,
                                selectbackground= self.text_selection_bg,
                                insertbackground=self.insertion_color,
                                insertofftime=self.insertion_blink,
                                bd=self.border,
                                highlightthickness=self.border,
                                highlightbackground='black',
                                font=self.font_family,
                                undo=True,
                                autoseparators=True,
                                maxundo=-1,
                                padx=self.padding_x,
                                pady=self.padding_y)

        self.initial_content = self.textarea.get("1.0", tk.END)

        #retrieving the font from the text area and setting a tab width
        self._font = tk_font.Font(font=self.textarea['font'])
        self._tab_width = self._font.measure(' ' * self.tab_size_spaces)
        self.textarea.config(tabs=(self._tab_width,))

        self.menu_hidden = False
        self.context_menu = ContextMenu(self)
        self.statusbar = Statusbar(self)
        self.linenumbers = TextLineNumbers(self)
        self.syntax_highlighter = SyntaxHighlighting(self, self.textarea, self.initial_content)
        self.menubar = Menubar(self)

        self.linenumbers.attach(self.textarea)
        self.scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollx.pack(side=tk.BOTTOM, fill='both')
        self.linenumbers.pack(side=tk.LEFT, fill=tk.Y)
        self.textarea.pack(side=tk.RIGHT, fill='both', expand=True)
        
        self.textarea.tag_configure('find_match', background='#75715e')
        self.textarea.find_match_index = None
        self.textarea.find_search_starting_index = 1.0

        self.tags_configured = False
        #calling function to bind hotkeys.
        self.bind_shortcuts()
        self.control_key = False

    def clear_and_replace_textarea(self):
            self.textarea.delete(1.0, tk.END)
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
    def reconfigure_settings(self, overwrite_with_default=False):
            if overwrite_with_default:
                _settings = self.loader.load_settings_data(default=True)
            else:
                _settings = self.loader.load_settings_data()
            font_family = _settings['font_family']
            bg_color = _settings['textarea_background_color']
            font_color = _settings['font_color']
            top_spacing = _settings['text_top_lineheight']
            bottom_spacing = _settings['text_bottom_lineheight']
            insertion_blink = 300 if _settings['insertion_blink'] else 0
            insertion_color = _settings['insertion_color']
            tab_size_spaces = _settings['tab_size']
            padding_x = _settings['textarea_padding_x']
            padding_y = _settings['textarea_padding_y']
            text_wrap = _settings['text_wrap']
            border = _settings['textarea_border']
            text_selection_bg = _settings['text_selection_bg']
            scrollx_clr = _settings['horizontal_scrollbar_color']
            troughx_clr = _settings['horizontal_scrollbar_trough_color']
            scrollx_width = _settings['horizontal_scrollbar_width']
            scrollx_active_bg = _settings['horizontal_scrollbar_active_bg']
            menu_fg = _settings['menu_fg']
            menu_bg = _settings['menu_bg']

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
                                    selectbackground= text_selection_bg,
                                    insertofftime=insertion_blink,
                                    bd=border,
                                    highlightthickness=border,
                                    wrap=text_wrap)

            self.set_new_tab_width(tab_size_spaces)
            self.menubar.reconfigure_settings()
            self.linenumbers.font_color = menu_fg
            self.linenumbers.config(bg=bg_color, highlightbackground=bg_color)
            self.statusbar._label.config(bg=bg_color)
            self.linenumbers.redraw()

            if overwrite_with_default:
                MsgBox = tk.messagebox.askquestion('Reset Settings?',
                                                   'Are you sure you want to reset the editor settings to their default value?',
                                                    icon='warning')
                if MsgBox == 'yes':
                    self.loader.store_settings_data(_settings)
                else:
                    self.save('config/settings.yaml')

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

    # toggle the visibility of line numbers
    def toggle_linenumbers(self, *args):
        self.linenumbers.visible = not self.linenumbers.visible

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
            self.clear_and_replace_textarea()
            self.set_window_title(name=self.filename)
            self.syntax_highlighter.initial_highlight()

    # opening an existing file without TK filedialog
    def open_file_without_dialog(self, path):
        if os.path.isdir(path):
            self.statusbar.update_status('Unable to open directory.')
            return

        if not os.path.exists(path):
            self.statusbar.update_status('File does not exists.')
            return

        self.filename = path
        self.clear_and_replace_textarea()
        self.syntax_highlighter.initial_highlight()

    # saving changes made in the file
    def save(self,*args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, 'w') as f:
                    f.write(textarea_content)
                self.statusbar.update_status('saved')
                if self.filename == 'config/settings.yaml':
                    self.reconfigure_settings()
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
            
    #On exiting the Program
    def quit_save(self):
        try:
            os.path.isfile(self.filename)
            self.save()          
        except:
            self.save_as()
        quit()
                        

    def on_closing(self):
        message = tk.messagebox.askyesnocancel("Save On Close", "Do you want to save the changes before closing?")
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
                #run separate commands for different os
                if os.name == 'nt':
                    os.system(f'start cmd.exe @cmd /k "python {self.filename}"')
                else:
                    os.system(f"gnome-terminal -- python3.8 {self.filename}")
            else:
                self.statusbar.update_status('no python')
        except TypeError:
            self.statusbar.update_status('no file run')

    # opens the main setting file of the editor
    def open_settings_file(self):
        self.filename = 'config/settings.yaml'
        self.textarea.delete(1.0, tk.END)
        with open(self.filename, 'r') as f:
            self.textarea.insert(1.0, f.read())
        self.syntax_highlighter.initial_highlight()
        self.set_window_title(name=self.filename)

    # reset the settings set by the user to the default settings
    def reset_settings_file(self):
        self.reconfigure_settings(overwrite_with_default=True)
        self.clear_and_replace_textarea()
        self.syntax_highlighter.initial_highlight()

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

    def _on_change(self, key_event):
        self.linenumbers.redraw()

    def _on_mousewheel(self, event):
        if self.control_key:
            self.change_font_size(1 if event.delta > 0 else -1)

    def _on_linux_scroll_up(self, _):
        if self.control_key:
            self.change_font_size(1)
            if self.filename == 'config/settings.yaml':
                self.syntax_highlighter.initial_highlight()

    def _on_linux_scroll_down(self, _):
        if self.control_key:
            self.change_font_size(-1)
            if self.filename == 'config/settings.yaml':
                self.syntax_highlighter.initial_highlight()

    def change_font_size(self, delta):
        self.font_size = self.font_size + delta
        min_font_size = 6
        self.font_size = min_font_size if self.font_size < min_font_size else self.font_size
        self.font_style = tk_font.Font(family=self.font_family,
                                       size=self.font_size)

        self.italics = tk_font.Font(family=self.font_family,
                                    size=self.font_size,
                                    slant='italic')

        self.textarea.configure(font=self.font_style)
        self.syntax_highlighter.text.tag_configure("Token.Name.Builtin.Pseudo",font=self.italics)
        self.set_new_tab_width()
        
        _settings = self.loader.load_settings_data()
        _settings['font_size'] = self.font_size
        self.loader.store_settings_data(_settings)

        if self.filename == 'config/settings.yaml':
            self.clear_and_replace_textarea()


    # control_l = 37
    # control_r = 109
    # mac_control = 262401 #control key in mac keyboard
    # mac_control_l = 270336 #tk.LEFT control key in mac os with normal keyboard
    # mac_control_r = 262145 #tk.RIGHT control key in mac os with normal keyboard
    def _on_keydown(self, event):
        if event.keycode in [37, 109, 262401, 270336, 262145]:
            self.control_key = True
            self.textarea.isControlPressed = True
        else:
            self.statusbar.update_status('hide')

    def syntax_highlight(self, *args):
        self.syntax_highlighter.default_highlight()
        if not self.tags_configured:
            self.syntax_highlighter.syntax_theme_configuration()
        self.control_key = False
        self.textarea.isControlPressed = False

    def show_find_window(self, event=None):
        FindWindow(self.textarea)
        self.control_key = False
        self.textarea.isControlPressed = False

    def select_all(self):
        self.selection_set(0, 'end')

    def autoclose_base(self, symbol):
        index = self.textarea.index(tk.INSERT)
        self.textarea.insert(index, symbol)
        self.textarea.mark_set(tk.INSERT, index)

    def autoclose_parentheses(self, event):
        if self.autoclose_parentheses:
            self.autoclose_base(')')

    def autoclose_curly_brackets(self, event):
        if self.autoclose_curlybraces:
            self.autoclose_base('}')

    def autoclose_square_brackets(self, event):
        if self.autoclose_squarebrackets:
            self.autoclose_base(']')

    def autoclose_double_quotes(self, event):
        if self.autoclose_doublequotes:
            self.autoclose_base('"')

    def autoclose_single_quotes(self, event):
        if self.autoclose_singlequotes:
            self.autoclose_base("'")

    def auto_indentation(self, event):
        text = self.textarea
        line = text.get('insert linestart', 'insert lineend')
        new_indent = self.get_indent_level(line) * 4
        text.insert('insert', '\n' + ' ' * new_indent)
        return 'break'

    def get_indent_level(self, line):
        num_leading_whitespaces = len(line) - len(line.lstrip())
        return num_leading_whitespaces // 4

    def auto_block_indentation(self, event):
        text = self.textarea
        line = text.get('insert linestart', 'insert lineend')
        match = re.match(r'^(\s+)', line)
        current_indent = len(match.group(0)) if match else 0
        new_indent = current_indent + 4
        text.insert('insert', event.char + '\n' + ' ' * new_indent)
        return 'break'


    def get_chars_in_front_and_back(self):
        index = self.textarea.index(tk.INSERT)
        first_pos = f'{str(index)}-1c'
        end_second_pos = f'{str(index)}+1c'
        first_char = self.textarea.get(first_pos, index)
        second_char = self.textarea.get(index, end_second_pos)
        return (first_char, second_char, index, end_second_pos)
        
    def backspace_situations(self, event):
        first_char, second_char, index, end_second_pos = self.get_chars_in_front_and_back()

        if first_char == "'" and second_char == "'":
            self.textarea.delete(index, end_second_pos)
        elif first_char == '"' and second_char == '"':
            self.textarea.delete(index, end_second_pos)
        elif first_char == '(' and second_char == ')':
            self.textarea.delete(index, end_second_pos)
        elif first_char == '{' and second_char == '}':
            self.textarea.delete(index, end_second_pos)
        elif first_char == '[' and second_char == ']':
            self.textarea.delete(index, end_second_pos)

    def hide_and_unhide_menubar(self, key_event):
        if self.menu_hidden:
            self.menubar.show_menu()
        else:
            self.menubar.hide_menu()
        self.menu_hidden = not self.menu_hidden

    def tab_text(self, event):
        index = self.textarea.index("sel.first linestart")
        last = self.textarea.index("sel.last linestart")
        if last != index:
            while self.textarea.compare(index,"<=", last):
                self.textarea.insert(index, '\t')
                index = self.textarea.index("%s + 1 line" % index)
        else:
            index = self.textarea.index(tk.INSERT)
            self.textarea.insert(index, '\t')
        return "break"


    def bind_shortcuts(self, *args):
        text = self.textarea
        text.bind('<Control-n>', self.new_file)
        text.bind('<Control-o>', self.open_file)
        text.bind('<Control-s>', self.save)
        text.bind('<Control-S>', self.save_as)
        text.bind('<Control-b>', self.context_menu.bold)
        text.bind('<Control-h>', self.context_menu.hightlight)
        text.bind('<Control-a>', self.select_all_text)
        text.bind('<Control-m>', self.apply_hex_color)
        text.bind('<Control-r>', self.run)
        text.bind('<Control-q>', self.enter_quiet_mode)
        text.bind('<Control-f>', self.show_find_window)
        text.bind('<Escape>', self.leave_quiet_mode)
        text.bind('<<Change>>', self._on_change)
        text.bind('<Configure>', self._on_change)
        text.bind('<Button-3>', self.context_menu.popup)
        text.bind('<MouseWheel>', self._on_mousewheel)
        text.bind('<Button-4>', self._on_linux_scroll_up)
        text.bind('<Button-5>', self._on_linux_scroll_down)
        text.bind('<Key>', self._on_keydown)
        text.bind('<KeyRelease>', self.syntax_highlight)
        text.bind_all('<<Paste>>', self.context_menu.paste)
        text.bind('<Shift-asciitilde>', self.syntax_highlighter.initial_highlight)
        text.bind('<Control-Shift-KeyRelease>', self.syntax_highlighter.initial_highlight)
        text.bind('<Shift-parenleft>', self.autoclose_parentheses)
        text.bind('<bracketleft>', self.autoclose_square_brackets)
        text.bind('<quoteright>', self.autoclose_single_quotes)
        text.bind('<quotedbl>', self.autoclose_double_quotes)
        text.bind('<braceleft>', self.autoclose_curly_brackets)
        text.bind('<Return>', self.auto_indentation)
        text.bind('<Shift-colon>', self.auto_block_indentation)
        text.bind('<BackSpace>', self.backspace_situations)
        text.bind('<Alt_L>', self.hide_and_unhide_menubar)
        text.bind('<Control-L>', self.toggle_linenumbers)
        text.bind('<KeyPress-Tab>', self.tab_text)


if __name__ == '__main__':
    master = tk.Tk()
    try:
        p1 = tk.PhotoImage(file='../images/q.png')
        master.iconphoto(False, p1)
    except Exception as e:
        print(e)
    qt = QuietText(master)
    qt.pack(side='top', fill='both', expand=True)
    if len(sys.argv) > 1:
        qt.open_file_without_dialog(sys.argv[-1])
    master.protocol("WM_DELETE_WINDOW", qt.on_closing)
    master.mainloop()












