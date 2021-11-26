import random
from tkinter import *
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
event = None

data = {}
try: 
    data = pd.read_csv("data/words_to_learn.csv")
    print("using saved data")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
data = data.to_dict(orient="records")
print(data)

window = Tk()
window.title("flashcard")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
img = canvas.create_image(400, 263, image=card_front_img)
title = canvas.create_text(400, 150, text="Title", font=("Hack", 40, "italic"))
word = canvas.create_text(400, 263, text="word", font=("Hack", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0,column=0, columnspan=2)

crossimg = PhotoImage(file="images/wrong.png")
btncross = Button(image=crossimg, highlightthickness=0)
btncross.grid(row=1, column=0)

checkimg = PhotoImage(file="images/right.png")
btncheck = Button(image=checkimg, highlightthickness=0)
btncheck.grid(row=1, column=1)

def flip_card():
    global img, canvas, current_word, title, word
    canvas.itemconfig(img, image=card_back_img)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_word["English"], fill="white")

def next_card():
    global title, word, img, data, current_word, canvas, event
    if event is not None:
        window.after_cancel(event)
    current_word = random.choice(data)
    canvas.itemconfig(img, image=card_front_img)
    canvas.itemconfig(title, text = "French", fill="black")
    canvas.itemconfig(word, text = current_word["French"], fill="black")
    event = window.after(3000, func=flip_card)

def remove_and_next():
    global current_word, data
    data.remove(current_word)
    next_card()

btncross.config(command=next_card)
btncheck.config(command=remove_and_next)
next_card()

window.mainloop()
df = pd.DataFrame(data)
df.to_csv('data/words_to_learn.csv', index=False)
