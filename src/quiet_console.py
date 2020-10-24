import tkinter as tk
import subprocess as sp
from re import match
from threading import Thread
from queue import Queue
from tkinter import ttk


class QuietConsole:

    def __init__(self, master):
        self.master = master
        self.queue = Queue()
        # Pack main frame
        self.termf = tk.Frame(self.master, width=50, height=150, bd=0, bg=master.bg_color)
        self.termf.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.NO, padx=0, pady=0)
        self.wid = self.termf.winfo_id()
        self.main()
        
    def main(self):

        # Allow window resize
        sp.Popen("""echo '*VT100.allowWindowOps: true' | xrdb -merge""", shell=True)

        # Craft command
        cmd = (
            # Create into me
            f'xterm -into {self.wid} -geometry 100x50 '
            # Log to stdout
            r'-sb -l -lc -lf /dev/stdout '
            # Launch `ps` command: output, tty, = for remove header
            """-e /bin/bash -c "ps -o tt=;bash" """
            r'| tee'
        )
        # print('Launching:', cmd)

        # Spawn Xterm
        process = sp.Popen(
            cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        # print('Xterm pid:', process.pid)

        # Get pts
        thread = Thread(target=lambda: self.get_xterm_pts(self.termf, process, self.queue))
        thread.start()

        # Set resize callback
        self.termf.bind("<Configure>", lambda event: self.on_resize(event, self.queue))


    def on_resize(self, event, queue):
        """On resize: send escape sequence to pts"""
        # Magic && Check
        magic_x, magic_y = 6.1, 13
        # print('Resize (w, h):', event.width, event.height)
        if not self.queue.queue:
            return

        # Calculate
        width = int(event.width / magic_x)
        height = int(event.height / magic_y)
        # print('To (lin,col):', height, width)
        ctl = f"\u001b[8;{height};{width}t"

        # Send to pts
        with open(queue.queue[0], 'w') as f:
            f.write(ctl)


    def get_xterm_pts(self, parent, process, queue):
        """Retrieve pts(`process`) -> `queue`"""
        while True:
            out = process.stdout.readline().decode()
            # print('Xterm out' + out)

            match_pts = match(r'pts/\d+', out)
            if match_pts:
                pts = '/dev/' + match_pts.group(0)
                # print('-----------> pts:', pts)
                self.queue.put(pts)
                break

            if out == b'' and process.poll() is not None:
                break

        # Resize now
        fake_event = tk.Event()
        fake_event.width = parent.winfo_width()
        fake_event.height = parent.winfo_height()
        self.on_resize(fake_event, self.queue)
        
    def remove_console(self):
        self.termf.forget()
    

