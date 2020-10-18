import tkinter as tk
import yaml
import os, sys
import re
from tkinter.colorchooser import askcolor
from quiet_syntax_highlighting import SyntaxHighlighting


class Menubar():
    # initialising the menu bar of editor
    def __init__(self, parent):
        self.current_theme = None
        self._parent = parent
        self.syntax = parent.syntax_highlighter
        self.default_theme = parent.loader.load_default_theme()
        self.settings = parent.loader.load_settings_data()
        self.settings['menubar_active_bg'] = self.default_theme['menu_bg_active']
        self.settings['menubar_active_fg'] = self.default_theme['menu_fg_active']
        self.settings['menu_fg'] = self.default_theme['comment_color']
        self.settings['menu_bg'] = self.default_theme['bg_color']
        font_specs = ('Droid Sans Fallback', 12)

        self.monokaipro_theme_path = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/monokai_pro.yaml'))
        self.monokai_theme_path = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/monokai.yaml'))
        self.gruvbox_theme_path = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/gruvbox.yaml'))
        self.solarized_theme_path = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/solarized.yaml'))
        self.darkheart_theme_path = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/dark-heart.yaml'))
        self.githubly_theme_path = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/githubly.yaml'))
        self.dracula_theme_path = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/dracula.yaml'))
        self.pumpkin_theme_path = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/pumpkin.yaml'))
        self.material_theme_path = self._parent.loader.resource_path(os.path.join('data', 'theme_configs/material.yaml'))
        # setting up basic features in menubar
        menubar = tk.Menu(parent.master,
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
        # exit feature
        file_dropdown.add_separator()
        file_dropdown.add_command(label='Exit',
                                  command=parent.on_closing)

        # adding featues to settings dropdown in menubar
        # Edit settings feature
        settings_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        settings_dropdown.add_command(label='Edit Settings',
                                      command=parent.open_settings_file)
        # reset settings feature
        settings_dropdown.add_command(label='Reset Settings to Default',
                                      command=parent.reset_settings_file)

        #view dropdown menu
        view_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        view_dropdown.add_command(label='Toggle Menu Bar',
                                  accelerator='Alt',
                                  command=self.hide_menu)
        view_dropdown.add_command(label='Hide Status Bar',
                                  command=parent.hide_status_bar)
        view_dropdown.add_command(label='Toggle Line Numbers',
                                  accelerator='Ctrl+Shift+L',
                                  command=parent.toggle_linenumbers)
        view_dropdown.add_command(label='Toggle Text Border',
                                  command=self.toggle_text_border)
        view_dropdown.add_command(label='Toggle Horizontal Scrollbar',
                                  command=self.toggle_scroll_x)
        view_dropdown.add_command(label='Toggle Vertical Scrollbar',
                                  command=self.toggle_scroll_y)
        view_dropdown.add_command(label='Enter Quiet Mode',
                                  accelerator='Ctrl+Q',
                                  command=self.enter_quiet_mode)

        #tools dropdown menu
        tools_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        tools_dropdown.add_command(label='Open Color Selector',
                                   accelerator='Ctrl+M',
                                   command=self.open_color_picker)

        #theme dropdown menu
        theme_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        theme_dropdown.add_command(label='Monokai',
                                   command=self.load_monokai)
        theme_dropdown.add_command(label='Monokai Pro',
                                   command=self.load_monokai_pro)
        theme_dropdown.add_command(label='Material',
                                   command=self.load_material)
        theme_dropdown.add_command(label='Gruvbox',
                                   command=self.load_gruvbox)
        theme_dropdown.add_command(label='Solarized',
                                   command=self.load_solarized)
        theme_dropdown.add_command(label='Dark Heart',
                                   command=self.load_darkheart)
        theme_dropdown.add_command(label='Githubly',
                                   command=self.load_githubly)
        theme_dropdown.add_command(label='Dracula',
                                   command=self.load_dracula)
        theme_dropdown.add_command(label='Pumpkin',
                                   command=self.load_pumpkin)
        theme_dropdown.add_command(label='Set Current Theme as Default',
                                   command=self.set_default_theme)


        syntax_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        syntax_dropdown.add_command(label='Markdown',
                                    command=self.syntax.load_markdown_syntax)
        syntax_dropdown.add_command(label='Python3',
                                    command=self.syntax.load_python3_syntax)
        syntax_dropdown.add_command(label='HTML',
                                    command=self.syntax.load_html_syntax)
        syntax_dropdown.add_command(label='CSS',
                                    command=self.syntax.load_css_syntax)
        syntax_dropdown.add_command(label='JavaScript',
                                    command=self.syntax.load_javascript_syntax)
        syntax_dropdown.add_command(label='C',
                                    command=self.syntax.load_c_syntax)
        syntax_dropdown.add_command(label='C++',
                                    command=self.syntax.load_cpp_syntax)
        syntax_dropdown.add_command(label='Go',
                                    command=self.syntax.load_go_syntax)
        syntax_dropdown.add_command(label='Yaml',
                                    command=self.syntax.load_yaml_syntax)

        build_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        build_dropdown.add_command(label='Build',
                                   comman=self.build)
        build_dropdown.add_command(label='Run',
                                   accelerator='Ctrl+R',
                                   command=self.run)
        build_dropdown.add_command(label='Build+Run',
                                   command=self.build_run)

        # menubar add buttons
        menubar.add_cascade(label='File', menu=file_dropdown)
        menubar.add_cascade(label='View', menu=view_dropdown)
        menubar.add_cascade(label='Settings', menu=settings_dropdown)
        menubar.add_cascade(label='Tools', menu=tools_dropdown)
        menubar.add_cascade(label='Syntax', menu=syntax_dropdown)
        menubar.add_cascade(label='Themes', menu=theme_dropdown)
        menubar.add_cascade(label='Build Options', menu=build_dropdown)
        # menubar.add_cascade(label='About', menu=about_dropdown)

        self.menu_fields = [field for field in (file_dropdown, view_dropdown, syntax_dropdown, build_dropdown,
                                                settings_dropdown, tools_dropdown, theme_dropdown)]

        self.default_settings = parent.default_theme
        for field in self.menu_fields:
            field.configure(bg=parent.default_theme['bg_color'],
                            fg=self.settings['menu_fg'],
                            activeforeground=parent.default_theme['menu_fg_active'],
                            activebackground=parent.default_theme['menu_bg_active'])

        # Settings reconfiguration function
    def reconfigure_settings(self):
        settings = self._parent.loader.load_settings_data()
        for field in self.menu_fields:
            field.configure(bg=settings['menu_bg'],
                            fg=settings['menu_fg'],
                            activeforeground=settings['menu_active_fg'],
                            activebackground=settings['menu_active_bg'],
                            background = settings['textarea_background_color'],)

        self._menubar.configure(bg=settings['menu_bg'],
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


    def build(self, *args):
        try:
            ptrn = r'[^\/]+$'
            file_from_path = re.search(ptrn, self._parent.filename)
            filename = file_from_path.group(0)
            file_path = self._parent.filename[:-len(filename)]
            if filename[-3:] == '.go':
                if self._parent.operating_system == 'Linux':
                    build = f"gnome-terminal -- bash -c 'go build {self._parent.filename}; read'"
                elif self._parent.operating_system == 'Windows':
                    build = f'start cmd.exe @cmd /k "go build {self._parent.filename}"'
                os.system(build)
            elif filename[-2:] == '.c':
                compiled_name = filename[:-2]
                if self._parent.operating_system == 'Linux':
                    compile_cmd = f"gnome-terminal -- bash -c 'cd {file_path}; cc {filename} -o {compiled_name}; read'"
                elif self._parent.operating_system == 'Windows':
                    compile_cmd = f'start cmd.exe @cmd /k "cd {file_path}; cc {filename} -o {compiled_name}"'
                os.system(compile_cmd)
            elif filename[-4:] == '.cpp':
                compiled_name = filename[:-4]
                if self._parent.operating_system == 'Linux':
                    compile_cmd = f"gnome-terminal -- bash -c 'cd {file_path}; g++ -o {compiled_name} {filename}; read'"
                elif self._parent.operating_system == 'Windows':
                    compile_cmd = f"start cmd.exe @cmd /k 'cd {file_path}; g++ -o {compiled_name} {filename}'"
                os.system(compile_cmd)
            else:
                self._parent.statusbar.update_status('no python')
        except TypeError:
            self._parent.statusbar.update_status('no file run')



    def run(self, *args):
        try:
            ptrn = r'[^\/]+$'
            file_from_path = re.search(ptrn, self._parent.filename)
            filename = file_from_path.group(0)
            file_path = self._parent.filename[:-len(filename)]
            if self._parent.filename[-3:] == '.py':
                #run separate commands for different os
                if self._parent.operating_system == 'Windows':
                    cmd = f'start cmd.exe @cmd /k "python {self._parent.filename}"'
                elif self._parent.operating_system == 'Linux':
                    cmd = f"gnome-terminal -- bash -c 'python3 {self._parent.filename}; read'"
                os.system(cmd)
            elif self._parent.filename[-5:] == '.html':
                if self._parent.operating_system == 'Linux':
                    cmd = f"gnome-terminal -- bash -c '{self._parent.browser} {self._parent.filename}; read'"
                elif self._parent.operating_system == 'Windows':
                    cmd = f'start cmd.exe @cmd /k "{self._parent.browser} {self._parent.filename}"'
                os.system(cmd)
            elif self._parent.filename[-3:] == '.js':
                if self._parent.operating_system == 'Linux':
                    cmd = f"gnome-terminal -- bash -c 'node {self._parent.filename}; read'"
                elif self._parent.operating_system == 'Windows':
                    cmd = f'start cmd.exe @cmd /k " node {self._parent.filename}"'
                os.system(cmd)
            elif self._parent.filename[-3:] == '.go':
                if self._parent.operating_system == 'Linux':
                    cmd = f"gnome-terminal -- bash -c 'go run {self._parent.filename}; read'"
                elif self._parent.operating_system == 'Windows':
                    cmd = f'start cmd.exe @cmd /k "go run {self._parent.filename}"'
                os.system(cmd)
            elif self._parent.filename[-2:] == '.c':
                compiled_name = filename[:-2]
                if self._parent.operating_system == 'Linux':
                    run_cmd = f"gnome-terminal -- bash -c 'cd {file_path}; ./{compiled_name}; read'"
                elif self._parent.operating_system == 'Windows':
                    run_cmd = f"start cmd.exe @cmd /k 'cd {file_path}; ./{compiled_name}'"
                os.system(run_cmd)
            elif self._parent.filename[-4:] == '.cpp':
                compiled_name = filename[:-4]
                if self._parent.operating_system == 'Linux':
                    run_cmd = f"gnome-terminal -- bash -c 'cd {file_path}; ./{compiled_name}; read'"
                elif self._parent.operating_system == 'Windows':
                    run_cmd = f"start cmd.exe @cmd /k 'cd {file_path}; ./{compiled_name}'"
                os.system(run_cmd)
            else:
                self._parent.statusbar.update_status('no python')
        except TypeError:
            self._parent.statusbar.update_status('no file run')

    # running the python file
    def build_run(self, *args):
        try:
            ptrn = r'[^\/]+$'
            file_from_path = re.search(ptrn, self._parent.filename)
            filename = file_from_path.group(0)
            file_path = self._parent.filename[:-len(filename)]
            if filename[-3:] == '.go':
                compiled_name = filename[:-3]
                if self._parent.operating_system == 'Linux':
                    build = f"gnome-terminal -- bash -c 'go build {self._parent.filename}; read'"
                    run = f"gnome-terminal -- bash -c 'cd {file_path}; ./{compiled_name}; read'"
                elif self._parent.operating_system == 'Windows':
                    build = f'start cmd.exe @cmd /k "go build {self._parent.filename}"'
                    run = f'start cmd.exe @cmd /k "./{compiled_name}"'
                os.system(build)
                os.system(run)
            elif filename[-2:] == '.c':
                compiled_name = filename[:-2]
                if self._parent.operating_system == 'Linux':
                    compile_cmd = f"gnome-terminal -- bash -c 'cd {file_path}; cc {filename} -o {compiled_name}; read'"
                    run_cmd = f"gnome-terminal -- bash -c 'cd {file_path}; ./{compiled_name}; read'"
                elif self._parent.operating_system == 'Windows':
                    compile_cmd = f'start cmd.exe @cmd /k "cd {file_path}; cc {filename} -o {compiled_name}"'
                    run_cmd = f"start cmd.exe @cmd /k 'cd {file_path}; ./{compiled_name}'"
                os.system(compile_cmd)
                os.system(run_cmd)
            elif filename[-4:] == '.cpp':
                compiled_name = filename[:-4]
                if self._parent.operating_system == 'Linux':
                    compile_cmd = f"gnome-terminal -- bash -c 'cd {file_path}; g++ -o {compiled_name} {filename}; read'"
                    run_cmd = f"gnome-terminal -- bash -c 'cd {file_path}; ./{compiled_name}; read'"
                elif self._parent.operating_system == 'Windows':
                    compile_cmd = f"start cmd.exe @cmd /k 'cd {file_path}; g++ -o {compiled_name} {filename}'"
                    run_cmd = f"start cmd.exe @cmd /k 'cd {file_path}; ./{compiled_name}'"
                os.system(compile_cmd)
                os.system(run_cmd)
            else:
                self._parent.statusbar.update_status('no python')
        except TypeError:
            self._parent.statusbar.update_status('no file run')


    def set_default_theme(self):
        themes = {'monokai pro':self.monokaipro_theme_path,
                  'monokai':self.monokai_theme_path,
                  'gruvbox':self.gruvbox_theme_path,
                  'solarized':self.solarized_theme_path,
                  'darkheart':self.darkheart_theme_path,
                  'githubly':self.githubly_theme_path,
                  'dracula':self.dracula_theme_path,
                  'pumpkin':self.pumpkin_theme_path,
                  'material':self.material_theme_path}
        new_default_theme_path = themes[self.current_theme]
        with open(new_default_theme_path, 'r') as new_theme_data:
            new_theme = yaml.load(new_theme_data, Loader=yaml.FullLoader)
        with open(self._parent.loader.default_theme_path, 'w') as default_theme:
            yaml.dump(new_theme, default_theme)


    def load_monokai_pro(self):
        self.syntax.load_new_theme(self.monokaipro_theme_path)
        self.current_theme = 'monokai pro'

    def load_monokai(self):
        self.syntax.load_new_theme(self.monokai_theme_path)
        self.current_theme = 'monokai'

    def load_gruvbox(self):
        self.syntax.load_new_theme(self.gruvbox_theme_path)
        self.current_theme = 'gruvbox'

    def load_solarized(self):
        self.syntax.load_new_theme(self.solarized_theme_path)
        self.current_theme = 'solarized'

    def load_darkheart(self):
        self.syntax.load_new_theme(self.darkheart_theme_path)
        self.current_theme = 'darkheart'

    def load_githubly(self):
        self.syntax.load_new_theme(self.githubly_theme_path)
        self.current_theme = 'githubly'

    def load_dracula(self):
        self.syntax.load_new_theme(self.dracula_theme_path)
        self.current_theme = 'dracula'

    def load_pumpkin(self):
        self.syntax.load_new_theme(self.pumpkin_theme_path)
        self.current_theme = 'pumpkin'

    def load_material(self):
        self.syntax.load_new_theme(self.material_theme_path)
        self.current_theme = 'material'
