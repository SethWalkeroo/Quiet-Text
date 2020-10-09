import tkinter as tk


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self.isControlPressed = False
        self._orig = self._w + '_orig'
        self.tk.call('rename', self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

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
