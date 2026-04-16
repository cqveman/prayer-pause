import sys
import tkinter as tk

from prayer_pause.utils import get_logger

logger = get_logger('Locker')


def lock(prayer_name: str, duration_minutes: int):
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure((0, 1, 2), weight=1, uniform='a')

    logger.info(f"Triggering locker for {prayer_name} ({duration_minutes} mins)")

    # Make it full screen and borderless
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.configure(bg='#1a1a1a')

    # Disable Alt+F4 / Window Manager 'X'
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    # Intercept keyboard and mouse events
    root.grab_set()
    root.focus_force()

    # Exiter
    root.bind('<Control-Shift-Up>', lambda e: root.destroy())

    tk.Label(root, text='Prayer Pause', font=('Helvetica', 32, 'bold'), fg='white', bg='#1a1a1a') \
        .grid(row=0, column=0, sticky='s')
    tk.Label(root, text=f"Device locked for {prayer_name}'s prayer.", font=('Helvetica', 32, 'bold'), fg='white',
             bg='#1a1a1a').grid(row=1, column=0, sticky='n')

    countdown_label = tk.Label(root, text='00:00', font=('Helvetica', 72, 'bold'), fg='white', bg='#1a1a1a')
    countdown_label.grid(row=2, column=0, sticky='n')

    duration_seconds = duration_minutes * 60
    _countdown(root, duration_seconds, countdown_label)

    root.mainloop()


def _countdown(root, remaining, label):
    # https://docs.python.org/3/library/functions.html#divmod
    mins, secs = divmod(remaining, 60)  # Returns (a // b, a % b)
    label.config(text=f'{mins:02d}:{secs:02d}')  # Add 2 leading zeros

    if remaining <= 0:
        root.destroy()
        return

    root.after(1000, _countdown, root, remaining - 1, label)


if __name__ == "__main__":
    p = sys.argv[1]
    t = int(sys.argv[2])
    lock(p, t)
