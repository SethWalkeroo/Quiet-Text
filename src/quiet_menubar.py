import tkinter as tk
import yaml
from tkinter.colorchooser import askcolor
from quiet_zutilityfuncs import load_settings_data
from quiet_syntax_highlighting import SyntaxHighlighting

class Menu(tk.Menu):
    # menu method and its initializatipn from config/settings.yaml
    def __init__(self, *args, **kwargs):
        settings = load_settings_data()
        super().__init__(bg=settings["menu_bg"],
                         activeforeground=settings['menu_active_fg'],
                         activebackground=settings['menu_active_bg'],
                         foreground='#458588',
                         background = '#1d2021',
                         activeborderwidth=0,
                         bd=0,
                         *args, **kwargs)

class Menubar:
    # initialising the menu bar of editor
    def __init__(self, parent):
        self._parent = parent
        self.syntax = parent.syntax_highlighter
        font_specs = ('Droid Sans Fallback', 12)

        # setting up basic features in menubar
        menubar = tk.Menu(parent.master,
                          font=font_specs,
                          fg='#458588',
                          bg='#1d2021',
                          activeforeground='#83a598',
                          activebackground='#282828',
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
                                   accelerator='Ctrl+Shift+S',
                                   command=parent.save_as)
        # exit feature
        file_dropdown.add_separator()
        file_dropdown.add_command(label='Exit', 
                                  command=parent.on_closing)

        # adding featues to settings dropdown in menubar
        # Edit settings feature
        settings_dropdown = Menu(menubar, font=font_specs, tearoff=0)
        settings_dropdown.add_command(label='Edit Settings',
                                      command=parent.open_settings_file)
        # reset settings feature
        settings_dropdown.add_command(label='Reset Settings to Default',
                                      command=parent.reset_settings_file)

        #view dropdown menu
        view_dropdown = Menu(menubar, font=font_specs, tearoff=0)
        view_dropdown.add_command(label='Hide Menu Bar',
                                  accelerator='Alt',
                                  command=self.hide_menu)

        view_dropdown.add_command(label='Hide Status Bar',
                                  command=parent.hide_status_bar)
        
        view_dropdown.add_command(label='Toggle Line Numbers',
                                  accelerator='Ctrl+Shift+L',
                                  command=parent.toggle_linenumbers)

        view_dropdown.add_command(label='Enter Quiet Mode',
                                  accelerator='Ctrl+Q',
                                  command=self.enter_quiet_mode)

        #tools dropdown menu
        tools_dropdown = Menu(menubar, font=font_specs, tearoff=0)
        tools_dropdown.add_command(label='Open Color Selector',
                                   accelerator='Ctrl+M',
                                   command=self.open_color_picker)

        tools_dropdown.add_command(label='Run Selected File',
                                   accelerator='Ctrl+R',
                                   command=parent.run)

        #syntax dropdown menu
        syntax_dropdown = Menu(menubar, font=font_specs, tearoff=0)
        syntax_dropdown.add_command(label='Monokai',
                                    command=self.load_monokai)

        syntax_dropdown.add_command(label='Monokai Pro',
                                    command=self.load_monokai_pro)

        syntax_dropdown.add_command(label='Gruvbox',
                                    command=self.load_gruvbox)

        syntax_dropdown.add_command(label='Solarized',
                                    command=self.load_solarized)

        # menubar add buttons
        menubar.add_cascade(label='File', menu=file_dropdown)
        menubar.add_cascade(label='View', menu=view_dropdown)
        menubar.add_cascade(label='Settings', menu=settings_dropdown)
        menubar.add_cascade(label='Tools', menu=tools_dropdown)
        menubar.add_cascade(label='Color Schemes', menu=syntax_dropdown)
        # menubar.add_cascade(label='About', menu=about_dropdown)
        
        self.menu_fields = [field for field in (file_dropdown, view_dropdown, settings_dropdown, tools_dropdown)]

        # Settings reconfiguration function
    def reconfigure_settings(self):
        with open('config/settings.yaml', 'r') as settings_yaml:
            settings = yaml.load(settings_yaml, Loader=yaml.FullLoader)
        for field in self.menu_fields:
            field.configure(bg=settings['menu_bg'],
                            activeforeground=settings['menu_active_fg'],
                            activebackground=settings['menu_active_bg'],)

    # color to different text tye can be set here
    def open_color_picker(self):
        return askcolor(title='Color Menu', initialcolor='#d5c4a1')[1]

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

    def load_monokai_pro(self):
        self.syntax.load_new_theme('theme_configs/Python3/monokai_pro.yaml')

    def load_monokai(self):
        self.syntax.load_new_theme('theme_configs/Python3/monokai.yaml')

    def load_gruvbox(self):
        self.syntax.load_new_theme('theme_configs/Python3/gruvbox.yaml')

    def load_solarized(self):
        self.syntax.load_new_theme('theme_configs/Python3/solarized.yaml')


