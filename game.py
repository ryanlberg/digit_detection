import pygame, sys
from keras.models import load_model
from cell import cell
from tkinter import *
from tkinter import messagebox
import numpy as np

pygame.init()
font = pygame.font.SysFont("Courier New", 36)
size = width, height = (600, 800)
white = (255,255,255)
black = (0,0,0)
gray = (128, 128, 128)
screen = pygame.display.set_mode(size)

def setup():
    board = []
    size = 20
    for x in range(28):
        currow = [] 
        for y in range(28):
            currow.append(cell(size*(x+1), (y+1)*size, size))
        board.append(currow)
    return board

def translate(x, y):
    posx = (x-20) // 20
    posy = (y-20) // 20
    return posx, posy

def convertTo(board):
    out = []
    for x in range(28):
        currow = []
        for y in range(28):
            cell = board[y][x]
            if cell.color == white:
                currow.append(0)
            else:
                currow.append(1)
        out.append(currow)
    return np.array(out)

class button():

    def __init__(self, color, x, y, width, height, text= ""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self):
        border = 3
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        button_text_surf = font.render(self.text, True, black)
        pygame.draw.rect(screen, black, button_rect, border) 
        textx = self.x +(self.width//2- button_text_surf.get_width()//2)
        texty = self.y + (self.height//2 - button_text_surf.get_height()//2)
        screen.blit(button_text_surf, (textx, texty))


def getPred(model, input):
    sample = input.reshape((1, 28, 28, 1))
    prediction = model.predict(sample)
    return np.argmax(prediction, axis=1)[0]
    

if __name__ == "__main__":
    model = load_model("model.h5")
    board = setup()
    button1 = button(gray, 240, 675, 120, 50, "Guess")
    while True:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type ==  pygame.QUIT:
                sys.exit()


            if pygame.mouse.get_pressed()[0]:
                
                x, y = mouse_pos[0], mouse_pos[1]
                posx, posy = translate(x, y)
                if posx >= 0 and posx < 28 and posy >= 0 and posy < 28:
                    board[posx][posy].click()

                elif x >= 240 and x <= (240+120) and y >= 675 and y <= (675+50):
                    b = convertTo(board)
                    Tk().wm_withdraw()
                    pred = getPred(model, b)
                    messagebox.showinfo("Guess", str(pred))
                    board = setup()

               
        screen.fill(white)
        button1.draw()
        for x in board:
            for y in x:
                y.draw(screen)
        pygame.display.update()