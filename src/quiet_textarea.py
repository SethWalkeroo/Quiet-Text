import tkinter as tk
from tkinter import messagebox

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self.isControlPressed = False
        self._orig = self._w + '_orig'
        self.tk.call('rename', self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        self.bg_color = '#272822'

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        try:
            cmd = (self._orig,) + args
            result = ''
            if not self.isControlPressed:
                # if command is not present, execute the event
                result = self.tk.call(cmd)
            else:
                # Suppress y-scroll and x-scroll when control is pressed
                if args[0:2] not in [('yview', 'scroll'), ('xview', 'scroll')]:
                    result = self.tk.call(cmd)
        except tk.TclError:
            result = ''

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ('insert', 'replace', 'delete') or 
            args[0:3] == ('mark', 'set', 'insert') or
            args[0:2] == ('xview', 'moveto') or
            args[0:2] == ('xview', 'scroll') or
            args[0:2] == ('yview', 'moveto') or
            args[0:2] == ('yview', 'scroll')
        ):
            self.event_generate('<<Change>>', when='tail')

        # return what the actual widget returned
        return result   

    def find(self, text_to_find):
        length = tk.IntVar()
        index = self.search(text_to_find, self.find_search_starting_index, stopindex=tk.END, count=length)

        if index:
            self.tag_remove('find_match', 1.0, tk.END)

            end = f'{index}+{length.get()}c'
            self.tag_add('find_match', index, end)
            self.see(index)

            self.find_search_starting_index = end
            self.find_match_index = index
        else:
            if self.find_match_index != 1.0:
                if tk.messagebox.askyesno("No more results", "No further matches. Repeat from the beginning?"):
                    self.find_search_starting_index = 1.0
                    self.find_match_index = None
                    return self.find(text_to_find)
            else:
                tk.messagebox.showinfo("No Matches", "No matching text found")

    def replace_text(self, target, replacement):
        if self.find_match_index:
            current_found_index_line = str(self.find_match_index).split('.')[0]

            end = f"{self.find_match_index}+{len(target)}c"
            self.replace(self.find_match_index, end, replacement)

            self.find_search_starting_index = current_found_index_line + '.0'

    def cancel_find(self):
        self.find_search_starting_index = 1.0
        self.find_match_index = None
        self.tag_remove('find_match', 1.0, tk.END)

