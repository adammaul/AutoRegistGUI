import tkinter as tk
from tkinter import ttk

def curse():
    print(f'Sn anda adalah {sn.get() or "empty"}')

root = tk.Tk()
root.geometry('600x400')

sn = tk.StringVar()

sn_label = ttk.Label(root, text='Masukkan SN: ')
sn_entry = ttk.Entry(root,textvariable=sn )


top_button = ttk.Button(root,text='click me',command=curse)
lower_button = ttk.Button(root,text='Quit',command=root.destroy)

sn_label.pack(side='left',expand=True)
sn_entry.pack(side='left',expand=True)
top_button.pack(side='top',expand=True)
lower_button.pack(side='bottom',expand=True)

root.mainloop()