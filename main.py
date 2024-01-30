import tkinter as tk
from PIL import ImageTk, Image
from unwarp import execute

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
ent_fourth = tk.Entry()
label.pack()
ent_fourth.pack()

click = 0
label_image = tk.Label()


def handle_keypress():
    global click, label_image, img
    click += 1
    file_name = execute('myimg.jpg', float(ent_second.get()), float(ent_third.get()), float(ent_fourth.get()), click)
    img = ImageTk.PhotoImage(Image.open(file_name))
    label_image.config(image=img)


frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=5)
frame.pack()
btn_submit = tk.Button(
    text="Submit",
    width=5,
    height=2,
    command=handle_keypress
)
btn_submit.pack()

img = ImageTk.PhotoImage(Image.open('myimg.jpg'))
label_image.config(image=img)
label_image.pack()

window.mainloop()
