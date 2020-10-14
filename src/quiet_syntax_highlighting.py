import tkinter as tk
import math
import yaml
import tkinter.font as tk_font
from pygments import lex
from pygments.lexers import get_lexer_by_name

class SyntaxHighlighting():

    def __init__(self, parent, text_widget, initial_content):
        self.settings = parent.loader.load_settings_data()
        self.syntax = parent.loader.load_default_syntax()
        self.default_theme = parent.loader.load_default_theme()

        self.parent = parent
        self.text = text_widget
        self.font_family = parent.font_family
        self.font_size = parent.font_size
        self.previousContent = initial_content
        self.lexer = get_lexer_by_name('python')

        self.comment_tokens = self.syntax['comments']
        self.string_tokens = self.syntax['strings']
        self.number_tokens = self.syntax['numbers']
        self.keyword_tokens = self.syntax['keywords']
        self.function_tokens = self.syntax['functions']
        self.class_tokens = self.syntax['class_self']
        self.object_tokens = self.syntax['object_names']
        self.text_tokens = self.syntax['text']

        self.comment_color = self.default_theme['comment_color']
        self.string_color = self.default_theme['string_color']
        self.number_color = self.default_theme['number_color']
        self.keyword_color = self.default_theme['keyword_color']
        self.function_color = self.default_theme['function_color']
        self.class_color = self.default_theme['class_self_color']
        self.object_color = self.default_theme['object_color']
        self.text_color = parent.font_color


    def default_highlight(self):
        row = float(self.text.index(tk.INSERT))
        row = str(math.trunc(row))
        content = self.text.get("1.0", tk.END)
        lines = content.split("\n")

        if (self.previousContent != content):
            self.text.mark_set("range_start", row + ".0")
            data = self.text.get(row + ".0", row + "." + str(len(lines[int(row) - 1])))

            for token, content in lex(data, self.lexer):
                self.text.mark_set("range_end", "range_start + %dc" % len(content))
                self.text.tag_add(str(token), "range_start", "range_end")
                self.text.mark_set("range_start", "range_end")

        self.previousContent = self.text.get("1.0", tk.END)

    def syntax_theme_configuration(self):
        def configure_tokens(tokens, token_color):
            if tokens:
                for token in tokens:
                    self.text.tag_configure(token, foreground=token_color)
        configure_tokens(self.comment_tokens, self.comment_color)
        configure_tokens(self.string_tokens, self.string_color)
        configure_tokens(self.number_tokens, self.number_color)
        configure_tokens(self.keyword_tokens, self.keyword_color)
        configure_tokens(self.function_tokens, self.function_color)
        configure_tokens(self.object_tokens, self.object_color)
        configure_tokens(self.text_tokens, self.text_color)
        if self.class_tokens:
            for token in self.class_tokens:
                self.text.tag_configure(token, foreground=self.class_color, font=self.parent.italics, size=self.font_size)


    def initial_highlight(self, *args):
        for tag in self.text.tag_names():
            self.text.tag_delete(tag)

        content = self.text.get("1.0", tk.END)
        self.text.mark_set("range_start", "1.0")
        data = self.text.get("1.0", tk.END)
        for token, content in lex(data, self.lexer):
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
        self.text_color = new_config['font_color']
        
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

        self.initial_highlight()


    def load_new_tokens(self, new_syntax):
        self.comment_tokens = new_syntax['comments']
        self.string_tokens = new_syntax['strings']
        self.number_tokens = new_syntax['numbers']
        self.keyword_tokens = new_syntax['keywords']
        self.function_tokens = new_syntax['functions']
        self.class_tokens = new_syntax['class_self']
        self.object_tokens = new_syntax['object_names']
        self.text_tokens = new_syntax['text']
        self.initial_highlight()

    def load_python3_syntax(self):
        new_syntax = self.parent.loader.load_python3_syntax()
        self.lexer = get_lexer_by_name('python')
        self.load_new_tokens(new_syntax)

    def load_c_syntax(self):
        new_syntax = self.parent.loader.load_c_syntax()
        self.lexer = get_lexer_by_name('c')
        self.load_new_tokens(new_syntax)

    def load_javascript_syntax(self):
        new_syntax = self.parent.loader.load_javascript_syntax()
        self.lexer = get_lexer_by_name('javascript')
        self.load_new_tokens(new_syntax)





