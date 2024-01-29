import tkinter as tk

window = tk.Tk()

label = tk.Label(text="2nd coeficient")
ent_second = tk.Entry()
label.pack()
ent_second.pack()

label = tk.Label(text="3rd coeficient")
ent_third = tk.Entry()
label.pack()
ent_third.pack()

label = tk.Label(text="4th coeficient")
ent_fourth = tk.Entry(text="Fourth coeficient")
label.pack()
ent_fourth.pack()

def handle_keypress():
    print(ent_second.get(), ent_third.get(), ent_fourth.get())

frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=5)
frame.pack()
btn_submit = tk.Button(
    text="Submit",
    width=5,
    height=2,
    command=handle_keypress
)
btn_submit.pack()

window.mainloop()