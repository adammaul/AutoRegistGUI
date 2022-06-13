import tkinter as tk

root = tk.Tk()

header = tk.Label(
    text="EZ-Regist",
    fg="white",
    bg="black",
    width=10,
    height=10
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

header.pack()
regist_pertama.grid()

button.pack()

root.mainloop()
