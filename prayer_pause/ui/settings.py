import tkinter as tk

from prayer_pause.utils import load_config, update_config


def settings_menu(on_settings_saved):
    notify_dur, lock_dur, locker_offset, before_or_after = load_config()

    root = tk.Tk()

    root.title('Config')
    root.minsize(250, 150)
    root.resizable(False, False)

    notify_var = tk.IntVar(value=notify_dur)
    lock_var = tk.IntVar(value=lock_dur)
    locker_offset_var = tk.IntVar(value=locker_offset)
    before_or_after_var = tk.StringVar(value=before_or_after)

    tk.Label(root, text='Notify (minutes)').pack()
    tk.Entry(root, textvariable=notify_var).pack()

    tk.Label(root, text='Lock (minutes)').pack()
    tk.Entry(root, textvariable=lock_var).pack()

    offset_frame = tk.Frame(root)
    offset_frame.pack(pady=10)
    offset_frame.columnconfigure((0, 1), weight=1)
    offset_frame.rowconfigure((0, 1, 2), weight=1)

    tk.Radiobutton(offset_frame, text='Before Adhan', variable=before_or_after_var, value='BEFORE') \
        .grid(column=0, row=0)
    tk.Radiobutton(offset_frame, text='After Adhan', variable=before_or_after_var, value='AFTER') \
        .grid(column=1, row=0)

    tk.Label(offset_frame, text='Locker Offset (minutes)').grid(column=0, columnspan=2, row=1)
    tk.Entry(offset_frame, textvariable=locker_offset_var).grid(column=0, columnspan=2, row=2)

    def save():
        try:
            update_config(notify_var.get(), lock_var.get(), locker_offset_var.get(), before_or_after_var.get())
            on_settings_saved()
            root.destroy()
        except Exception as e:
            tk.Label(root, text=str(e), fg='red').pack()

    tk.Button(root, text="Save", command=save).pack(pady=10)

    root.mainloop()
