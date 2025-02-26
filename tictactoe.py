import sys
import pygame
import numpy as np

from constants import *

#PYGAME Setup
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BG_COLOR)

class Board():

    def __init__(self):

        self.squares=np.zeros((ROWS,COLS))
        self.empty_sqrs=self.squares
        self.marked_sqrs=0

    def final_state(self):
        '''
        @return 0 if no win
        @return 1 if 1 win
        @return 2 if 2 win
        '''

        #vertical wins
        for col in range(COLS):
            if self.squares[0][col]==self.squares[1][col]==self.squares[2][col] !=0:
                return self.squares[0][col]

        #horizontal wins
        for row in range(ROWS):
            if self.squares[row][0]==self.squares[row][1]==self.squares[row][2] !=0:
                return self.squares[row][0]

        #desc_diagonal wins
        if self.squares[0][0]==self.squares[1][1]==self.squares[2][2]!=0:
            return self.squares[1][1]

        #asc_diagonal wins
        if self.squares[0][2]==self.squares[1][1]==self.squares[2][0]!=0:
            return self.squares[1][1]

        #no win yet
        return 0

    def mark_sqr(self,row,col,player):
        self.squares[row][col]=player
        self.marked_sqrs+=1

    def empty_sqr(self,row,col):
        return self.squares[row][col]==0

    def get_empty_sqrs(self):
        empty_sqrs=[]
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs==9

    def isempty(self):
        return self.marked_sqrs==0
class Game:

    def __init__(self):
        self.Board=Board()
        self.player=1 #1->cross, 2->circle
        self.show_lines()

    def show_lines(self):
        #vertical
        pygame.draw.line(screen,LINE_COLOR,(SQSIZE,0),(SQSIZE,HEIGHT),LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(WIDTH-SQSIZE,0),(WIDTH-SQSIZE,HEIGHT),LINE_WIDTH)
        #horizontal
        pygame.draw.line(screen,LINE_COLOR,(0,SQSIZE),(WIDTH,SQSIZE),LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(0,HEIGHT-SQSIZE),(WIDTH,HEIGHT-SQSIZE),LINE_WIDTH)

    def next_turn(self):
        self.player=self.player%2+1

    def draw_fig(self,row,col):

        if self.player==1:

            #cross_descending_line
            start_desc=(col*SQSIZE+OFFSET,row*SQSIZE+OFFSET)
            end_desc=(col*SQSIZE+SQSIZE-OFFSET,row*SQSIZE+SQSIZE-OFFSET)
            pygame.draw.line(screen,CROSS_COLOR,start_desc,end_desc,CROSS_WIDTH)

            #cross_ascending_line
            start_asc=(col*SQSIZE+OFFSET,row*SQSIZE+SQSIZE-OFFSET)
            end_asc=(col*SQSIZE+SQSIZE-OFFSET,row*SQSIZE+OFFSET)
            pygame.draw.line(screen,CROSS_COLOR,start_asc,end_asc,CROSS_WIDTH)

        elif self.player==2:
            #circle
            center=(col*SQSIZE+SQSIZE//2,row*SQSIZE+SQSIZE//2)
            pygame.draw.circle(screen,CIRC_COLOR,center,RADIUS,CIRCLE_WIDTH)



def main():
    #object
    game = Game()
    board=game.Board

    #mainloop
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=event.pos
                row=pos[1]//SQSIZE
                col=pos[0]//SQSIZE
                print(row,col)

                if board.empty_sqr(row,col):
                    board.mark_sqr(row,col,game.player)
                    game.draw_fig(row,col)
                    game.next_turn()
                    print(board.squares)
        pygame.display.update()
main()