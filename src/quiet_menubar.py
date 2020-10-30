import tkinter as tk
import os
import re
from tkinter.colorchooser import askcolor
from quiet_syntax_highlighting import SyntaxHighlighting
from time import sleep


class Menubar():
    # initialising the menu bar of editor
    def __init__(self, parent):
        self._parent = parent
        self.settings = parent.loader.load_settings_data()
        self.syntax = parent.syntax_highlighter
        self.ptrn = r'[^\/]+$'
        font_specs = ('Droid Sans Fallback', 12)

        # setting up basic features in menubar
        menubar = tk.Menu(
          parent.master,
          font=font_specs,
          fg=self.settings['menu_fg'],
          bg=self.settings['menu_bg'],
          activeforeground= self.settings['menubar_active_fg'],
          activebackground= self.settings['menubar_active_bg'],
          activeborderwidth=0,
          bd=0)

        parent.master.config(menu=menubar)
        self._menubar = menubar
        # adding features file dropdown in menubar
        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(
          label='Load Previous File',
          accelerator='Ctrl+P',
          command=parent.load_previous_file)
        # new file creation feature
        file_dropdown.add_command(
          label='New File',
            accelerator='Ctrl+N',
            command=parent.new_file)
        # open file feature
        file_dropdown.add_command(
          label='Open File',
            accelerator='Ctrl+O',
            command=parent.open_file)
        file_dropdown.add_command(
          label='Open Directory',
          command=parent.open_dir)
        # save file feature
        file_dropdown.add_command(
          label='Save',
            accelerator='Ctrl+S',
            command=parent.save)
        # Save as feature
        file_dropdown.add_command(
          label='Save As',
            accelerator='Ctrl+Shift+S',
            command=parent.save_as)
        # exit feature
        file_dropdown.add_separator()
        file_dropdown.add_command(
          label='Exit',
          command=parent.on_closing)

        # adding featues to settings dropdown in menubar
        # Edit settings feature
        settings_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        settings_dropdown.add_command(
          label='Edit Settings',
          command=parent.open_settings_file)
        # reset settings feature
        settings_dropdown.add_command(
          label='Reset Settings to Default',
          command=parent.reset_settings_file)

        #view dropdown menu
        view_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        view_dropdown.add_command(
          label='Toggle Menu Bar',
          accelerator='Alt',
          command=self.hide_menu)
        view_dropdown.add_command(
          label='Hide Status Bar',
          command=parent.hide_status_bar)
        view_dropdown.add_command(
          label='Toggle Line Numbers',
          accelerator='Ctrl+Shift+L',
          command=parent.toggle_linenumbers)
        view_dropdown.add_command(
          label='Toggle Text Border',
          command=self.toggle_text_border)
        view_dropdown.add_command(
          label='Shrink/Enlarge Horizontal Scrollbar',
          command=self.toggle_scroll_x)
        view_dropdown.add_command(
          label='Shrink/Enlarge Vertical Scrollbar',
          command=self.toggle_scroll_y)
        view_dropdown.add_command(
          label='Destroy Horizontal Scrollbar',
          command=self._parent.scrollx.forget)
        view_dropdown.add_command(label='Destroy Vertical Scrollbar',
          command=self._parent.scrolly.forget)
        view_dropdown.add_command(
          label='Enter Quiet Mode',
          accelerator='Ctrl+Q',
          command=self.enter_quiet_mode)

        #tools dropdown menu
        tools_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        tools_dropdown.add_command(
          label='Search and Replace',
          accelerator='Ctrl+F',
          command=parent.show_find_window)
        tools_dropdown.add_command(
          label='Display File Tree',
          accelerator='Ctrl+T',
          command=parent.show_file_tree)
        tools_dropdown.add_command(
          label='Open Color Selector',
          accelerator='Ctrl+M',
          command=self.open_color_picker)

        #theme dropdown menu
        theme_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        theme_dropdown.add_command(
          label='Dark Heart',
          command=self.syntax.syntax_and_themes.load_darkheart)
        theme_dropdown.add_command(
          label='Dracula',
          command=self.syntax.syntax_and_themes.load_dracula)
        theme_dropdown.add_command(
          label='Desert',
          command=self.syntax.syntax_and_themes.load_desert)
        theme_dropdown.add_command(
          label='Githubly',
          command=self.syntax.syntax_and_themes.load_githubly)
        theme_dropdown.add_command(
          label='Gruvbox',
          command=self.syntax.syntax_and_themes.load_gruvbox)
        theme_dropdown.add_command(
          label='Material',
          command=self.syntax.syntax_and_themes.load_material)
        theme_dropdown.add_command(
          label='Monokai',
          command=self.syntax.syntax_and_themes.load_monokai)
        theme_dropdown.add_command(
          label='Monokai Pro',
          command=self.syntax.syntax_and_themes.load_monokai_pro)
        theme_dropdown.add_command(
          label='Pumpkin',
          command=self.syntax.syntax_and_themes.load_pumpkin)
        theme_dropdown.add_command(
          label='Rust',
          command=self.syntax.syntax_and_themes.load_rust)
        theme_dropdown.add_command(
          label='Solarized',
          command=self.syntax.syntax_and_themes.load_solarized)

        syntax_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        syntax_dropdown.add_command(
          label='C',
          command=self.syntax.syntax_and_themes.load_c_syntax)
        syntax_dropdown.add_command(
          label='C++',
          command=self.syntax.syntax_and_themes.load_cpp_syntax)
        syntax_dropdown.add_command(
          label='CoffeeScript',
          command=self.syntax.syntax_and_themes.load_coffeescript_syntax)
        syntax_dropdown.add_command(
          label='CSS',
          command=self.syntax.syntax_and_themes.load_css_syntax)
        syntax_dropdown.add_command(
          label='Dart',
          command=self.syntax.syntax_and_themes.load_dart_syntax)
        syntax_dropdown.add_command(
          label='Dockerfile',
          command=self.syntax.syntax_and_themes.load_docker_syntax)
        syntax_dropdown.add_command(
          label='Haskell',
          command=self.syntax.syntax_and_themes.load_haskell_syntax)
        syntax_dropdown.add_command(
          label='HTML/Django',
          command=self.syntax.syntax_and_themes.load_html_syntax)
        syntax_dropdown.add_command(
          label='JavaScript',
          command=self.syntax.syntax_and_themes.load_javascript_syntax)
        syntax_dropdown.add_command(
          label='Java',
          command=self.syntax.syntax_and_themes.load_java_syntax)
        syntax_dropdown.add_command(
          label='Go',
          command=self.syntax.syntax_and_themes.load_go_syntax)
        syntax_dropdown.add_command(
          label='Markdown',
          command=self.syntax.syntax_and_themes.load_markdown_syntax)
        syntax_dropdown.add_command(
          label='Nim',
          command=self.syntax.syntax_and_themes.load_nim_syntax)
        syntax_dropdown.add_command(
          label='Python3',
          command=self.syntax.syntax_and_themes.load_python3_syntax)
        syntax_dropdown.add_command(
          label='Rust',
          command=self.syntax.syntax_and_themes.load_rust_syntax)
        syntax_dropdown.add_command(
          label='SQL',
          command=self.syntax.syntax_and_themes.load_sql_syntax)
        syntax_dropdown.add_command(
          label='Swift',
          command=self.syntax.syntax_and_themes.load_swift_syntax)
        syntax_dropdown.add_command(
          label='Yaml',
          command=self.syntax.syntax_and_themes.load_yaml_syntax)

        build_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        build_dropdown.add_command(
          label='Build',
          command=self.build)
        build_dropdown.add_command(
          label='Run',
          accelerator='Ctrl+R',
          command=self.run)
        build_dropdown.add_command(
          label='Build+Run',
          command=self.build_run)

        # menubar add buttons
        menubar.add_cascade(label='File', menu=file_dropdown)
        menubar.add_cascade(label='View', menu=view_dropdown)
        menubar.add_cascade(label='Settings', menu=settings_dropdown)
        menubar.add_cascade(label='Tools', menu=tools_dropdown)
        menubar.add_cascade(label='Syntax', menu=syntax_dropdown)
        menubar.add_cascade(label='Themes', menu=theme_dropdown)
        menubar.add_cascade(label='Build Options', menu=build_dropdown)
        
        self.menu_fields = [field for field in (
            file_dropdown, view_dropdown, syntax_dropdown, build_dropdown,
            settings_dropdown, tools_dropdown, theme_dropdown)]

    # Settings reconfiguration function
    def reconfigure_settings(self):
        settings = self._parent.loader.load_settings_data()
        for field in self.menu_fields:
            field.configure(
                bg=settings['menu_bg'],
                fg=settings['menu_fg'],
                activeforeground=settings['menu_active_fg'],
                activebackground=settings['menu_active_bg'],
                background = settings['textarea_background_color'],)

        self._menubar.configure(
            bg=settings['menu_bg'],
            fg=settings['menu_fg'],
            background = settings['textarea_background_color'],
            activeforeground= settings['menubar_active_fg'],
            activebackground= settings['menubar_active_bg'],)

    # color to different text tye can be set here
    def open_color_picker(self):
        return askcolor(title='Color Menu', initialcolor='#d5c4a1')[1]

    def toggle_text_border(self):
        settings = self._parent.loader.load_settings_data()
        border_status = settings['textarea_border']
        if border_status == 0:
          self._parent.textarea.configure(bd=0.5)
          settings['textarea_border'] = 0.5
        elif border_status > 0:
          self._parent.textarea.configure(bd=0)
          settings['textarea_border'] = 0
        self._parent.loader.store_settings_data(settings)

    def toggle_scroll_x(self):
        settings = self._parent.loader.load_settings_data()
        scrollx_width = settings['horizontal_scrollbar_width']
        if scrollx_width > 0:
          self._parent.scrollx.configure(width=0)
          settings['horizontal_scrollbar_width'] = 0
        elif scrollx_width == 0:
          self._parent.scrollx.configure(width=8)
          settings['horizontal_scrollbar_width'] = 8
        self._parent.loader.store_settings_data(settings)

    def toggle_scroll_y(self):
        settings = self._parent.loader.load_settings_data()
        scrolly_width = settings['vertical_scrollbar_width']
        if scrolly_width > 0:
          self._parent.scrolly.configure(width=0)
          settings['vertical_scrollbar_width'] = 0
        elif scrolly_width == 0:
          self._parent.scrolly.configure(width=8)
          settings['vertical_scrollbar_width'] = 8
        self._parent.loader.store_settings_data(settings)

    # quiet mode is defined here
    def enter_quiet_mode(self):
        self._parent.enter_quiet_mode()

    # hiding the menubar
    def hide_menu(self):
        self._parent.master.config(menu='')

    # display the menubar
    def show_menu(self):
        self._parent.master.config(menu=self._menubar)

    def base_cmd(self, command):
        if self._parent.operating_system == 'Windows':
            cmd = f'start cmd.exe @cmd /k {command}'
        elif self._parent.operating_system == 'Linux':
            cmd = f"gnome-terminal -- bash -c '{command}; read'"
        file_from_path = re.search(self.ptrn, self._parent.filename)
        filename = file_from_path.group(0)
        file_path = self._parent.filename[:-len(filename)]
        os.chdir(file_path)
        os.system(cmd)

    def build(self):
        try:
            file_from_path = re.search(self.ptrn, self._parent.filename)
            filename = file_from_path.group(0)
            if filename[-3:] == '.go':
                self.base_cmd(f'go build {self._parent.filename}')
            elif filename[-2:] == '.c':
                compiled_name = filename[:-2]
                self.base_cmd(f'cc {filename} -o {compiled_name}')
            elif filename[-4:] == '.cpp':
                compiled_name = filename[:-4]
                self.base_cmd(f'g++ -o {compiled_name} {filename}')
            elif filename[-5:] == '.java':
                compiled_name = filename[:-5]
                self.base_cmd(f'javac {filename}')
            elif filename[-3:] == '.rs':
                self.base_cmd(f'rustc {filename}')
            elif filename[-3:] == '.hs':
                compiled_name = filename[:-3]
                self.base_cmd(f'ghc -o {compiled_name} {filename}')
            else:
                self._parent.statusbar.update_status('cant build')
        except TypeError:
            self._parent.statusbar.update_status('cant build')

    def run(self, *args):
        try:
            file_from_path = re.search(self.ptrn, self._parent.filename)
            filename = file_from_path.group(0)
            if filename[-3:] == '.py':
                self.base_cmd(f'python {self._parent.filename}')
            elif filename[-5:] == '.html':
                self.base_cmd(f'{self._parent.browser} {filename}')
            elif filename[-3:] == '.js':
                self.base_cmd(f'node {self._parent.filename}')
            elif filename[-3:] == '.go':
                self.base_cmd(f'go run {self._parent.filename}')
            elif filename[-2:] == '.c':
                compiled_name = filename[:-2]
                self.base_cmd(f'{compiled_name}')
            elif filename[-4:] == '.cpp':
                compiled_name = filename[:-4]
                self.base_cmd(f'{compiled_name}')
            elif filename[-5:] == '.java':
                compiled_name = filename[:-5]
                self.base_cmd(f'java {compiled_name}')
            elif filename[-3:] == '.rs':
                compiled_name = filename[:-3]
                self.base_cmd(f'{compiled_name}')
            elif filename[-4:] == '.nim':
                self.base_cmd(f'nim c -r {filename}')
            elif filename[-3:] == '.hs':
                compiled_name = filename[:-3]
                self.base_cmd(f'{compiled_name}')
            else:
                self._parent.statusbar.update_status('no python')
        except TypeError as e:
            print(e)
            self._parent.statusbar.update_status('no file run')

    def build_run(self):
        self.build()
        sleep(.5)
        self.run()