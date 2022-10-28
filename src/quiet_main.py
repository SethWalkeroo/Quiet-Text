import os
import tkinter as tk 
import tkinter.font as tk_font
import re
import sys
from platform import system
from tkinter import (filedialog, ttk)
from quiet_syntax_highlighting import SyntaxHighlighting
from quiet_menubar import Menubar
from quiet_statusbar import Statusbar
from quiet_linenumbers import TextLineNumbers
from quiet_textarea import CustomText
from quiet_find import FindWindow 
from quiet_context import ContextMenu
from quiet_loaders import QuietLoaders
from quiet_tree import FileTree

class QuietText(tk.Frame):
    def __init__(self, *args, **kwargs):
        """The main class for bringing the whole shebang together"""
        tk.Frame.__init__(self, *args, **kwargs)
        master.title('untitled - Quiet Text')
        # defined size of the editer window
        master.geometry('1280x720')
        self.configure(bg='black')
        self.loader = QuietLoaders()
        self.operating_system = system()
        self.quiet_icon_path = self.loader.resource_path(os.path.join('data', 'q.png'))
        self.icon = tk.PhotoImage(file = self.quiet_icon_path)
        master.iconphoto(False, self.icon)

        # start editor according to defined settings in settings.yaml
        self.settings = self.loader.load_settings_data()

        #editable settings variables
        self.browser = self.settings['web_browser']
        self.font_family = self.settings['font_family']
        self.tab_size = self.settings['tab_size']
        self.font_size = int(self.settings['font_size'])
        self.top_spacing = self.settings['text_top_lineheight']
        self.bottom_spacing = self.settings['text_bottom_lineheight']
        self.padding_x = self.settings['textarea_padding_x']
        self.padding_y = self.settings['textarea_padding_y']
        self.insertion_blink = 300 if self.settings['insertion_blink'] else 0
        self.tab_size_spaces = self.settings['tab_size']
        self.text_wrap = self.settings['text_wrap']
        self.autoclose_parentheses = self.settings['autoclose_parentheses']
        self.autoclose_curlybraces = self.settings['autoclose_curlybraces']
        self.autoclose_squarebrackets = self.settings['autoclose_squarebrackets']
        self.autoclose_singlequotes = self.settings['autoclose_singlequotes']
        self.autoclose_doublequotes = self.settings['autoclose_doublequotes']
        self.scrollx_width = self.settings['horizontal_scrollbar_width']
        self.scrolly_width = self.settings['vertical_scrollbar_width']
        self.current_line_symbol = self.settings['current_line_indicator_symbol']
        self.current_line_indicator = self.settings['current_line_indicator']
        self.border = self.settings['textarea_border']

        # Editor color scheme variables
        self.insertion_color = '#eb4034'
        self.bg_color = '#eb4034'
        self.font_color = '#eb4034'
        self.text_selection_bg_clr = '#eb4034'
        self.scrollx_clr = '#242222'
        self.troughx_clr = '#242222'
        self.scrollx_active_bg = '#423d3d'
        self.scrolly_clr = '#242222'
        self.troughy_clr = '#242222'
        self.scrolly_active_bg = '#423d3d'
        self.menubar_bg_active = '#eb4034'
        self.menubar_fg_active = '#eb4034'
        self.menu_fg = '#eb4034'
        self.menu_bg = '#eb4034'

        #configuration of the file dialog text colors.
        self.font_style = tk_font.Font(family=self.font_family,
                                       size=self.font_size)

        self.italics = tk_font.Font(family=self.font_family, slant='italic', size=self.font_size)
        self.bold = tk_font.Font(family=self.font_family, weight='bold', size=self.font_size)
        self.header1 = tk_font.Font(family=self.font_family, weight='bold', size=self.font_size + 15)
        self.header2 = tk_font.Font(family=self.font_family, weight='bold', size=self.font_size + 7)

        self.master = master
        self.filename = os.getcwd()
        self.dirname = os.getcwd()

        self.previous_file = None
        self.textarea = CustomText(self)

        self.scrolly = tk.Scrollbar(
            master,
            command=self.textarea.yview,
            bg=self.scrolly_clr,
            troughcolor=self.troughy_clr,
            bd=0,
            width=self.scrolly_width,
            highlightthickness=0,
            activebackground=self.scrolly_active_bg,
            orient='vertical')

        self.scrollx = tk.Scrollbar(
            master,
            command=self.textarea.xview,
            bg=self.scrollx_clr,
            troughcolor=self.troughx_clr,
            bd=0,
            width=self.scrollx_width,
            highlightthickness=0,
            activebackground=self.scrollx_active_bg,
            orient='horizontal')

        self.textarea.configure(
            yscrollcommand=self.scrolly.set,
            xscrollcommand=self.scrollx.set,
            bg=self.bg_color,
            fg=self.font_color,
            wrap= self.text_wrap,
            spacing1=self.top_spacing, 
            spacing3=self.bottom_spacing,
            selectbackground= self.text_selection_bg_clr,
            insertbackground=self.insertion_color,
            insertofftime=self.insertion_blink,
            bd=self.border,
            highlightthickness=self.border,
            highlightbackground='black',
            font=self.font_style,
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

        self.context_menu = ContextMenu(self)
        self.linenumbers = TextLineNumbers(self)
        self.syntax_highlighter = SyntaxHighlighting(self, self.textarea, self.initial_content)
        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)
        self.syntax_highlighter.syntax_and_themes.load_theme_from_config()

        self.linenumbers.attach(self.textarea)
        self.scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        self.linenumbers.pack(side=tk.LEFT, fill=tk.Y)
        self.textarea.pack(side=tk.RIGHT, fill='both', expand=True)
        
        self.textarea.find_match_index = None
        self.textarea.find_search_starting_index = 1.0

        #calling function to bind hotkeys.
        self.bind_shortcuts()
        self.control_key = False
        self.menu_hidden = False
        self.first_word = True

    def clear_and_replace_textarea(self):
        self.textarea.delete(1.0, tk.END)
        try:
            if self.filename:
                with open(self.filename, 'r') as f:
                    self.textarea.insert(1.0, f.read())
            self.syntax_highlighter.initial_highlight()
        except TypeError as e:
            print(e)

    def set_new_tab_width(self, tab_spaces = 'default'):
        """Reconfigure the tab_width depending on changes."""
        if tab_spaces == 'default':
            space_count = self.tab_size_spaces
        else:
            space_count = tab_spaces
        _font = tk_font.Font(font=self.textarea['font'])
        _tab_width = _font.measure(' ' * int(space_count))
        self.textarea.config(tabs=(_tab_width,))

    def reconfigure_settings(self, overwrite_with_default=False):
        """
        Editor basic settings can be altered here
        Function used to reload settings after the user changes in settings.yaml
        """
        if overwrite_with_default:
            _settings = self.loader.load_settings_data(default=True)
        else:
            _settings = self.loader.load_settings_data()
        font_family = _settings['font_family']
        top_spacing = _settings['text_top_lineheight']
        bottom_spacing = _settings['text_bottom_lineheight']
        insertion_blink = 300 if _settings['insertion_blink'] else 0
        tab_size_spaces = _settings['tab_size']
        padding_x = _settings['textarea_padding_x']
        padding_y = _settings['textarea_padding_y']
        text_wrap = _settings['text_wrap']
        border = _settings['textarea_border']
        scrollx_width = _settings['horizontal_scrollbar_width']
        scrolly_width = _settings['vertical_scrollbar_width']
        self.autoclose_parentheses = _settings['autoclose_parentheses']
        self.autoclose_curlybraces = _settings['autoclose_curlybraces']
        self.autoclose_squarebrackets = _settings['autoclose_squarebrackets']
        self.autoclose_singlequotes = _settings['autoclose_singlequotes']
        self.autoclose_doublequotes = _settings['autoclose_doublequotes']
        self.linenumbers.current_line_symbol = _settings['current_line_indicator_symbol']
        self.linenumbers.indicator_on = _settings['current_line_indicator']
        self.browser = _settings['web_browser']
        self.textarea.reload_text_settings()
        self.set_new_tab_width(tab_size_spaces)
        self.menubar.reconfigure_settings()
        self.linenumbers._text_font = font_family
        self.linenumbers.redraw()

        font_style = tk_font.Font(family=font_family,
                                    size=_settings['font_size'])

        self.menubar._menubar.configure(
            fg=self.menu_fg,
            bg=self.menu_bg,
            activeforeground=self.menubar_fg_active,
            activebackground=self.menubar_bg_active,
            activeborderwidth=0,
            bd=0)

        self.context_menu.right_click_menu.configure(
            font=font_family,
            fg=self.menu_fg,
            bg=self.bg_color,
            activebackground=self.menubar_bg_active,
            activeforeground=self.menubar_fg_active,
            bd=0,
            tearoff=0)

        self.scrolly.configure(
            bg=self.scrolly_clr,
            troughcolor=self.troughy_clr,
            width=scrolly_width,
            activebackground=self.scrolly_active_bg)

        self.scrollx.configure(
            bg=self.scrollx_clr,
            troughcolor=self.troughx_clr,
            width=scrollx_width,
            activebackground=self.scrolly_active_bg)

        self.textarea.configure(
            font=font_style,
            bg=self.bg_color,
            pady=padding_y,
            padx=padding_x,
            fg=self.font_color,
            spacing1=top_spacing,
            spacing3=bottom_spacing,
            insertbackground=self.insertion_color,
            selectbackground= self.text_selection_bg_clr,
            insertofftime=insertion_blink,
            bd=border,
            highlightthickness=border,
            wrap=text_wrap)


        if overwrite_with_default:
            MsgBox = tk.messagebox.askquestion(
                'Reset Settings?',
                'Are you sure you want to reset the editor settings to their default value?',
                icon='warning')
            if MsgBox == 'yes':
                self.loader.store_settings_data(_settings)
            else:
                if self.filename == self.loader.settings_path:
                    self.save(self.loader.settings_path)
                self.reconfigure_settings()

    def enter_quiet_mode(self, *args):
        """Editor quiet mode calling which removes status bar and menu bar"""
        self.statusbar.hide_status_bar()
        self.menubar.hide_menu()
        self.scrollx.configure(width=0)
        self.scrolly.configure(width=0)
        self.statusbar.update_status('quiet')

    def leave_quiet_mode(self, *args):
        """Editor leaving quite enu to bring back status bar and menu bar"""
        self.statusbar.show_status_bar()
        self.menubar.show_menu()
        self.scrollx.configure(width=8)
        self.scrolly.configure(width=8)
        self.statusbar.update_status('hide')

    def hide_status_bar(self, *args):
        """Hides status bar for text class for use in the menu class"""
        self.statusbar.hide_status_bar()

    def toggle_linenumbers(self, *args):
        """Toggles the visibility of line numbers"""
        self.linenumbers.visible = not self.linenumbers.visible

    def set_window_title(self, name=None):
        """
        Sets up the editor title
        Renames the window title bar to the name of the current file.
        """
        if name:
            self.master.title(f'{name} - Quiet Text')
        else:
            self.master.title('untitled - Quiet Text')


    def load_previous_file(self, *args):
        if self.previous_file:
            try:
                previous = self.filename
                self.filename = self.previous_file
                self.previous_file = previous
                self.set_window_title(name=self.filename)
                self.initialize_syntax()
                self.clear_and_replace_textarea()
            except PermissionError as e:
                print(e)

    def new_file(self, *args):
        """
        Creates new file in the editor feature
        Deletes all of the text in the current area and sets window title to default
        """
        self.textarea.delete(1.0, tk.END)
        try:
            new_file = filedialog.asksaveasfilename(
                parent=self.master,
                title='New',
                initialdir=self.dirname,
                initialfile='untitled',
                filetypes=[('All Files', '*.*'),
                           ('Text Files', '*.txt'),
                           ('Python Scripts', '*.py'),
                           ('Python No Terminal Scripts', '*.py'),
                           ('Markdown Documents', '*.md'),
                           ('JavaScript Files', '*.js'),
                           ('Java Files', '*.java'),
                           ('Haskell Files', '*.hs'),
                           ('HTML Documents', '*.js'),
                           ('CSS Documents', '*.css'),
                           ('C Files', '*.c'),
                           ('C++ Files', '*.cpp'),
                           ('CoffeeScript Files', '*.coffee'),
                           ('Dart Files', '*.dart'),
                           ('Go Files', '*.go'),
                           ('Rust Files', '*.rs'),
                           ('Swift Files', '*.swift')])
            self.previous_file = self.filename
            self.filename = new_file
            textarea_content = self.textarea.get(1.0, tk.END)
            self.set_window_title('untitled')
            with open(new_file, 'w') as f:
                f.write(textarea_content)
            self.set_window_title(self.filename)
            self.statusbar.update_status('created')
            self.initialize_syntax()
        except Exception as e:
            print(e)

    def initialize_syntax(self):
        if self.filename:
            self.clear_and_replace_textarea()
            if self.filename[-4:] == '.txt' or self.filename[-3:] == '.md':
                self.syntax_highlighter.syntax_and_themes.load_markdown_syntax()
            elif self.filename[-2:] == '.c':
                self.syntax_highlighter.syntax_and_themes.load_c_syntax()
            elif self.filename[-2:] == '.coffee':
                self.syntax_highlighter.syntax_and_themes.load_coffeescript_syntax()
            elif self.filename[-5:] == '.dart':
                self.syntax_highlighter.syntax_and_themes.load_dart_syntax()
            elif self.filename[-3:] == '.py':
                self.syntax_highlighter.syntax_and_themes.load_python3_syntax()
            elif self.filename[-4:] == '.pyw':
                self.syntax_highlighter.syntax_and_themes.load_python3_syntax()
            elif self.filename[-3:] == '.js':
                self.syntax_highlighter.syntax_and_themes.load_javascript_syntax()
            elif self.filename[-5:] == '.java':
                self.syntax_highlighter.syntax_and_themes.load_java_syntax()
            elif self.filename[-3:] == '.hs':
                self.syntax_highlighter.syntax_and_themes.load_haskell_syntax()
            elif self.filename[-5:] == '.html':
                self.syntax_highlighter.syntax_and_themes.load_html_syntax()
            elif self.filename[-4:] == '.css':
                self.syntax_highlighter.syntax_and_themes.load_css_syntax()
            elif self.filename[-4:] == '.cpp':
                self.syntax_highlighter.syntax_and_themes.load_cpp_syntax()
            elif self.filename[-3:] == '.go':
                self.syntax_highlighter.syntax_and_themes.load_go_syntax()
            elif self.filename[-3:] == '.rs':
                self.syntax_highlighter.syntax_and_themes.load_rust_syntax()
            elif self.filename[-4:] == '.sql':
                self.syntax_highlighter.syntax_and_themes.load_sql_syntax()
            elif self.filename[-5:] == '.yaml':
                self.syntax_highlighter.syntax_and_themes.load_yaml_syntax()
            elif self.filename[-6:] == '.swift':
                self.syntax_highlighter.syntax_and_themes.load_swift_syntax()
            elif self.filename[-10:] == 'Dockerfile':
                self.syntax_highlighter.syntax_and_themes.load_docker_syntax()
            elif self.filename[-4:] == '.nim':
                self.syntax_highlighter.syntax_and_themes.load_nim_syntax()

    def open_file(self, *args):
        """Opens an existing file from supported file types"""
        self.previous_file = self.filename
        try:
            self.filename = filedialog.askopenfilename(
                parent=self.master,
                initialdir=self.dirname,
                filetypes=[('All Files', '*.*'),
                           ('Text Files', '*.txt'),
                           ('Python Scripts', '*.py'),
                           ('Python No Terminal Scripts', '*.py'),
                           ('Markdown Documents', '*.md'),
                           ('JavaScript Files', '*.js'),
                           ('Java Files', '*.java'),
                           ('Haskell Files', '*.hs'),
                           ('HTML Documents', '*.html'),
                           ('CSS Documents', '*.css'),
                           ('C Files', '*.c'),
                           ('C++ Files', '*.cpp'),
                           ('CoffeeScript Files', '*.coffee'),
                           ('Dart Files', '*.dart'),
                           ('Go Files', '*.go'),
                           ('Rust Files', '*.rs'),
                           ('Sql Files', '*.sql'),
                           ('Swift Files', '*.swift')])

            self.initialize_syntax()
            if not self.filename:
                self.filename = self.previous_file
            self.set_window_title(name=self.filename)
        except Exception as e:
            print(e)

    def open_dir(self):
        try:
            self.dirname = filedialog.askdirectory(
                parent=self.master)
            self.filename = self.dirname
            if self.dirname:
                self.set_window_title(name=self.filename)
                FileTree(self)
        except Exception:
            pass

    def show_file_tree(self, *args):
        self.control_key = False
        self.textarea.isControlPressed = False
        FileTree(self)
        return 'break'

    def save(self,*args):
        """Saves changes made to the file"""
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, 'w') as f:
                    f.write(textarea_content)
                self.statusbar.update_status('saved')
                if self.filename == self.loader.settings_path:
                    self.reconfigure_settings()
                    self.menubar.reconfigure_settings()
            except Exception as e:
                pass
        else:
            self.save_as()

    def save_as(self, *args):
        """Saves a file with a particular name"""
        try:
            self.filename = filedialog.asksaveasfilename(
                parent=self.master,
                initialdir=self.dirname,
                filetypes=[('All Files', '*.*'),
                           ('Text Files', '*.txt'),
                           ('Python Scripts', '*.py'),
                           ('Python No Terminal Scripts', '*.pyw'),
                           ('Markdown Documents', '*.md'),
                           ('Javascript Files', '*.js'),
                           ('Java Files', '*.java'),
                           ('Haskell Files', '*.hs'),
                           ('HTML Documents', '*.html'),
                           ('CSS Documents', '*.css'),
                           ('C Files', '*.c'),
                           ('C++ Files', '*.cpp'),
                           ('CoffeeScript Files', '*.coffee'),
                           ('Dart Files', '*.dart'),
                           ('Go Files', '*.go'),
                           ('Rust Files', '*.rs'),
                           ('Sql Files', '*.sql'),
                           ('Swift Files', '*.swift')])

            textarea_content = self.textarea.get(1.0, tk.END)
            with open(self.filename, 'w') as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
            self.statusbar.update_status('saved')
            self.initialize_syntax()
        except Exception as e:
            pass
            
    def quit_save(self):
        """On exit for the editor"""
        try:
            os.path.isfile(self.filename)
            self.save()
        except Exception:
            self.save_as()
        sys.exit()

    def on_closing(self):
        message = tk.messagebox.askyesnocancel("Save On Close", "Do you want to save the changes before closing?")
        if message == True:
            self.quit_save()
        elif message == False:
            sys.exit()
        else:
            return

    def open_settings_file(self):
        """Opens the main setting file of the editor"""
        self.syntax_highlighter.syntax_and_themes.load_yaml_syntax()
        self.previous_file = self.filename
        self.filename = self.loader.settings_path
        self.textarea.delete(1.0, tk.END)
        with open(self.filename, 'r') as f:
            self.textarea.insert(1.0, f.read())
        self.syntax_highlighter.initial_highlight()
        self.set_window_title(name=self.filename)

    def reset_settings_file(self):
        """Resets user defined settings to the default settings"""
        self.reconfigure_settings(overwrite_with_default=True)
        self.syntax_highlighter.syntax_and_themes.load_material()
        try:
            self.clear_and_replace_textarea()
        except IsADirectoryError:
            pass

    def select_all_text(self, *args):
        """Selects all written text in the editor"""
        self.textarea.tag_add(tk.SEL, '1.0', tk.END)
        self.textarea.mark_set(tk.INSERT, '1.0')
        self.textarea.see(tk.INSERT)
        return 'break'

    def apply_hex_color(self, key_event):
        """Applies hex colors to the file content for better understanding"""
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
            if self.filename == self.loader.settings_path:
                self.syntax_highlighter.initial_highlight()

    def _on_linux_scroll_down(self, _):
        if self.control_key:
            self.change_font_size(-1)
            if self.filename == self.loader.settings_path:
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

        self.bold = tk_font.Font(family=self.font_family,
                                 size = self.font_size,
                                 weight='bold')

        self.header1 = tk_font.Font(family=self.font_family,
                                    size = self.font_size + 15,
                                    weight='bold')

        self.header2 = tk_font.Font(family=self.font_family,
                                    size = self.font_size + 7,
                                    weight='bold')

        self.textarea.configure(font=self.font_style)
        self.syntax_highlighter.text.tag_configure("Token.Name.Builtin.Pseudo",font=self.italics)
        self.syntax_highlighter.text.tag_configure("Token.Keyword.Type",font=self.italics)
        self.syntax_highlighter.text.tag_configure("Token.Keyword.Declaration",font=self.italics)
        self.syntax_highlighter.text.tag_configure("Token.Generic.Emph",font=self.italics)
        self.syntax_highlighter.text.tag_configure("Token.Generic.Strong",font=self.bold)
        self.syntax_highlighter.text.tag_configure("Token.Generic.Heading",font=self.header1)
        self.syntax_highlighter.text.tag_configure("Token.Generic.Subheading",font=self.header2)
        self.set_new_tab_width()
        
        _settings = self.loader.load_settings_data()
        _settings['font_size'] = self.font_size
        self.loader.store_settings_data(_settings)

        if self.filename == self.loader.settings_path:
            self.clear_and_replace_textarea()

    def _on_keydown(self, event):
        keycodes = (
            17,
            37,  # control_l
            109,  # control_r
            262401,  # mac_control (control key in mac keyboard)
            270336,  # mac_control_l (tk.left control key in mac os with normal keyboard)
            262145,  # mac_control_r (tk.right control key in mac os with normal keyboard)
        )
        if event.keycode in keycodes:
            self.control_key = True
            self.textarea.isControlPressed = True
        else:
            self.statusbar.update_status('hide')

    def syntax_highlight(self, *args):
        if self.first_word:
            self.syntax_highlighter.initial_highlight()
            self.first_word = not self.first_word
        self.syntax_highlighter.default_highlight()
        self.control_key = False
        self.textarea.isControlPressed = False

    def show_find_window(self, event=None):
        self.textarea.tag_configure('find_match', background=self.text_selection_bg_clr)
        self.textarea.bg_color = self.bg_color
        self.textarea.fg_color = self.menu_fg
        self.textarea.active_fg = self.menubar_fg_active
        self.textarea.active_bg = self.menubar_bg_active
        FindWindow(self.textarea)
        self.control_key = False
        self.textarea.isControlPressed = False

    def select_all(self):
        self.selection_set(0, 'end')

    def autoclose_base(self, symbol):
        index = self.textarea.index(tk.INSERT)
        self.textarea.insert(index, symbol)
        self.textarea.mark_set(tk.INSERT, index)

    def autoclose_parens(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.autoclose_parentheses and not second_char.isalnum():
            self.autoclose_base(')')

    def autoclose_curly_brackets(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.autoclose_curlybraces and not second_char.isalnum():
            self.autoclose_base('}')

    def autoclose_square_brackets(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.autoclose_squarebrackets and not second_char.isalnum():
            self.autoclose_base(']')

    def autoclose_double_quotes(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.autoclose_doublequotes and not second_char.isalnum():
            self.autoclose_base('"')

    def autoclose_single_quotes(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.autoclose_singlequotes and not second_char.isalnum():
            self.autoclose_base("'")

    def get_indent_level(self):
        text = self.textarea
        line = text.get('insert linestart', 'insert lineend')
        match = re.match(r'^(\s+)', line)
        current_indent = len(match.group(0)) if match else 0
        return current_indent

    def auto_indentation(self):
        text = self.textarea
        new_indent = self.get_indent_level()
        text.insert('insert', '\n' + '\t' * new_indent)

    def auto_block_indentation(self, event):
        prev_char, second_char, _, _ = self.get_chars_in_front_and_back()
        text = self.textarea
        if prev_char == ':':
            current_indent = self.get_indent_level()
            new_indent = current_indent + 1
            text.insert('insert', '\n' + '\t' * new_indent)
            return 'break'
        elif prev_char in '{[(' and second_char in '}])':
            current_indent = self.get_indent_level()
            new_indent = current_indent + 1
            text.insert('insert', '\n\n')
            text.insert('insert', '\t' * current_indent)
            index = text.index(tk.INSERT)
            text.mark_set('insert', str(round(float(index) - 1, 1)))
            text.insert('insert', '\t' * new_indent)
            return 'break'
        else:
            self.auto_indentation()
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
            if event.state == 0:
                while self.textarea.compare(index,"<=", last):
                    if len(self.textarea.get(index, 'end')) != 0:
                        self.textarea.insert(index, '\t')
                    index = self.textarea.index("%s + 1 line" % index)
            else:
                while self.textarea.compare(index,"<=", last):
                    if self.textarea.get(index, 'end')[:1] == "\t":
                        self.textarea.delete(index)
                    index = self.textarea.index("%s + 1 line" % index)
        else:
            if event.state == 0:
                index = self.textarea.index(tk.INSERT)
                self.textarea.insert(index, '\t')
            else:
                index = self.textarea.index("insert linestart")
                if self.textarea.get(index, 'end')[:1] == "\t":
                    self.textarea.delete(index)
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
        text.bind('<Control-r>', self.menubar.run)
        text.bind('<Control-q>', self.enter_quiet_mode)
        text.bind('<Control-f>', self.show_find_window)
        text.bind('<Control-p>', self.load_previous_file)
        text.bind('<Control-t>', self.show_file_tree)
        text.bind('<Control-z>', self.syntax_highlighter.initial_highlight)
        text.bind('<Control-y>', self.syntax_highlighter.initial_highlight)
        text.bind('<Escape>', self.leave_quiet_mode)
        text.bind('<<Change>>', self._on_change)
        text.bind('<Configure>', self._on_change)
        text.bind('<Button-3>', self.context_menu.popup)
        text.bind('<MouseWheel>', self._on_mousewheel)
        text.bind('<Button-4>', self._on_linux_scroll_up)
        text.bind('<Button-5>', self._on_linux_scroll_down)
        text.bind('<Key>', self._on_keydown)
        text.bind('<KeyRelease>', self.syntax_highlight)
        text.bind('<Shift-asciitilde>', self.syntax_highlighter.initial_highlight)
        text.bind('<Shift-parenleft>', self.autoclose_parens)
        text.bind('<bracketleft>', self.autoclose_square_brackets)
        text.bind('<quoteright>', self.autoclose_single_quotes)
        text.bind('<quotedbl>', self.autoclose_double_quotes)
        text.bind('<braceleft>', self.autoclose_curly_brackets)
        text.bind('<Return>', self.auto_block_indentation)
        text.bind('<BackSpace>', self.backspace_situations)
        text.bind('<Alt_L>', self.hide_and_unhide_menubar)
        text.bind('<Control-L>', self.toggle_linenumbers)
        text.bind('<KeyPress-Tab>', self.tab_text)
        if self.operating_system == 'Windows':
            text.bind('<Shift-Tab>', self.tab_text)
        else:
            text.bind('<Shift-ISO_Left_Tab>', self.tab_text)

if __name__ == '__main__':
    master = tk.Tk()
    qt = QuietText(master)
    qt.pack(side='top', fill='both', expand=True)
    master.protocol("WM_DELETE_WINDOW", qt.on_closing)
    master.mainloop()

