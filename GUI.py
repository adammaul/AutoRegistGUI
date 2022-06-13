import tkinter as tk

root = tk.Tk()

header = tk.Label(
    text="EZ-Regist",
    width=25,
    height=5
)
regist_pertama = tk.Button(
    text="Regist Pertama",
    width=25,
    height=5,
)
regist_ulang = tk.Button(
    text="Regist Ulang / Replace",
    width=25,
    height=5,
)

label_sn = tk.Label(text='SN :')
entry_sn = tk.Entry()

label_fsp = tk.Label(text='FSP :')
entry_fsp = tk.Entry()

label_vlan = tk.Label(text='Vlan :')
entry_vlan = tk.Entry()

label_lineprofile = tk.Label(text='Lineprofile :')
entry_lineprofile = tk.Entry()

label_serviceprofile = tk.Label(text='Serviceprofile :')
entry_serviceprofile = tk.Entry()

label_nama = tk.Label(text='Nama :')
entry_nama = tk.Entry()

label_sid = tk.Label(text='SID :')
entry_sid = tk.Entry()

header.grid(row=1, column =1)

label_sn.grid(row=2, column =1)
entry_sn.grid(row=2, column =2)

label_fsp.grid(row=3, column =1)
entry_fsp.grid(row=3, column =2)

label_vlan.grid(row=4, column =1)
entry_vlan.grid(row=4, column =2)

label_lineprofile.grid(row=5, column =1)
entry_lineprofile.grid(row=5, column =2)

label_serviceprofile.grid(row=6, column =1)
entry_serviceprofile.grid(row=6, column =2)

label_sid.grid(row=8, column =1)
entry_sid.grid(row=8, column =2)


label_nama.grid(row=7, column =1)
entry_nama.grid(row=7, column =2)

root.mainloop()

