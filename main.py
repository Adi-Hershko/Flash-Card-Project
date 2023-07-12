from tkinter import *
from random import randint, choice
import pandas

BACKGROUND_COLOR = "#B1DDC6"
LANG_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")
LANG_X_POS = 400
LANG_Y_POS = 150
WORD_X_POS = 400
WORD_Y_POS = 263

flip_timer = None
current_word = {}

# -------------------------------- Creating Cards ---------------------------------------
try:
    words = pandas.read_csv("data/words_to_learn.csv").to_dict(orient="records")
except FileNotFoundError:
    words = pandas.read_csv("data/french_words.csv").to_dict(orient="records")


def next_card():
    global flip_timer, current_word
    if len(words) == 0:
        canvas.itemconfig(canvas_lang_text, text="No More Words To Learn!", fill="black")
        canvas.itemconfig(canvas_word_text, text="Congrats!", fill="black")
        return
    if flip_timer != None:
        window.after_cancel(flip_timer)
    canvas.itemconfig(canvas_image, image=card_front_img)
    current_word = choice(words)
    random_word_eng = current_word["English"]
    random_word_fr = current_word["French"]
    canvas.itemconfig(canvas_lang_text, text="French", fill="black")
    canvas.itemconfig(canvas_word_text, text=random_word_fr, fill="black")
    flip_timer = window.after(3000, flip_card, current_word)

# -------------------------------- Flip Card -------------------------------------------


def flip_card(random_word):
    eng_word = random_word["English"]
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(canvas_lang_text, text="English", fill="white")
    canvas.itemconfig(canvas_word_text, text=eng_word, fill="white")


# -------------------------------- Remove Known Cards -----------------------------------

def known_card():
    global current_word, words
    if len(words) != 0:
        words.remove(current_word)
        words_to_learn = pandas.DataFrame(words)
        words_to_learn.to_csv("data/words_to_learn.csv", index=False)
        next_card()


# -------------------------------- UI Setup --------------------------------------------

window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas_lang_text = canvas.create_text(LANG_X_POS, LANG_Y_POS, font=LANG_FONT)
canvas_word_text = canvas.create_text(WORD_X_POS, WORD_Y_POS, font=WORD_FONT)
canvas.grid(row=0, column=0, columnspan=2)

wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)
right_button = Button(image=right_img, highlightthickness=0, command=known_card)
right_button.grid(row=1, column=1)

next_card()

# print(words.shape)


window.mainloop()
