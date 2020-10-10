import tkinter as tk
import math
import tkinter.font as tk_font
from pygments import lex
from pygments.lexers import PythonLexer
from quiet_zutilityfuncs import load_settings_data

class PythonSyntaxHighlight():

    def __init__(self, text_widget, initial_content):
        self.settings = load_settings_data()
        self.font_family = self.settings['font_family']
        self.text = text_widget
        self.italics = tk_font.Font(family=self.font_family, slant='italic')
        self.previousContent = initial_content
        self.lexer = PythonLexer
        self.comment_tokens = [
            "Token.Comment.Single"
        ]
        self.string_tokens = [
            "Token.Name.Function",
            "Token.Name.Class",
            "Token.Literal.String.Single",
        ]
        self.object_tokens = [
            "Token.Name.Function",
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
        self.punctuation_tokens = [
            "Token.Punctuation",
        ]

        self.comment_color = '#75715E'
        self.string_color = '#FFD866'
        self.number_color = '#AB9DF2'
        self.keyword_color = '#F92672'
        self.function_color = '#78DCE8'
        self.class_color = '#c9bfbd'
        self.variable_color = '#fff'
        self.punctuation_color = '#c9bfbd'
        self.object_color = '#A9DC76'

    def update_highlight_font(self):
        settings = load_settings_data()
        self.font_family = settings['font_family']
        self.font_size = settings['font_size']
        self.italics = tk_font.Font(family=self.font_family, slant='italic')

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
            self.text.tag_configure(token, foreground=self.class_color, font=self.italics)
        for token in self.variable_tokens:
            self.text.tag_configure(token, foreground=self.variable_color)
        for token in self.punctuation_tokens:
            self.text.tag_configure(token, foreground=self.punctuation_color)
        for token in self.object_tokens:
            self.text.tag_configure(token, foreground=self.object_color)

    def initial_highlight(self):
        content = self.text.get("1.0", tk.END)

        self.text.mark_set("range_start", "1.0")

        words = content.split(" ")
        lastWordLength = len(words[len(words) - 1])

        lastPos = self.text.index("end-1c")
        startRow = int(lastPos.split(".")[0])
        startCol = abs(int(lastPos.split(".")[1]) - lastWordLength)

        data = self.text.get("1.0", tk.END)
        for token, content in lex(data, PythonLexer()):
            self.text.mark_set("range_end", "range_start + %dc" % len(content))
            self.text.tag_add(str(token), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")
            
        self.previousContent = self.text.get("1.0", tk.END)
        self.syntax_theme_configuration()
        self.update_highlight_font()


