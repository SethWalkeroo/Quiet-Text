import tkinter as tk

class TextLineNumbers(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self._text_font = parent.settings['font_family']
        self._parent = parent
        self.textwidget = parent.textarea
        self.font_color = parent.menu_fg
        self.bg_color = parent.bg_color
        self.indicator_on = parent.current_line_indicator
        self.current_line_symbol = parent.current_line_symbol


    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        if not self.visible:
            return

        self.delete('all')
        self.config(width=(self._parent.font_size * 3), 
                    bd=0, bg=self.bg_color, highlightthickness=0)

        i = self.textwidget.index('@0,0')
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            index = self.textwidget.index(tk.INSERT)
            pos = index.split('.')[0]
            if float(i) >= 10:
                linenum = str(i).split('.')[0]
                if pos == linenum and self.indicator_on:
                    linenum = linenum + self.current_line_symbol
            else:
                linenum = ' ' + str(i).split('.')[0]
                if ' ' + pos == linenum and self.indicator_on:
                    linenum = linenum + self.current_line_symbol
            self.create_text(2, y, anchor='nw',
                             text=linenum,
                             font=(self._text_font, self._parent.font_size),
                             fill=self.font_color)
            i = self.textwidget.index('%s+1line' % i)

    @property
    def visible(self):
        return self.cget('state') == 'normal'

    @visible.setter
    def visible(self, visible):
        self.config(state='normal' if visible else 'disabled')

        if visible:
            self.redraw()
        else:
            self.delete('all')
            self.config(width=0)
