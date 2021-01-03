import tkinter as tk

class Statusbar:

    # initialising the status bar
    def __init__(self, parent):
        self._parent = parent
        self.save_bg = '#FF6859'
        self.status_fg = '#000000'
        self.error_bg = '#B00020'
        self.hint_bg = '#B15DFF'
        # setting up the status bar
        font_specs = ('Droid Sans Fallback', 10)

        self.status = tk.StringVar()

        label = tk.Label(
            parent.textarea,
            textvariable=self.status,
            fg=parent.font_color,
            bg='#fff',
            anchor='se',
            font=font_specs)
        
        self._label = label

    # status update of the status bar
    def update_status(self, event):
        if event == 'saved':
            self.display_status_message('Changes saved', msg_type='save')
        elif event == 'no file run':
            self.display_status_message('Cannot run. No file selected.')
        elif event == 'cant build':
            self.display_status_message('Cannot build this type of file.')
        elif event == 'no file':
            self.display_status_message('No file detected. Create or open a file.')
        elif event == 'no python':
            self.display_status_message('You cannot run this type of file.')
        elif event == 'no txt bold':
            self.display_status_message('You can only bold text in text files.')
        elif event == 'no txt high':
            self.display_status_message('You can only highlight text in text files.')
        elif event == 'quiet':
            self.display_status_message('You can leave quiet mode by pressing "escape"', msg_type='hint')
        elif event == 'created':
            self.display_status_message('File created', msg_type='hint')
        else:
            self.hide_status_bar()

    def display_status_message(self, message, msg_type='error'):
        self.show_status_bar()
        self.status.set(message)
        if msg_type == 'save':
            self.save_color()
        elif msg_type == 'hint':
            self.hint_color()
        else:
            self.error_color()

    def error_color(self):
        self._label.config(bg=self.error_bg, fg=self.status_fg)

    def save_color(self):
        self._label.config(bg=self.save_bg, fg=self.status_fg)

    def hint_color(self):
        self._label.config(bg=self.hint_bg, fg=self.status_fg)

    # hiding the status bar while in quiet mode
    def hide_status_bar(self):
        self._label.pack_forget()

    # display of the status bar
    def show_status_bar(self):
        self._label.pack(side=tk.BOTTOM)

    def reconfigure_status_label(self):
        self._label.config()

