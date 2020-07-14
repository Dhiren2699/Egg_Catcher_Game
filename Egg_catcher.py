from itertools import cycle # different colorful eggs
from random import randrange
from tkinter import Tk , Canvas , messagebox , font

canvas_width = 800 
canvas_height = 400

win = Tk()
c = Canvas(win , width = canvas_width ,  height = canvas_height , background = 'deep sky blue')
#ground
c.create_rectangle(-5, canvas_height - 100 , canvas_width + 5 , canvas_height + 5 , fill='sea green', width=0)
#oval for score board
c.create_oval(-80,-80,120,120, fill='orange' , width=0)
c.pack()

color_cycle = cycle(['light blue' , 'pink' , 'yellow','light green' , 'red', 'blue' , 'green','black', 'light yellow', 'purple'])
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 500
egg_interval = 4000  # 4 seconds
difficulty_factor = 0.95


catcher_color = 'yellow'
catcher_width = 100
catcher_height = 100
catcher_start_x = canvas_width / 2 - catcher_width / 2
catcher_start_y = canvas_height - catcher_height - 20    # if want up more then take more than 20
# ending points
catcher_start_x2 = catcher_start_x + catcher_width
catcher_start_y2 = catcher_start_y + catcher_height

#create basket
catcher = c.create_arc(catcher_start_x ,catcher_start_y ,catcher_start_x2,catcher_start_y2 , start=200 , extent = 140 , style='arc' , outline=catcher_color , width=3)

score = 0
# create_text(pad_X,pad_y, northwest)
score_text = c.create_text(10,10,anchor='nw' , font=('Arial',18,'bold'),fill='darkblue',text='Score : ' + str(score))

lives_remaning = 3
lives_text = c.create_text(canvas_width-10,10,anchor='ne' , font=('Arial',18,'bold'),fill='darkblue',text='Lives : ' + str(lives_remaning))

eggs = []

def create_eggs():
    # x, y are postions. x is different but y is same falling height
    x = randrange(10,740) # random postion to fall
    y = 40 # falling from height 40
    new_egg = c.create_oval(x,y,x+egg_width,y+egg_height,fill=next(color_cycle),width=0)
    eggs.append(new_egg)
    win.after(egg_interval,create_eggs) # fall eggs after interval 4 sec

def move_eggs():
    for egg in eggs:
        (egg_x,egg_y,egg_x2,egg_y2) = c.coords(egg) #take all cordinates of egss and provide co ordinate value
        c.move(egg,0,10)  # corordinate 0 with distance 10
        if egg_y2 > canvas_height:  #if bottom of egg touches down
            egg_dropped(egg)
    win.after(egg_speed,move_eggs) # loop itself with increasing speed

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg) # or the egg will be on screen after drop
    lose_a_life()
    if lives_remaning == 0:
        messagebox.showinfo('GAME OVER!' , 'Final Score : ' + str(score))
        win.destroy()

def lose_a_life():
    global lives_remaning
    lives_remaning -= 1
    # update in game too canvas configure
    c.itemconfigure(lives_text , text='Lives : ' + str(lives_remaning))

def catch_check():
    (catcher_x,catcher_y,catcher_x2,catcher_y2) = c.coords(catcher)
    for egg in eggs:
        (egg_x,egg_y,egg_x2,egg_y2) = c.coords(egg)
        #basket left boundary must be less than egg left side boundary
        #basket right boundary must be more than egg right side boundary
        # vertical difference base of basket - base of egg must be less than 40
        if catcher_x < egg_x and egg_x2  < catcher_x2 and catcher_y2 - egg_y2 < 40:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    win.after(100,catch_check) # loop or it will stop after one catch. check every 100 millisecond and loop

def increase_score(points):
    global score , egg_speed , egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty_factor)
    egg_interval = int(egg_interval * difficulty_factor)
    c.itemconfigure(score_text , text='Score : ' + str(score))

def move_left(event):
    (x1,y1,x2,y2) = c.coords(catcher)
    if x1 > 0:  # then only you can move left
        c.move(catcher,-20,0)  # -20 to 0 as its moving left

def move_right(event):
    (x1,y1,x2,y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher,20,0)

# bind method to bind the keys with method
c.bind('<Left>' , move_left)
c.bind('<Right>' , move_right)
c.focus_set()

# call function at particular time to start game
win.after(1000,create_eggs)
win.after(1000,move_eggs)
win.after(1000,catch_check)

win.mainloop()
