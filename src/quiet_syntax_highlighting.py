import tkinter as tk
import math
import yaml
import tkinter.font as tk_font
from pygments import lex
from pygments.lexers import PythonLexer, CLexer, JavascriptLexer
from quiet_zutilityfuncs import load_settings_data

class SyntaxHighlighting():

    def __init__(self, parent, text_widget, initial_content):
        self.settings = load_settings_data()

        self.parent = parent
        self.text = text_widget
        self.font_family = self.parent.font_family
        self.font_size = self.parent.font_size
        self.previousContent = initial_content
        self.lexer = PythonLexer

        self.comment_tokens = [
            "Token.Comment.Single",
        ]
        self.string_tokens = [
            "Token.Name.Function",
            "Token.Name.Class",
            "Token.String",
            "Token.Literal.String.Single",
            "Token.Literal.String.Double"
        ]
        self.object_tokens = [
            "Token.Name.Class",
            "Token.Name.Function",
        ]
        self.number_tokens = [
            "Token.Keyword.Constant",
            "Token.Literal.String.Interpol",
            "Token.Literal.Number.Integer",
            "Token.Literal.Number.Float",
            "Token.Name.Decorator",
        ]
        self.keyword_tokens = [
            "Token.Operator",
            "Token.Operator.Word",
            "Token.Keyword.Namespace",
        ]
        self.function_tokens = [
            "Token.Keyword",
            "Token.Name.Builtin",
            "Token.Literal.String.Affix",
            "Token.Name.Function.Magic",
        ]
        self.class_tokens = [
            "Token.Name.Builtin.Pseudo",
        ]
        self.variable_tokens = [
            "Token.Name.Namespace",
        ]

        self.comment_color = '#928374'
        self.string_color = '#b8bb26'
        self.number_color = '#d3869b'
        self.keyword_color = '#fe8019'
        self.function_color = '#8ec87c'
        self.class_color = '#d3869b'
        self.object_color = '#b8bb26'

    def default_highlight(self):
        row = float(self.text.index(tk.INSERT))
        row = str(math.trunc(row))
        content = self.text.get("1.0", tk.END)
        lines = content.split("\n")

        if (self.previousContent != content):
            self.text.mark_set("range_start", row + ".0")
            data = self.text.get(row + ".0", row + "." + str(len(lines[int(row) - 1])))

            for token, content in lex(data, self.lexer()):
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
        self.class_color = new_config['class_color']
        self.object_color = new_config['object_color']

        self.syntax_theme_configuration()
        self.initial_highlight()


