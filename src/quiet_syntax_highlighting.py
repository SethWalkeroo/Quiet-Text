import tkinter as tk
import math
import tkinter.font as tk_font
from pygments import lex
from pygments.lexers import PythonLexer
from quiet_zutilityfuncs import load_settings_data, load_default_syntax

class PythonSyntaxHighlight():

    def __init__(self, parent, text_widget, initial_content):
        self.settings = load_settings_data()
        self.syntax = load_default_syntax()
        # lexer = get_lexer_by_name('python')
        self.parent = parent
        self.text = text_widget
        self.font_family = self.parent.font_family
        self.font_size = self.parent.font_size
        self.previousContent = initial_content
        self.lexer = PythonLexer
        self.comment_tokens = [
            "Token.Comment.Single"
        ]
        self.string_tokens = [
            "Token.Name.Function",
            "Token.Name.Class",
            "Token.String",
            "Token.Literal.String.Single",
            "Token.Literal.String.Double"
        ]
        self.func_object_tokens = [
            "Token.Name.Function",
        ]
        self.class_object_tokens = [
            "Token.Name.Class",
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
        self.variable_color = '#fbf1c7'
        self.func_object_color = '#b8bb26'
        self.class_object_color = '#458588'

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
        for token in self.variable_tokens:
            self.text.tag_configure(token, foreground=self.variable_color)
        for token in self.func_object_tokens:
            self.text.tag_configure(token, foreground=self.func_object_color)
        for token in self.class_object_tokens:
            self.text.tag_configure(token, foreground=self.class_object_color)

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


    def load_new_syntax(self, path):
        with open(path) as new_syntax_config:
            new_config = yaml.load(new_syntax_config, Loader=yaml.FullLoader)
        pass
