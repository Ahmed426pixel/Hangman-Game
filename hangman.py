import tkinter as tk
import random

# Setup display
root = tk.Tk()
root.title("Hangman Game!")
WIDTH, HEIGHT = 800, 500
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# Exit button
def exit_game():
    root.destroy()

exit_button = tk.Button(root, text="Exit", command=exit_game, bg="red", fg="white")
exit_button.pack(pady=20)

# Button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# Fonts
LETTER_FONT = ("comicsans", 20)
WORD_FONT = ("comicsans", 30)
TITLE_FONT = ("comicsans", 40)

# Load images
images = []
for i in range(7):
    image = tk.PhotoImage(file=f"hangman{i}.png")
    images.append(image)

# Load win/lose images
won_image = tk.PhotoImage(file="won.png")
lost_image = tk.PhotoImage(file="lose.png")

# Game variables
hangman_status = 0
words = ["SUN", "GAME", "PYTHON", "NEAR", "CHAIR", "PHONE", "HOUSE", "HANGMAN", "WOMEN", "COMPUTER", "COLLEGE"]
word = random.choice(words)
guessed = []

# Colors
WHITE = "#FFFFFF"
BLACK = "#000000"

def draw():
    canvas.delete("all")
    
    # Draw title
    canvas.create_text(WIDTH/2, 50, text="HANGMAN GAME", font=TITLE_FONT, fill=BLACK)
    
    # Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    canvas.create_text(WIDTH/2, 200, text=display_word, font=WORD_FONT, fill=BLACK)
    
    # Draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, outline=BLACK, width=3)
            canvas.create_text(x, y, text=ltr, font=LETTER_FONT, fill=BLACK)
    
    canvas.create_image(150, 100, anchor=tk.NW, image=images[hangman_status])

def display_message(message, image=None):
    canvas.delete("all")
    if image:
        # Display image to cover full frame
        canvas.create_image(WIDTH/2, HEIGHT/2, anchor=tk.CENTER, image=image)
    canvas.create_text(WIDTH/2, HEIGHT/2 + 200, text=message, font=WORD_FONT, fill=BLACK)
    root.update()
    root.after(3000, main)

def check_letter(event):
    global hangman_status
    m_x, m_y = event.x, event.y
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            dis = ((x - m_x)**2 + (y - m_y)**2)**0.5
            if dis < RADIUS:
                letter[3] = False
                guessed.append(ltr)
                if ltr not in word:
                    hangman_status += 1
    draw()
    check_win_or_loss()

def check_win_or_loss():
    global hangman_status

    won = all(letter in guessed for letter in word)
    if won:
        display_message("You WON!", won_image)
    elif hangman_status == 6:
        display_message(f"You LOST! The word was {word}", lost_image)

def main():
    global hangman_status, word, guessed, letters
    hangman_status = 0
    word = random.choice(words)
    guessed = []
    for letter in letters:
        letter[3] = True
    draw()

canvas.bind("<Button-1>", check_letter)

main()
root.mainloop()
