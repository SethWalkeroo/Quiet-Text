import tkinter as tk
import math
import yaml
import tkinter.font as tk_font
from pygments import lex
from pygments.lexers import PythonLexer, CLexer, JavascriptLexer

class SyntaxHighlighting():

    def __init__(self, parent, text_widget, initial_content):
        self.settings = parent.loader.load_settings_data()
        self.syntax = parent.loader.load_default_syntax()
        self.theme = parent.loader.load_default_theme()

        self.parent = parent
        self.text = text_widget
        self.font_family = self.parent.font_family
        self.font_size = self.parent.font_size
        self.previousContent = initial_content
        self.lexer = PythonLexer

        self.comment_tokens = self.syntax['comments']
        self.string_tokens = self.syntax['strings']
        self.number_tokens = self.syntax['numbers']
        self.keyword_tokens = self.syntax['keywords']
        self.function_tokens = self.syntax['functions']
        self.class_tokens = self.syntax['class_self']
        self.object_tokens = self.syntax['object_names']

        self.comment_color = self.theme['comment_color']
        self.string_color = self.theme['string_color']
        self.number_color = self.theme['number_color']
        self.keyword_color = self.theme['keyword_color']
        self.function_color = self.theme['function_color']
        self.class_color = self.theme['class_self_color']
        self.object_color = self.theme['object_color']


    def default_highlight(self):
        row = float(self.text.index(tk.INSERT))
        row = str(math.trunc(row))
        content = self.text.get("1.0", tk.END)
        lines = content.split("\n")

        if (self.previousContent != content):
            self.text.mark_set("range_start", row + ".0")
            data = self.text.get(row + ".0", row + "." + str(len(lines[int(row) - 1])))

            for token, content in lex(data, self.lexer()):
                print(token)
                self.text.mark_set("range_end", "range_start + %dc" % len(content))
                self.text.tag_add(str(token), "range_start", "range_end")
                self.text.mark_set("range_start", "range_end")

        self.previousContent = self.text.get("1.0", tk.END)

    def syntax_theme_configuration(self):
        for token in self.comment_tokens:
            self.text.tag_configure(token, foreground=self.comment_color)
        for token in self.string_tokens:
            self.text.tag_configure(token, foreground=self.string_color)
        for token in self.number_tokens:
            self.text.tag_configure(token, foreground=self.number_color)
        for token in self.keyword_tokens:
            self.text.tag_configure(token, foreground=self.keyword_color)
        for token in self.function_tokens:
            self.text.tag_configure(token, foreground=self.function_color)
        for token in self.class_tokens:
            self.text.tag_configure(token, foreground=self.class_color, font=self.parent.italics, size=self.font_size)
        for token in self.object_tokens:
            self.text.tag_configure(token, foreground=self.object_color)

    def initial_highlight(self, *args):
        content = self.text.get("1.0", tk.END)

        self.text.mark_set("range_start", "1.0")

        data = self.text.get("1.0", tk.END)
        for token, content in lex(data, PythonLexer()):
            print(token)
            self.text.mark_set("range_end", "range_start + %dc" % len(content))
            self.text.tag_add(str(token), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")
            
        self.previousContent = self.text.get("1.0", tk.END)
        self.syntax_theme_configuration()


    def load_new_theme(self, path):

        with open(path) as new_theme_config:
            new_config = yaml.load(new_theme_config, Loader=yaml.FullLoader)

        self.comment_color = new_config['comment_color']
        self.string_color = new_config['string_color']
        self.number_color = new_config['number_color']
        self.keyword_color = new_config['keyword_color']
        self.function_color = new_config['function_color']
        self.class_color = new_config['class_self_color']
        self.object_color = new_config['object_color']
        
        # object_color determines the color of both function names
        #  and class names. This allows themes to set them independently
        # while not breaking existing themes.
        if 'function_name_color' in new_config:
            self.function_name_color = new_config['function_name_color']
        else:
            self.function_name_color = self.object_color
        
        settings = self.parent.loader.load_settings_data()
        settings['menu_fg'] = new_config['comment_color']
        settings['menu_bg'] = new_config['bg_color']
        settings['font_color'] = new_config['font_color']
        settings['textarea_background_color'] = new_config['bg_color']
        settings['menubar_active_bg'] = new_config['menu_bg_active']
        settings['menubar_active_fg'] = new_config['menu_fg_active']  
        settings['menu_active_bg'] = new_config['menu_bg_active']
        settings['menu_active_fg'] = new_config['menu_fg_active']  
        self.parent.loader.store_settings_data(settings)

        self.parent.reconfigure_settings()
        self.syntax_theme_configuration()
        self.initial_highlight()

    def load_new_syntax(self, syntax):
        pass



