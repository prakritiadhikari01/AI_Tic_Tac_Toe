lass AI():

    def __init__(self,level=1,player=2):
        self.level=level
        self.player=player

    def rnd(self,board):
        empty_sqrs=board.get_empty_sqrs()
        idx=random.randrange(0,len(empty_sqrs))

        return empty_sqrs[idx]

    def minimax(self,board,maximizing):

        #terminal states
        case=board.final_state()

        #player 1 wins
        if case ==1:
            return 1,None
        #player 2 wins
        elif case==2:
            return -1,None
        #draw
        elif board.isfull():
            return 0,None

        if maximizing:
            max_eval=-100
            best_move=None
            empty_sqrs=board.get_empty_sqrs()

            for (row,col) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.mark_sqr(row,col,1)
                eval=self.minimax(temp_board,False)[0]
                if eval>max_eval:
                    max_eval=eval
                    best_move=(row,col)

            return max_eval,best_move

        elif not maximizing:
            min_eval=100
            best_move=None
            empty_sqrs=board.get_empty_sqrs()

            for (row,col) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.mark_sqr(row,col,self.player)
                eval=self.minimax(temp_board,True)[0]
                if eval<min_eval:
                    min_eval=eval
                    best_move=(row,col)

            return min_eval,best_move

    def eval (self,main_board):
        if self.level ==0:
            #random choice
            eval="random"
            move=self.rnd(main_board)
        else:
            #minimax algo choice
            eval,move=self.minimax(main_board,False)

        print("AI has chosen to mark the square in pos",move,"with an eval of",eval)
        return move
class Game:

    def __init__(self):
        self.Board=Board()
        self.ai=AI()
        self.player=1 #1->cross, 2->circle
        self.gamemode="ai"
        self.running= True
        self.show_lines()

    def show_lines(self):
        #BG
        screen.fill(BG_COLOR)
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

    def make_move(self,row,col):
        self.Board.mark_sqr(row,col,self.player)
        self.draw_fig(row,col)
        self.next_turn()

    def change_gamemode(self):
        self.gamemode = "ai" if self.gamemode == "pvp" else "pvp"

    def isover(self):
        return self.Board.final_state(show=True) !=0 or self.Board.isfull()

    def reset(self):
        self.__init__()