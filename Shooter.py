# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 15:54:01 2019

@author: Martin
"""


import pygame
from os import chdir

chdir('C:\\Users\\Martin\\Desktop\\Programmation\\Shooter')

pygame.init()

width = 400
height = 400
rows = 8
columns = 8
dist = width//rows

color_black = (0, 0, 0)
color_white = (255, 255, 255)
backwhite = (250, 236, 192)
backbrown = (206, 159, 96)
whiteChosen = (249, 177, 113)
blackChosen = (224, 141, 58)
whiteAiming = (135, 239, 137)
blackAiming = (55, 149, 53)

whiteKingImg = pygame.image.load('White King.png')
blackKingImg = pygame.image.load('Black King.png')
whiteSquireImg = pygame.image.load('White Squire.png')
blackSquireImg = pygame.image.load('Black Squire.png')
whiteShooterImg = pygame.image.load('White Shooter.png')
blackShooterImg = pygame.image.load('Black Shooter.png')
bulletImg = pygame.image.load('Bullet.png')

kingMoves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
shooterMoves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
squireMoves = [(-2, 0), (-1, -1), (0, -2), (1, -1), (2, 0), (1, 1), (0, 2), (-1, 1)]
shooterAiming = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (0, 0)]

myfont = pygame.font.SysFont('Comic Sans MS', 15, 1)

class Color:
    
    def __init__(self, opposite, ownPieces, oppositePieces):
        self.opposite = opposite
        self.ownPieces = ownPieces
        self.oppositePieces = oppositePieces
       
#Color class has the opposite color and the lists of pieces as attributes (own and enemy pieces)
#White's opposite is black, white's opposite pieces are black own pieces and vice versa
#Empty's opposite is just the string 'empty' as I only call the opposite attribute when color is different than empty

#I use a global variable called board which is the matrix that stores the information of every piece
#Each one of these is distinguished by its color and its index on the color ownPieces list
#That's why on board every case stocks a tuple (color, ind) that spots every piece
#If a case is empty by convention it's filled with the tuple (empty, 0)

#I choosed this kind of structure because stocking directly every piece on a global matrix would require to create an empty piece
#that has the same attributes than all other pieces. I'm not pretty sure about how this would work but we can always try to 
#implement this other form of structure

class Piece:
    
    def __init__(self, x, y, moves, color, img):
        self.x = x
        self.y = y
        self.alive = True        
        self._moves = moves
        self._img = img
        self.chosen = False
        self._color = color
        self._color.ownPieces.append(self)
        self._color.opposite.oppositePieces.append(self)
        
    #When a piece is initialized it's appended to it's own color list of pieces and to the opposite too
        
    def valid_space(self):
        pos = []
        for dl in self._moves:
            dx, dy = dl
            if (self.x+dx)>=0 and (self.x+dx)<columns and (self.y+dy)>=0 and (self.y+dy)<rows:
                if board[self.x+dx][self.y+dy][0]!=self._color:
                    pos.append((self.x+dx, self.y+dy))
        return pos
    
    #valid_space returns the positions where a piece can move, considering the own color ones but also the edges
    
    def move(self, i, j):
        if (i, j) in self.valid_space():
            _, ownInd = board[self.x][self.y]
            board[self.x][self.y] = (empty, 0)
            color, ind = board[i][j]
            self.x = i
            self.y = j
            if color!=empty:
                self._color.oppositePieces[ind].alive = False
            board[i][j] = (self._color, ownInd)
          
    
    def drawPossibleMoves(self, surface):
        for pos in self.valid_space():
            i, j = pos
            if (i+j)%2==0:
                pygame.draw.rect(surface, whiteChosen, (i*dist, j*dist, dist, dist))
            else:
                pygame.draw.rect(surface, blackChosen, (i*dist, j*dist, dist, dist))


class King(Piece):
    
    def __init__(self, x, y, color, image):
        Piece.__init__(self, x, y, kingMoves, color, image)
        textColor = 'White'
        if self._color==black:
            textColor = 'Black'
        print('A '+textColor+' King has been created')
        
    def draw(self, surface):
        if self.alive:
            surface.blit(self._img, (self.x*dist, self.y*dist))
        

class Squire(Piece):
    
    def __init__(self, x, y, color, img):
        Piece.__init__(self, x, y, squireMoves, color, img)
        self.shield = 3
        textColor = 'White'
        if self._color==black:
            textColor = 'Black'
        print('A '+textColor+' Squire has been created')
        
    #A Squire has a shield level, it's value here is 3: you have to shoot him 3 times to manage to kill him
        
    def draw(self, surface):
        if self.alive:
            surface.blit(self._img, (self.x*dist, self.y*dist))
            shieldLevel = myfont.render(str(self.shield), False, (0, 0, 0))
            surface.blit(shieldLevel, (self.x*dist, self.y*dist+30))


class Shooter(Piece):
    
    def __init__(self, x, y, color, img):
        Piece.__init__(self, x, y, shooterMoves, color, img)
        self.ammo = 5
        self.aimingSpots = shooterAiming
        textColor = 'White'
        if self._color==black:
            textColor = 'Black'
        print('A '+textColor+' Shooter has been created')
            
    def valid_aiming(self):
        spots = []
        for pos in shooterAiming:
            i, j = pos
            if (self.x+i)>=0 and (self.x+i)<columns and (self.y+j)>=0 and (self.y+j)<rows:
                color , ind = board[self.x+i][self.y+j]
                if color!=self._color:
                    spots.append(((self.x+i), (self.y+j)))
        return spots
    
    #A Shooter can shoot at any direction: there is friend fire. If you shoot to a partner piece it will affect it just as much
    #as if it was on the other team. Shooter's ammunition is finite and it's initial value is 5.
    
    def draw(self, surface):
        if self.alive:
            surface.blit(self._img, (self.x*dist, self.y*dist))
            ammoDisp = myfont.render(str(self.ammo), False, (0, 0, 0))
            surface.blit(ammoDisp, (self.x*dist, self.y*dist-5))
            
    #Here ammoDisp is just a Surface object that contains the string containing the value of a Shooter's ammo
    
    def drawAiming(self, surface):
        for pos in self.valid_aiming():
            i, j = pos
            if (i+j)%2==0:
                pygame.draw.rect(surface, whiteAiming, (i*dist, j*dist, dist, dist))
            else:                
                pygame.draw.rect(surface, blackAiming, (i*dist, j*dist, dist, dist))
                
class Bullet:    
    
    #bullet position is not an int on the grid but real coordinates on the surface display
    #thanks to that it's easier to display it while moving
    
    def __init__(self, x, y, dirnx, dirny, color, img):
        self.x = x
        self.y = y
        self.dirnx = dirnx
        self.dirny = dirny
        self.stx = 0
        self.sty = 0
        self.color = color
        self._image = img
        self.triggered = False
        self.collided = False
        
    def biais(self):
        d = dist//2
        temp = [(-d, -d), (-d, d), (-d, 3*d), (d, 3*d), (3*d, 3*d), (3*d, d), (3*d, -d), (d, -d), (0, 0)]
        i = shooterAiming.index((self.dirnx, self.dirny))
        return temp[i]            
    
    #As a bullet hits everybody the same way no matter what the color is I had to use an initial translation so the bullet does not
    #kill the shooter at the very beginning
        
    def move(self):
        if (self.x+self.dirnx)>=0 and (self.x+self.dirnx)<width and (self.y+self.dirny)>=0 and (self.y+self.dirny)<height:
            self.x+=self.dirnx
            self.y+=self.dirny
        else:
            self.collided = True
            self.triggered = False   
    
    def collide(self):
        color, ind = board[self.x//dist][self.y//dist]
        if color!=empty:
            self.triggered = False
            self.collided = True
            if type(color.ownPieces[ind])==Squire:
                if color.ownPieces[ind].shield>1:
                    color.ownPieces[ind].shield-=1                    
                else:
                    color.ownPieces[ind].alive = False
                    board[self.x//dist][self.y//dist] = (empty, 0)

            else:
                color.ownPieces[ind].alive = False
                board[self.x//dist][self.y//dist] = (empty, 0)

    def reset(self):
        self.x = 0
        self.y = 0
        self.dirnx = 0
        self.dirny = 0
        self.color = empty
        self.triggered = False
        self.collided = False
        
    def draw(self, surface):
        surface.blit(self._image, (self.x-5, self.y))
    
def interaction():
    global chosenPiece
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        pres = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            show_board()        
        if pres[0]:
            tempx, tempy = pygame.mouse.get_pos()
            posx = tempx//dist
            posy = tempy//dist
            if chosenPiece:
                chosenColor, chosenInd = chosenPiece[0]
                chosenColor.ownPieces[chosenInd].move(posx, posy)
                chosenColor.ownPieces[chosenInd].chosen = False
                chosenPiece = []
            else:
                color, ind = board[posx][posy]
                if color!=empty:
                    chosenPiece = [board[posx][posy]]
                    color.ownPieces[ind].chosen = True
        if pres[2]:
            tempx, tempy = pygame.mouse.get_pos()
            posx = tempx//dist
            posy = tempy//dist
            if chosenPiece:
                chosenColor, chosenInd = chosenPiece[0]
                if type(chosenColor.ownPieces[chosenInd])==Shooter:
                    ownx = chosenColor.ownPieces[chosenInd].x
                    owny = chosenColor.ownPieces[chosenInd].y
                    if (posx-ownx, posy-owny) in chosenColor.ownPieces[chosenInd].aimingSpots:
                        if chosenColor.ownPieces[chosenInd].ammo>0:
                            if chosenColor==white:
                                whiteBall.dirnx = (posx-ownx)
                                whiteBall.dirny = (posy-owny)
                                whiteBall.x = ownx*dist+whiteBall.biais()[0]
                                whiteBall.y = owny*dist+whiteBall.biais()[1]
                                whiteBall.color = chosenColor
                                whiteBall.triggered = True
                                whiteBall.stx = posx
                                whiteBall.sty = posy
                            elif chosenColor==black:
                                blackBall.dirnx = (posx-ownx)
                                blackBall.dirny = (posy-owny)
                                blackBall.x = ownx*dist+blackBall.biais()[0]
                                blackBall.y = owny*dist+blackBall.biais()[1]
                                blackBall.color = chosenColor
                                blackBall.triggered = True
                                blackBall.stx = posx
                                blackBall.sty = posy
                            chosenColor.ownPieces[chosenInd].ammo-=1
                            print('FIIIREEEEEEE')
                        else:
                            print('This shooter has no more ammunition')
                    chosenColor.ownPieces[chosenInd].chosen = False
                    chosenPiece = []
    if whiteBall.triggered:
        whiteBall.move()
        whiteBall.collide()
    if whiteBall.collided:
        whiteBall.reset()
    if blackBall.triggered:
        blackBall.move()
        blackBall.collide()
    if blackBall.collided:
        blackBall.reset()
                    
            
def show_board():
    temp = [['empty']*columns for k in range(rows)]
    for i in range(columns):
        for j in range(rows):
            color, _ = board[i][j]
            if color==white:
                temp[j][i] = 'white'
            elif color==black:
                temp[j][i] = 'black'
    print(temp)

                
def drawBoard(surface):
    for i in range(rows):
        for j in range(columns):
            if (i+j)%2==0:
                pygame.draw.rect(surface, backwhite, (i*dist, j*dist, dist, dist))
            else:
                pygame.draw.rect(surface, backbrown, (i*dist, j*dist, dist, dist))
                
        
def redrawWindow(surface):
    drawBoard(surface)
    for whiteItem in white.ownPieces:
        if whiteItem.chosen:
            whiteItem.drawPossibleMoves(surface)
            if type(whiteItem)==Shooter:
                whiteItem.drawAiming(surface)
    for blackItem in black.ownPieces:
        if blackItem.chosen:
            blackItem.drawPossibleMoves(surface)
            if type(blackItem)==Shooter:
                blackItem.drawAiming(surface)
    for whiteItem in white.ownPieces:
        whiteItem.draw(surface)
    for blackItem in black.ownPieces:
        blackItem.draw(surface)
    if whiteBall.triggered:
        whiteBall.draw(surface)
    if blackBall.triggered:
        blackBall.draw(surface)

    pygame.display.update()
    
def main():
    global board, white, black, empty, win, whiteBall, blackBall, chosenPiece
    
    win = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    
    white = Color('temp', [], [])
    black = Color(white, [], [])
    empty = Color('empty', [], [])
    white.opposite = black
    
    whiteKing = King(4, 7, white, whiteKingImg)
    whiteSquire1 = Squire(3, 6, white, whiteSquireImg)
    whiteSquire2 = Squire(5, 6, white, whiteSquireImg)
    whiteShooter1 = Shooter(3, 7, white, whiteShooterImg)
    whiteShooter2 = Shooter(5, 7, white, whiteShooterImg)
    blackKing = King(4, 0, black, blackKingImg)
    blackSquire1 = Squire(3, 1 ,black, blackSquireImg)
    blackSquire2 = Squire(5, 1, black, blackSquireImg)
    blackShooter1 = Shooter(3, 0, black, blackShooterImg)
    blackShooter2 = Shooter(5, 0, black, blackShooterImg)
    
    chosenPiece = []
    whiteBall = Bullet(0, 0, 0, 0, white, bulletImg)
    blackBall = Bullet(0, 0, 0, 0, black, bulletImg)
        
    board = [[(empty, 0)]*columns for k in range(rows)]
    for ind, whiteItem in enumerate(white.ownPieces):
        board[whiteItem.x][whiteItem.y] = (white, ind)
    for ind, blackItem in enumerate(black.ownPieces):
        board[blackItem.x][blackItem.y] = (black, ind)
                        
    while whiteKing.alive and blackKing.alive:
        clock.tick(90)
        interaction()
        redrawWindow(win) 
        
    pygame.quit()
    
    
main()
