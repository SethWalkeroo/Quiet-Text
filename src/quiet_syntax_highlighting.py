import pygments
import tkinter as tk
import pygments.token
import math
from pygments import lex
from pygments.lexers import PythonLexer

class PythonSyntaxHighlight():

    def __init__(self, text_widget, initial_content):
        self.text = text_widget
        self.previousContent = initial_content

    def default_highlight(self):
        row = float(self.text.index(tk.INSERT))
        row = str(math.trunc(row))
        content = self.text.get("1.0", tk.END)
        lines = content.split("\n")

        if (self.previousContent != content):
            self.text.mark_set("range_start", row + ".0")
            data = self.text.get(row + ".0", row + "." + str(len(lines[int(row) - 1])))

            for token, content in lex(data, PythonLexer()):
                self.text.mark_set("range_end", "range_start + %dc" % len(content))
                self.text.tag_add(str(token), "range_start", "range_end")
                self.text.mark_set("range_start", "range_end")

        self.previousContent = self.text.get("1.0", tk.END)



    def syntax_theme_configuration(self):
            self.text.tag_configure("Token.Keyword", foreground="#F92672")
            self.text.tag_configure("Token.Name.Builtin.Pseudo", foreground="#FD971F")
            self.text.tag_configure("Token.Operator", foreground="#F92672")
            self.text.tag_configure("Token.Literal.String.Single", foreground="#A6E22E")
            self.text.tag_configure("Token.Literal.String.Double", foreground="#A6E22E")
            self.text.tag_configure("Token.Literal.Number.Float", foreground="#AE81FF")
            self.text.tag_configure("Tokens.Name", foreground="#66D9EF")
            self.text.tag_configure("Tokens.Literal.String.Affix", foreground="#66D9EF")
            self.text.tag_configure("Tokens.Text", foreground="#F8F8F2")
            self.text.tag_configure("Tokens.Punctuation", foreground="#F8F8F2")
            self.text.tag_configure("Tokens.Literal.String.Interpol", foreground="#F8F8F2")
            self.text.tag_configure("Tokens.Literal.Number.Integer", foreground="#AE81FF")


    def initial_highlight(self):
        content = self.text.get("1.0", tk.END)

        if (self.previousContent != content):
            self.text.mark_set("range_start", "1.0")

            words = content.split(" ")
            lastWordLength = len(words[len(words) - 1])

            lastPos = self.text.index("end-1c")
            startRow = int(lastPos.split(".")[0])
            startCol = abs(int(lastPos.split(".")[1]) - lastWordLength)

            # print(startRow, startCol) # Results in incorrect values

            data = self.text.get("0.0", tk.END)
            for token, content in lex(data, PythonLexer()):

                self.text.mark_set("range_end", "range_start + %dc" % len(content))
                self.text.tag_add(str(token), "range_start", "range_end")
                self.text.mark_set("range_start", "range_end")
                
        self.previousContent = self.text.get("1.0", tk.END)


