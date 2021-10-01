import pygame
from pygame.locals import *
import sqlite3
import os
import sys
import math
import random
import time
import tkinter as tk
from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from queue import PriorityQueue
pygame.init()
W, H = 800, 600
window = pygame.display.set_mode((W,H))
pygame.display.set_caption('Scroller Survival')
bg = pygame.image.load(os.path.join('images','bg.png')).convert()
mback = pygame.image.load(os.path.join('images','back2.jpg')).convert()
mback = pygame.transform.scale(mback,(800,600))
Xs = 0
Ys = 0
bg1 = 0
bg2 = -H
clock = pygame.time.Clock()
white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
light_red= (255,0,0)
yellow = (200,200,0)
green = (34,177,76)
light_green = (0,255,0)
light_yellow = (255,255,0)

class Basic_Class(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
class player(Basic_Class): 
    def __init__(self, x, y, width, height):
        super().__init__(x,y,width,height) 
        self.Jumping = False
        self.Sliding = False
        self.Slide_Length = 0
        self.Jump_Length = 9
        self.Run_Length = 0
        self.JumpSlide = False
        self.hit = False
    def Lose(self, window):
        if self.hit:
            pygame.draw.rect(window,(0,255,0),(self.x,self.y,self.width,self.height))

    def Jumps(self, window):
        if self.Jumping:
            if self.Jump_Length >= -9:
                negative = 2.5
                if self.Jump_Length < 0:
                    negative = -2.5
                self.y -= self.Jump_Length**2*0.1*negative
                pygame.draw.rect(window, (255,0,0), (self.x,self.y,self.width,self.height))
                self.Jump_Length -= 0.25
            else:
                self.Jump_Length = 9
                self.Jumping = False
            self.collision = (self.x+4,self.y,self.width-24,self.height-10)
        else:
            self.Jump_Length = 9
            self.Jumping = False
        self.collision = (self.x+4,self.y,self.width-24,self.height-10)
        return False
    def Slides(self,window):
        if self.Sliding or self.JumpSlide:
            if self.Slide_Length < 20: 
                self.y += 1
            elif self.Slide_Length == 80:
                self.y -= 19
                self.Sliding = False
            elif self.Slide_Length >20 and self.Slide_Length <80:
                self.collision = (self.x,self.y+3,self.width-8,self.height-35)
                self.JumpSlide = True
            if self.Slide_Length >= 110:
                self.Slide_Length = 0
                self.JumpSlide = False
                self.Run_Length = 0
                self.collision = (self.x+4,self.y,self.width-24,self.height-10)
            pygame.draw.rect(window,(255,0,0),(self.x-5,self.y,self.width+15,self.height-10))
            self.Slide_Length += 1
    def Runs(self,window):
        if self.Run_Length > 42:
            self.Run_Length = 0
        pygame.draw.rect(window,(255,0,0),(self.x,self.y,self.width,self.height))
        self.Run_Length += 1
        self.collision = (self.x+8,self.y-10,self.width-24,self.height-13)




class saw(Basic_Class):
    def __init__(self, x, y, width, height): 
        super().__init__(x,y,width,height) 
        self.collision = (x,y,width,height) 
    def Show(self,window):
        self.collision = (self.x + 8,self.y + 2, self.width - 20,self.height) 
        pygame.draw.rect(window,(0,0,255),(self.x,self.y,self.width,self.height)) 
        
    def collide(self,rectangle):
        if rectangle[0] + rectangle[2] > self.collision[0] and rectangle[0] < self.collision[0] + self.collision[2]:
            if rectangle[1] + rectangle[3] > self.collision[1]:
                return True
        return False

class spike(saw): 
    
    def Show(self,winndow):
        self.collision = (self.x + 15, self.y +15, 32,315) 
        pygame.draw.rect(window,(0,0,255),(self.x,self.y,self.width,self.height)) 

    def collide(self,rectangle): 
        if rectangle[0] + rectangle[2] > self.collision[0] and rectangle[0] < self.collision[0] + self.collision[2]: 
            if rectangle[1] < self.collision[3]: 
                return True 
        return False  


def database():
    conn = sqlite3.connect("database/tes2.db")
    sql1 = "SELECT question,canswers,wanswer,wanswer2,difficulty FROM question,answers,difficulty WHERE question.questionID = answers.questionID AND answers.diffiucltyID = difficulty.difficultyID ORDER BY random()"
    cursor = conn.execute(sql1)
    rows = cursor.fetchall()
    return rows


def leaderboard():
    conn = sqlite3.connect("database\leaderboard.db")
    sql1 = "SELECT Name,Score FROM lead ORDER BY Score DESC"
    cursor = conn.execute(sql1)
    rows = cursor.fetchall()
    return rows

def queue_add(d,rows,i):
    Queue_Quiz.put((d[rows[i][4]],rows[i]))
def queue(rows,Queue_Quiz):
    d = {'easy':1,'medium':2,'hard':3} 
    for i in range(0, len(rows)): 
        if rows[i][4] == 'easy': 
            queue_add(d,rows,i)
        if rows[i][4] == 'medium': 
            queue_add(d,rows,i)
        if rows[i][4] == 'hard':
            queue_add(d,rows,i)

    
def UpdateScore():
    rows = leaderboard()
    high = rows[0][1]
    return high




def insert():
    root = tk.Tk()
    rows = database()
    root.attributes("-topmost",True)
    root.geometry("800x600+0+0")
    root.lift()
    def dropdown(*args):
        return tkvar.get()
    def finish(e,e2,e3,e4,e5):
        s1 = e.get()
        s2 = e2.get()
        s3 = e3.get()
        s4 = e4.get()
        s5 = dropdown()
        if s5 == 'easy':
            s5 = "1"
        if s5 == 'medium':
            s5 = "2"
        if s5 == 'hard':
            s5 = "3"
        conn = sqlite3.connect("database/tes2.db")
        conn.execute("BEGIN TRANSACTION;")
        conn.execute("INSERT INTO question(question)VALUES(?);",(s1,))
        conn.execute("COMMIT;")
        conn.execute("BEGIN TRANSACTION;")
        conn.execute("INSERT INTO answers(canswers,wanswer,wanswer2,questionID,diffiucltyID)VALUES(?,?,?,(SELECT questionID FROM question WHERE question.questionID NOT IN(SELECT questionID FROM answers)),  ?);",(s2,s3,s4,s5,))
        conn.execute("COMMIT;")
        conn.commit()
        root.destroy()
    bgh=tk.PhotoImage(file = "images//sky.png")
    bgl = tk.Label(root, image=bgh)
    bgl.place(x=0, y=0, relwidth=1, relheight=1)
    bgl.image = bgh
    titleFont = Font(family="Arial", size="48")
    labelFont = Font(family="Arial", size="24")
    buttonFont = Font(family="Arial",size = "20")
    titleLabel=tk.Label(root,text=("Welcome"),font=titleFont,bg='red',fg='black')
    titleLabel.grid(row  = 0, column = 1,columnspan = 10,sticky="N",padx=10, pady=10)
    titleLabel=tk.Label(root,text="Enter Question:",font=labelFont,bg='red',fg='black').grid(sticky = "nsew",padx=10, pady=10)
    titleLabe2=tk.Label(root,text="Enter correct answer:",font=labelFont,bg='red',fg='black').grid(row = 2, column = 0,sticky = "nsew",padx=10, pady=10)
    titleLabe3=tk.Label(root,text="Enter wrong answer:",font=labelFont,bg='red',fg='black').grid(row = 3, column = 0,sticky = "nsew",padx=10, pady=10)
    titleLabe4=tk.Label(root,text="Enter another wrong answer:",font=labelFont,bg='red',fg='black').grid(row = 4, column = 0,sticky = "nsew",padx=10, pady=10)
    titleLabe5=tk.Label(root,text="Enter difficulty of question:",font=labelFont,bg='red',fg='black').grid(row = 5, column = 0,sticky = "nsew",padx=10, pady=10)
    Button=tk.Button(root,text="Submit",font=buttonFont,bg='yellow',fg='black',command=lambda : finish(e,e2,e3,e4,e5))
    Button.grid(row=6,column=5,columnspan = 3 ,sticky="nsew")
    tkvar = StringVar(root)
    choices = {'easy','medium','hard'}
    tkvar.set('easy')
    tkvar.trace('w',dropdown)
    e5 = OptionMenu(root,tkvar, *choices)
    e5.grid(row=5, column= 2, columnspan =4 ,sticky ="W")
    e = Entry(root)
    e.focus_set()
    e.grid(row=1, column= 2, columnspan =4 ,sticky = "W")
    e2 = Entry(root)
    e2.focus_set()
    e2.grid(row=2, column= 2, columnspan =4 ,sticky = "W")
    e3 = Entry(root)
    e3.focus_set()
    e3.grid(row=3, column= 2, columnspan =4 ,sticky = "W")
    e4 = Entry(root)
    e4.focus_set()
    e4.grid(row=4, column= 2, columnspan =4 ,sticky = "W")


def authentication():
    root = tk.Tk()
    root.lift()
    root.geometry('800x600')
    root.attributes("-topmost",True)
    password = "WOW"
    def ends():
        root.destroy()
    def submi(e):
        s = e.get()
        print(s)
        if s.upper() == password:
            root.destroy()
            insert()
        else:
            titleLabel=tk.Label(root,text="wrong",font=labelFont,bg='blue',fg='black').grid(row = 3, column = 1 ,sticky = "nsew",padx=10, pady=10)
            titleLabel=tk.Label(root,text="Returning to Main Menu",font=labelFont,bg='blue',fg='black').grid(row = 4, column = 1,sticky = "nsew",padx=10, pady=10)
            time.sleep(5)
            root.destroy()
    background_image=tk.PhotoImage(file = "images//sky2.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    root.geometry("700x400+0+0")
    background_label.image = background_image
    titleFont = Font(family="Arial", size="48")
    labelFont = Font(family="Arial", size="24")
    buttonFont = Font(family="Arial",size = "20")
    titleLabel=tk.Label(root,text=("Authentication"),font=titleFont,bg = 'red',fg='black')
    titleLabel.grid(row  = 0, column = 1,sticky="nsew",padx=10, pady=10)
    titleLabel=tk.Label(root,text="Enter password:",font=labelFont,bg = 'red',fg='black').grid(row = 2 , column = 0,sticky = "nsew",padx=10, pady=10)
    e = Entry(root)
    e.focus_set()
    e.grid(row=2, column= 1, sticky="",padx=10, pady=10)
    Button=tk.Button(root,text="Submit",font=buttonFont,bg='yellow',fg='black',command=lambda : submi(e))
    Button.grid(row=3,column=1,sticky="s")
    Button=tk.Button(root,text="Quit",font=buttonFont,bg='yellow',fg='black',command=ends)
    Button.grid(row=4,column=1,sticky="s",padx=10, pady=10)
    root.mainloop()
    
    

tr = False
fonts = pygame.font.SysFont(None,20)
fontm = pygame.font.SysFont(None,25)
fontl = pygame.font.SysFont(None,100)   
def textm(texts,colour):
    texx = fontm.render(texts,True, colour)
    return texx, texx.get_rect()
def textl(texts,colour):
    texx = fontl.render(texts,True,colour)
    return texx, texx.get_rect()
def texts(texts,colour):
    texx = fonts.render(texts,True,colour)
    return texx, texx.get_rect()
def btext(msg,colour,bx,by,bw,bh):
    texx,textre = textm(msg,colour)
    textre.center = ((bx+(bw/2)),(by+(bh/2)))
    window.blit(texx,textre)
def message(msg,colour,yd= 0,size= "small"):
    if size == "small":
        tex,textre = texts(msg,colour)
    if size == "large":
        tex,textre = textl(msg,colour)
    else:
        tex,textre = textm(msg,colour)
    textre.center = (int(W/2),int(H/2)+ yd)
    window.blit(tex,textre)
def instructions():
    instr = True
    
    pygame.event.get()
    while instr:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        window.fill((255,255,255))
        window.blit(mback , (0,0))
        message("instructions",
                white,-250,size = "large")
        message(" 1. UP key to jump",
                white,-180)
        message("2. DOWN key to slide",
                white,-150)
        message("3. Every 20 seconds you will be asked a question",
                white,-120)
        message("4. correct answer = continue the game",
                white,-90)
        message("5. wrong answer = you lose",
                white,-60)
        message("6. avoid the obsticles as well",
                white,-30)
        message("7. beat the high score by surviving and answering questions correctly",
                white,0)
        bbtext("play",150,500,150,50,red,light_green,action ="play")
        bbtext("update questions",350,400,150,50,red,light_green,action = "Update questions")
        bbtext("quit",550,500,150,50,red,light_green,action = "quit")
        if bbtext("play",150,500,150,50,red,light_green,action = "play") == True:
            run = True
            tr = True
            return run,tr
            
            
        pygame.display.update()
        clock.tick(15)

def bbtext(text,x,y,wi,hi,nor,usu,action):
    pygame.event.get()
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + wi > cur[0] > x and y+ hi >cur[1] > y:
        pygame.draw.rect(window,usu,(x,y,wi,hi))
        if click[0] == 1 and action != None:
            if action =="quit":
                pygame.quit()
                quit()
            if action == "Update questions":
                authentication()
            if action == "instructions":
                instructions()
            if action == "play":
                run = True
                return run
    else:
        pygame.draw.rect(window,nor,(x,y,wi,hi))
    btext(text,black,x,y,wi,hi)

def intro():
    intro = True
    
    pygame.event.get()
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        window.fill((255,255,255))
        window.blit(mback , (0,0))
        message("""Scroller Survival""",
                white,-200,size = "large")
        bbtext("play",350,150,150,50,red,light_green,action ="play")
        bbtext("instructions",350,250,150,50,red,light_green,action = "instructions")
        bbtext("update questions",350,350,150,50,red,light_green,action = "Update questions")
        bbtext("quit",350,450,150,50,red,light_green,action = "quit")
        if bbtext("play",350,150,150,50,red,light_green,action = "play") == True:
            run = True
            tr = True
            return run,tr
        pygame.display.update()
        clock.tick(15)


def endgame():
    global stop, obstacles, speed,score,playtime,time
    stop = 0
    obstacles = []
    speed = 30
    start = True
    while start:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                start = False
                sprite.hit = False
                sprite.Sliding = False
                sprite.Jumping = False
        window.blit(bg,(0,0))
        largeFont = pygame.font.SysFont('comicsans',80)
        previousScore = largeFont.render('High Score: ' + str(UpdateScore()),1 , (255,255,255))
        window.blit(previousScore,(W/2 - previousScore.get_width()/2,200))
        newScore = largeFont.render('Score: ' + str(score) , 1, (255,255,255))
        window.blit(newScore,(W/2 - newScore.get_width()/2,320 ))
        pygame.display.update()
    score = 0
    sprite.hit = False

def wrong():
    global stop, obstacles, speed,score,playtime,time
    stop = 0
    obstacles = []
    speed = 30
    start = True
    while start:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                start = False
                sprite.hit = False
                sprite.Sliding = False
                sprite.Jumping = False
        window.blit(bg,(0,0))
        largeFont = pygame.font.SysFont('comicsans',80)
        wrong = largeFont.render('Wrong',1,(255,255,255))
        window.blit(wrong,(500,320))
        pygame.display.update()

def welldone():
    start = True
    while start:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                start = False
                sprite.hit = False
                sprite.Sliding = False
                sprite.Jumping = False
    window.blit(bg,(0,0))
    largeFont = pygame.font.SysFont('comicsans',80)
    correct = largeFont.render('WellDone',1,(255,255,255))
    window.blit(correct,(500,320))
    pygame.display.update()
        


def leadscreen():
    roots = tk.Tk() 
    def exits(): 
        roots.destroy()
    def submit(e):
        string = e.get() 
        conn = sqlite3.connect("database\leaderboard.db")
        sql1 = """INSERT INTO lead(Name,Score)VALUES(?,?)"""
        cursor = conn.execute(sql1,(string,score,))
        conn.commit()
        rows = cursor.fetchall()
        print (string,rows)
        roots.destroy()
        intro()
    rows = leaderboard() 
    e = Entry(roots)
    e.focus_set()
    e.grid(row=1, column= 3, sticky="") 
    treeview = ttk.Treeview(roots) 
    roots.geometry("1000x400+0+0")
    roots.configure(background = "red")
    titleFont = Font(family="Arial", size="48")
    labelFont = Font(family="Arial", size="24")
    buttonFont = Font(family="Arial",size = "20")
    s = str(score) 
    scorelabel = "Your Score is : " + s 
    titleLabel=tk.Label(roots,text=("Leaderboard"),font=titleFont,bg='blue',fg='black') 
    titleLabel.grid(row=0,sticky="nsew",padx=10, pady=10) 
    titleLabel=tk.Label(roots,text="Enter Your Name:",font=labelFont,bg='blue',fg='black').grid(row = 0, column= 3, sticky = "E",padx=10, pady=10)
    titleLabel2=tk.Label(roots,text=(scorelabel),font=labelFont,bg='blue',fg='black').grid(row = 0, column= 4, sticky = "E",padx=10, pady=10)
    Button=tk.Button(roots,text="Submit",font=buttonFont,bg='blue',fg='lightblue',command = lambda : submit(e))
    ebutton = tk.Button(roots,text="exit",font=buttonFont,bg='blue',fg='lightblue',command = exits)
    roots.title("Leaderboard")
    treeview.grid(row=1,sticky="nsew",padx=10, pady=10)
    Button.grid(row=3,column=3,sticky="s")
    ebutton.grid(row=3,column=0,sticky="s")
    treeview.insert('','0','item1',text = rows[0][0])
    treeview.insert('','1','item2',text = rows[1][0])
    treeview.insert('','end','item3',text = rows[2][0])
    treeview.insert('','end','item4',text = rows[3][0])
    treeview.insert('','end','item5',text = rows[4][0])
    treeview.config(height = 5)
    treeview.item('item1',open = True)
    treeview.item('item1','open')
    treeview.config(columns =('scores')) 
    treeview.column('scores',width = 100,anchor = 'center')
    treeview.column('#0',width = 150)
    treeview.heading('#0',text = 'Name')
    treeview.heading('scores',text = 'Top Scores') 
    treeview.set('item1','scores',rows[0][1])
    treeview.set('item2','scores',rows[1][1])
    treeview.set('item3','scores',rows[2][1])
    treeview.set('item4','scores',rows[3][1])
    treeview.set('item5','scores',rows[4][1])
    mainloop()

def try_again():
    pygame.time.delay(300)
    root = tk.Tk()
    def end():
        pygame.quit()
        root.destroy()
        leadscreen()
        intro()
    def coll():
        window.blit(bg,(0,0))
        largeFont = pygame.font.SysFont('comicsans',80)
        wrong = largeFont.render('collision happened',1,(255,255,255))
        window.blit(wrong,(100,100))
        pygame.display.update()
        root.destroy()
        leadscreen()
    titleFont = Font(family="Arial", size="48")
    labelFont = Font(family="Arial", size="24")
    buttonFont = Font(family="Arial",size = "20")
    root.title("failed")
    root.geometry("500x500+0+0")
    root.configure(background = 'black')
    tlabel = tk.Label(root,text='You Failed',font = titleFont,bg='blue',fg='black')
    tlabel.pack()
    tbutton = tk.Button(root,text="Try again",font= buttonFont,bg='blue',fg='lightblue',command=coll)
    tbutton.pack()
    tbutton2 = tk.Button(root,text="Quit?",font= buttonFont,bg='blue',fg='lightblue',command=end)
    tbutton2.pack()
    root.mainloop()
def randoms():
    #determine answer order
    r = random.randint(1,3) 
    s = random.randint(1,3)
    f = random.randint(1,3)
    return r,s,f
def quiz(rows):
    root = tk.Tk()
    root.title("Quiz")
    root.geometry("800x447+300+300")
    root.configure(background='black')
    ques = random.randint(0,(len(database())-1))

    def close():
        if messagebox.askokcancel("Quit","Do you want to quit? " ):
            root.destroy()
            wrong()
            try_again()
    root.protocol("WM_DELETE_WINDOW", close)
        
    def print_answer(event,answer):
        canswer = Queue_Quiz.queue[0][1][1] 
        if (answer== canswer):
            root.destroy()
            welldone()
        else:
            root.destroy()
            wrong() 
            try_again()
            endgame()
    class question:
        def __init__(self,question):
            labelfont =('times', 20, 'bold')
            self.question = question
            self.label = tk.Label(root,text = question)
            self.label.config(bg ='black', fg = 'yellow') 
            self.label.config(font = labelfont)
            self.label.config(height = 1 , width= 30)
            self.label.pack()
            
    class answer:
        def __init__(self,answer):
            labelfont =('times', 15, 'bold')
            self.answer = answer
            self.label = tk.Label(root,text = self.answer)
            self.label.config(bg ='black', fg = 'yellow')
            self.label.config(font = labelfont)
            self.label.config(height = 1 , width= 20)
            self.label.bind("<Button-1>" , lambda event: print_answer(event, self.answer))
            self.label.pack(expand = 1) 
    def questions():
        r,s,f = randoms()
        while r == s or r == f or s == f: 
            r,s,f = randoms()
        q1= question(Queue_Quiz.queue[0][1][0]) 
        a1= answer(Queue_Quiz.queue[0][1][r])
        a2= answer(Queue_Quiz.queue[0][1][s])
        a3= answer(Queue_Quiz.queue[0][1][f])
        return q1,a1,a2,a3


    questions()
    root.mainloop()
    print(Queue_Quiz.get()) 
def draw_again():
    window.blit(bg, (Xs,Ys))
    window.blit(bg , (bg1,bg2))
    if sprite.Jumping == True:
        sprite.Jumps(window)
    elif sprite.Sliding == True:
        sprite.Slides(window)
    elif sprite.hit == True:
        sprite.Lose(window)
    else:
        sprite.Runs(window)
    for x in obstacles:
        x.Show(window)
    font = pygame.font.SysFont('comicsans',30)
    text = font.render('Score: ' + str(score),1,(255,255,255))
    window.blit(text,(700,10))
    font = pygame.font.SysFont('comicsans',30)
    timertext = font.render('Timer: ' + str(timer),1,(255,255,255))
    window.blit(timertext,(100,10))
    pygame.display.update()
def cScreen():
    start = True
    while start:
        pygame.time.delay(300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                t0 = time.time()
                t1 = time.time()
                start = False
        window.blit(bg,(0,0))
        largeFont = pygame.font.SysFont('comicsans',80)
        previousScore = largeFont.render('High Score: ' + str(UpdateScore()),1 , (255,255,255))
        window.blit(previousScore,(W/2 - previousScore.get_width()/2,200))
        newScore = largeFont.render('Score: ' + str(score) , 1, (255,255,255))
        window.blit(newScore,(W/2 - newScore.get_width()/2,320 ))
        pygame.display.update()
def times():
    t1 = time.time() 
    final_timer = int(t1 - t0)
    return final_timer
def t2():
    t2 = time.time() 
    return t2
sprite = player(200,315,50,50)
pygame.time.set_timer(USEREVENT+1,500)
pygame.time.set_timer(USEREVENT+2,random.randrange(3000,5000))
speed = 30
stop = 0
collision_speed = 0
obstacles = []
t0 = time.time()
rows = database()
Queue_Quiz = PriorityQueue()
queue(rows,Queue_Quiz)
start,tr = intro()
if tr == True:
    t0 = time.time()
else:
    tr = False
while start:
    score = speed//5 - 6
    if stop > 0:
        stop+= 1
        if stop > collision_speed:
            try_again()
            endgame()
            t0=t2()
    timer = times()
    if timer == 21:
        quiz(rows)
        cScreen()
        t0 = t2()
        times()
    for i in obstacles:
        if i.collide(sprite.collision): 
            sprite.hit = True
            if stop == 0:
                collision_speed = speed
                stop = 1   
        i.x -= 3
        if i.x < i.width * -1:
            obstacles.pop(obstacles.index(i))
    bg1 -= 1.4
    Xs -= 1.4
    if  bg1 > -W:
        bg1 = W
    if Xs < -W:
        Xs = W
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
            quit()
        if event.type == (USEREVENT+1):
            speed += 1
        if event.type == (USEREVENT+2):
            r= random.randrange(0,2)
            if r == 0:
                obstacles.append(saw(810,320,50,50))
            else:
                obstacles.append(spike(810,0,48,320))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if not(sprite.Jumping):
            sprite.Jumping = True
    if keys[pygame.K_DOWN] :
        if not(sprite.Sliding):
            sprite.Sliding = True
    draw_again()
    clock.tick(speed)
