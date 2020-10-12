import tkinter as tk

class TextLineNumbers(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self._text_font = parent.settings['font_family']
        self._parent = parent
        self.textwidget = parent.textarea

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        if not self.visible:
            return

        self.delete('all')
        self.config(width=(self._parent.font_size * 3))

        i = self.textwidget.index('@0,0')
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split('.')[0]
            self.create_text(2, y, anchor='nw',
                             text=linenum,
                             font=(self._text_font, self._parent.font_size),
                             fill='#75715E')
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
