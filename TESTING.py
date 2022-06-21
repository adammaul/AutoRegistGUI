import tkinter as tk
from tkinter import ttk

def curse():
    print(f'Sn anda adalah {sn.get() or "empty"}')

root = tk.Tk()

one_frame = ttk.Frame()
one_frame.pack(side='top',fill='both')

two_frame = ttk.Frame()
two_frame.pack(side='top',fill='both')


root.geometry('1000x150')

sn = tk.StringVar()
fsp = tk.StringVar()


#INPUT SN
sn_label = ttk.Label(one_frame, text='Masukkan SN: ')
sn_entry = ttk.Entry(one_frame,textvariable=sn )

#INPUT FSP
# fsp_label = ttk.Label(left_frame, text='Masukkan FSP: ')
# fsp_entry = ttk.Entry(right_frame,textvariable=fsp)

#INPUT BUTTON
top_button = ttk.Button(two_frame,text='click me',command=curse)
lower_button = ttk.Button(two_frame,text='Quit',command=root.destroy)

sn_label.pack(side='left')
sn_entry.pack(side='left',expand=True,fill="x")
top_button.pack(side='left',expand=True,fill='both')
lower_button.pack(side='left',expand=True,fill='both')


root.mainloop()