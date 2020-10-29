from tkinter import *
from tkinter import messagebox
import math
import random
import string
from functools import partial
from PIL import ImageTk, Image
import os, sys

#selecting word from files
word_file= "google-10000-english.txt"

f= open(word_file,"r")

data= f.readlines()
wordselected=""

while 1:
    line_index= random.randint(1,len(data))
    if len(data[line_index]) > 3:
        wordselected+= data[line_index].lower().strip()
        break
    
f.close()

alphabet=list(string.ascii_lowercase)
Mistery_word=list(wordselected)
print(Mistery_word)

limit=8
correct_counter=0

#initializing
my_window=Tk()
my_window.title("HANGMAN GAME")
img = PhotoImage(file='gameicon.ico')
my_window.tk.call('wm', 'iconphoto', my_window._w, img)
widthx=len(Mistery_word)*9 +791 #8 letters is the perfect amount for letter boxes
my_window.geometry("{}x600".format(widthx))
my_window.configure(background="#94d42b")

#image setup. hangman stages display per mistake(everytime limit decreases).
all_images=["hangman_pics/stage8.png", "hangman_pics/stage7.png", "hangman_pics/stage6.png", "hangman_pics/stage5.png", "hangman_pics/stage4.png", "hangman_pics/stage3.png", "hangman_pics/stage2.png", "hangman_pics/stage1.png", "empty.png"]
hangman_img = Image.open(all_images[limit])
hangman_img = hangman_img.resize((200, 200), Image.ANTIALIAS)
hangman_img= ImageTk.PhotoImage(hangman_img)
panel = Label(my_window, image = hangman_img)
panel.grid(column=10, row=0)


letter_display=[]
for i in range(len(Mistery_word)):
    letter_display.append(Label(my_window, text="",width="9", height="5"))
    letter_display[i].grid(row=0, column=i,columnspan=1)

Vrow=2
Vcolumn=0



def repeatletter(letter): #this counts how many times a letter repeats, becuase the button function can only checks if the letter is in the word(which is once)
    counter=0
    for i in wordselected:
        if i == letter:
            counter+=1
    return counter

def letterindex(letter):
    letterposition=[i for i in range(len(Mistery_word)) if Mistery_word[i]== letter]
    #print(letterposition)
    return letterposition
    
def change_color(i):
    global limit
    global correct_counter
    buttonletter= allbuttons[i].cget("text")
    
    location=letterindex(buttonletter)
    
    if buttonletter in wordselected:
        correct_counter+=1 * repeatletter(buttonletter) #correct_counter only checks once so I multiply by how many times it appears. 
        allbuttons[i].configure(bg="green")
        for i in location:
            letter_display[i].config(text=buttonletter)
        if len(letter_display) == correct_counter:
            messagebox.showinfo('All CORRECT' , 'YOU WIN')
            my_window.destroy()

    else:
        allbuttons[i].configure(bg="red")
        limit=limit-1
        guess_display.configure(text="you have {} guesses left".format(limit))

        hangman_img = Image.open(all_images[limit])
        hangman_img = hangman_img.resize((200, 200), Image.ANTIALIAS)
        hangman_img= ImageTk.PhotoImage(hangman_img)
        panel.configure(image=hangman_img)
        panel.image=hangman_img
        
        if limit==0:
            messagebox.showinfo('RAN OUT OF GUESSES' , 'YOU LOSE')
            my_window.destroy()
            
    
allbuttons=[]


for i in range(0,len(alphabet)):
    allbuttons.append(Button(my_window, text=alphabet[i], fg="blue", bg="yellow", height=5, width=9, command=partial(change_color, i)))
    allbuttons[i].grid(row=Vrow, column=Vcolumn)

    Vcolumn+=1
    
    if Vcolumn > 7 and Vrow==2:
        Vcolumn = 0
        Vrow += 1
    if Vcolumn> 7 and Vrow==3:
        Vcolumn = 0
        Vrow += 1
    if Vcolumn > 7 and Vrow==4:
        Vcolumn = 3
        Vrow+=1
        
guess_display=Label(my_window, text="you have {} guesses left".format(limit))
guess_display.grid(row=10, column=10)

my_window.mainloop()
