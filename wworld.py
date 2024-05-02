import pygame as pg
import sys
import random
from connect_four import con_start
from Q_Learning_Tic_Tac_Toe import ttt_start

bg = (48, 39, 32)

room_size = 100
board_size = bwidth, bheight = 24,20
board_dim = bwidth*room_size//2, bheight*room_size//2
# print(board_dim)

Wind = pg.transform.scale(pg.image.load('./wind.png'),(900//9,769//9))
Stench = pg.transform.scale(pg.image.load('./stench.png'),(3239//51, 5137//51))
Monst = pg.transform.scale(pg.image.load('./monster.png'),(3489//48, 4806//48))
Tres = pg.transform.scale(pg.image.load('./treasure.png'),(100,100))
HMan = pg.transform.scale(pg.image.load('./man.png'),(100,100))
RBot = pg.transform.scale(pg.image.load('./bot.png'),(100,100))

fps = 60

window = pg.display.set_mode(board_dim)
pg.display.set_caption("Cave World")

class Pit:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        
        self.x = col*room_size+room_size//2
        self.y = row*room_size+room_size//2
        
        self.winds = []
        
        self.find_winds()
        
    def find_winds(self):
        w = self.row-1,self.col
        if(all(w) >= 0 and w[0]<bheight//2):
            self.winds.append(w)
        w = self.row+1,self.col
        if(all(w) >= 0 and w[0]<bheight//2):
            self.winds.append(w)
        w = self.row,self.col-1
        if(all(w) >= 0 and w[1]<bwidth//2):
            self.winds.append(w)
        w = self.row,self.col+1
        if(all(w) >= 0 and w[1]<bwidth//2):
            self.winds.append(w)
        w = self.row-1,self.col-1
        if(all(w) >= 0 and w[0]<bheight//2 and w[1]<bwidth//2):
            self.winds.append(w)
        w = self.row+1,self.col+1
        if(all(w) >= 0 and w[0]<bheight//2 and w[1]<bwidth//2):
            self.winds.append(w)
        w = self.row+1,self.col-1
        if(all(w) >= 0 and w[1]<bwidth//2 and w[0]<bheight//2):
            self.winds.append(w)
        w = self.row-1,self.col+1
        if(all(w) >= 0 and w[1]<bwidth//2 and w[0]<bheight//2):
            self.winds.append(w)
        
    def draw(self,window,bstate):
        for pos in self.winds:
            if "W" in bstate[pos[0]][pos[1]]:
                window.blit(Wind, (pos[1]*room_size, pos[0]*room_size))
        # pg.draw.rect(window, bg, (self.col*room_size, self.row*room_size, room_size, room_size))
        pg.draw.circle(window, (0,0,0), (self.x,self.y), room_size//2-6)
        
class Monster:
    def __init__(self, row, col):
        self.row = row
        self.col = col 
        
        self.x = col*room_size
        self.y = row*room_size
        
        self.stench = []
        
        self.find_stench()
        
    def find_stench(self):
        w = self.row-1,self.col
        if(all(w) >= 0 and w[0]<bheight//2):
            self.stench.append(w)
        w = self.row+1,self.col
        if(all(w) >= 0 and w[0]<bheight//2):
            self.stench.append(w)
        w = self.row,self.col-1
        if(all(w) >= 0 and w[1]<bwidth//2):
            self.stench.append(w)
        w = self.row,self.col+1
        if(all(w) >= 0 and w[1]<bwidth//2):
            self.stench.append(w)
        w = self.row-1,self.col-1
        if(all(w) >= 0 and w[0]<bheight//2 and w[1]<bwidth//2):
            self.stench.append(w)
        w = self.row+1,self.col+1
        if(all(w) >= 0 and w[0]<bheight//2 and w[1]<bwidth//2):
            self.stench.append(w)
        w = self.row+1,self.col-1
        if(all(w) >= 0 and w[1]<bwidth//2 and w[0]<bheight//2):
            self.stench.append(w)
        w = self.row-1,self.col+1
        if(all(w) >= 0 and w[1]<bwidth//2 and w[0]<bheight//2):
            self.stench.append(w)
        
    def draw(self,window):
        for pos in self.stench:
            window.blit(Stench, (pos[1]*room_size+12, pos[0]*room_size))
        # pg.draw.rect(window, bg, (self.col*room_size, self.row*room_size, room_size, room_size))
        window.blit(Monst, (self.x+12, self.y))
        
class Treasure:
    def __init__(self, row, col):
        self.row = row
        self.col = col 
        self.collected = False
        
        self.x = col*room_size
        self.y = row*room_size
        
    def draw(self,window):
        if(not self.collected):
            window.blit(Tres, (self.x, self.y))
        
class User:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.T = 0

        self.x = col*room_size
        self.y = row*room_size
        
    def draw(self,window):
        window.blit(HMan, (self.x,self.y))
        
    def up(self,window):
        if(self.row > 0):
            self.row -= 1
            self.y = self.row*room_size
        
    def down(self,window):
        if(self.row < bheight//2-1):
            self.row += 1
            self.y = self.row*room_size
        
    def left(self,window):
        if(self.col > 0):
            self.col -= 1
            self.x = self.col*room_size
        
    def right(self,window):
        if(self.col < bwidth//2-1):
            self.col += 1
            self.x = self.col*room_size

            
        
class Bot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.T = 0

        self.x = col*room_size
        self.y = row*room_size
        
        self.knowledge = [[""]*(bwidth//2) for i in range(bheight//2)]
        
        self.table = {
            #cur,left,right
            1 : [
    
            ],
            0: [
                ["S","S","S"],["W","W","W"]
            ]
        }
        
        self.P = {
            "": 1,
            "T":1,
            "W":1-1/75,
            "S":1-1/75,
            "WS":1-6/75,
            "TW":1-1/75,
            "TS":1-1/75,
            "TWS":1-4/75
        }
        
    def draw(self,window):
        window.blit(RBot, (self.x,self.y))
        
    def up(self,window):
        if(self.row > 0):
            self.row -= 1
            self.y = self.row*room_size
        
    def down(self,window):
        if(self.row < bheight//2-1):
            self.row += 1
            self.y = self.row*room_size
        
    def left(self,window):
        if(self.col > 0):
            self.col -= 1
            self.x = self.col*room_size
        
    def right(self,window):
        if(self.col < bwidth//2-1):
            self.col += 1
            self.x = self.col*room_size
            
    def prob3(self,c,l,r):
        safe = self.P[c]*self.P[l]*self.P[r]
        unsafe = (1-self.P[c])*(1-self.P[l])*(1-self.P[r])
        Safe = safe/(safe+unsafe)
        Unsafe = unsafe/(safe+unsafe)
        return [Unsafe,Safe]
    
    def prob2(self,c,l):
        safe = self.P[c]*self.P[l]
        unsafe = (1-self.P[c])*(1-self.P[l])
        Safe = safe/(safe+unsafe)
        Unsafe = unsafe/(safe+unsafe)
        return [Unsafe,Safe]
    
    def prob1(self,c):
        safe = self.P[c]
        unsafe = (1-self.P[c])
        Safe = safe/(safe+unsafe)
        Unsafe = unsafe/(safe+unsafe)
        return [Unsafe,Safe]
        
        
class Board:
    def __init__(self):
        self.pits = []
        self.ploc = []
        self.treas = []
        self.treses = []
        self.monst = None
        self.mloc = None
        self.man = None
        self.bot = None
        self.turn = 0
        self.pflag = False
        self.board_status = [[""]*(bwidth//2) for i in range(bheight//2)]
    
    def draw_box(self, window):
        window.fill(bg)
        for i in range(bwidth):
            for j in range(bheight):
                pg.draw.rect(window, (0,0,0), (i*room_size, j*room_size, room_size, room_size), 1)
                
    def create_board(self):
        pits = [random.sample(list(range(bwidth//2)), 4),random.sample(list(range(bheight//2)), 4)]
        # print(pits)
        self.ploc = pits
        for i in range(4):
            self.pits.append(Pit(pits[1][i],pits[0][i]))
            for j in self.pits[i].winds:
                try:
                    if self.board_status[j[0]][j[1]] == "":
                        self.board_status[j[0]][j[1]] = "W"
                except IndexError:
                    print(j)
            self.board_status[pits[1][i]][pits[0][i]] = "P"
        
        tees = [random.sample(list(range(bwidth//2)), 4),random.sample(list(range(bheight//2)), 4)]
        self.treses = tees
        for i in range(4):
            t = self.treses[0][i],self.treses[1][i]
            while(self.board_status[t[1]][t[0]] == 'P'):
                self.treses[0][i],self.treses[1][i] = random.choice(list(range(bwidth//2))),random.choice(list(range(bheight//2)))
                t = self.treses[0][i],self.treses[1][i]
            self.treas.append(Treasure(t[1],t[0]))
            self.board_status[t[1]][t[0]] += "T"
        
        mpos = random.choice(list(range(bwidth//2))),random.choice(list(range(bheight//2)))
        while("P" == any(self.board_status[mpos[1]-1:mpos[1]+2][mpos[0]-1:mpos[0]+2]) or "T" in self.board_status[mpos[1]][mpos[0]]):
            mpos = random.choice(list(range(bwidth//2))),random.choice(list(range(bheight//2)))
        self.mloc = mpos
        self.monst = Monster(mpos[1],mpos[0])
        self.board_status[mpos[1]][mpos[0]] = "M"
        for i in self.monst.stench:
            try:
                self.board_status[i[0]][i[1]] += "S"
            except IndexError:
                print(i)
        self.man = User(0,self.board_status[0].index(""))
        self.bot = Bot(bheight//2-1,self.board_status[-1].index(""))
        
                                
        # print(len(self.pits))
            
    def draw(self,window):
        self.draw_box(window)
        if not self.pflag:
            self.create_board()
            self.pflag = True
            print(self.board_status)
        for pit in self.pits:
            pit.draw(window,self.board_status)
        for t in self.treas:
            t.draw(window)
        self.monst.draw(window)
        self.man.draw(window)
        self.bot.draw(window)
        self.bot.knowledge[self.bot.row][self.bot.col] = self.board_status[self.bot.row][self.bot.col]

def main():
    run = True
    clock = pg.time.Clock()
    board = Board()
    
    while run:
        clock.tick(fps)
        
        board.draw(window)
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                print()
                print()
                print()
                print("User:",board.man.T)
                print("AI:",board.bot.T)
                print()
                print()
                print()
                run = False
            if(board.turn == 0):   
                if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    board.man.up(window)
                    board.turn = 1
                if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    board.man.down(window)
                    board.turn = 1
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                    board.man.left(window)
                    board.turn = 1
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                    board.man.right(window)
                    board.turn = 1
                manpos = board.man.row,board.man.col
                if("T" in board.board_status[manpos[0]][manpos[1]]):
                    board.man.T += 100
                    board.board_status[manpos[0]][manpos[1]] = "".join([x for x in board.board_status[manpos[0]][manpos[1]] if x!='T'])
                    for i in range(len(board.treas)):
                        t = board.treas[i]
                        if(t.row == board.man.row and t.col == board.man.col and not t.collected):
                            board.treas[i].collected = True
                if("P" in board.board_status[manpos[0]][manpos[1]]):
                    board.man.T = 0
                    board.man.row, board.man.col = 0,board.board_status[0].index("")
                    board.man.y, board.man.x = board.man.row*room_size, board.man.col*room_size
                if("M" in board.board_status[manpos[0]][manpos[1]]):
                    ttt_start()
                    out = ""
                    with open("ttt_out.txt","r") as f:
                        out += f.read()
                    if(out == "O"):
                        board.man.T = 0
                        board.man.row, board.man.col = 0,board.board_status[0].index("")
                        board.man.y, board.man.x = board.man.row*room_size, board.man.col*room_size
                    else:
                        board.man.row, board.man.col = 0,board.board_status[0].index("")
                        board.man.y, board.man.x = board.man.row*room_size, board.man.col*room_size
                if(board.man.row == board.bot.row and board.man.col == board.bot.col):
                    winner = con_start()
                    pg.display.set_mode(board_dim)
                    board.draw(window)
                    if(winner == 1):
                        board.man.T += board.bot.T/2
                        board.bot.T /= 2
                    else:
                        board.bot.T += board.man.T/2
                        board.man.T /= 2
                    board.man.row, board.man.col = [board.man.row,board.man.row-1][board.man.row != 0], [board.man.col,board.man.col-1][board.man.col != 0]
                    board.man.y, board.man.x = board.man.row*room_size, board.man.col*room_size
                    board.bot.row, board.bot.col = [board.bot.row,board.bot.row+1][board.bot.row < bheight//2-1], [board.bot.col,board.bot.col+1][board.bot.col < bwidth//2-1]
                    board.bot.y, board.bot.x = board.bot.row*room_size, board.bot.col*room_size
            
            elif(board.turn == 1):
                p = []
                #up
                c , l , r = (board.bot.row,board.bot.col),(board.bot.row,board.bot.col-1),(board.bot.row,board.bot.col+1)
                if(all(l)>=0 and l[1]<=bwidth//2-1 and l[0]<=bheight//2-1 and all(r)>=0 and r[1]<=bwidth//2-1 and r[0]<=bheight//2-1):
                    cc = board.bot.knowledge[c[0]][c[1]]
                    ll = board.bot.knowledge[l[0]][l[1]]
                    rr = board.bot.knowledge[r[0]][r[1]]
                    p = board.bot.prob3(cc,ll,rr)
                elif(all(r)>=0 and r[1]<=bwidth//2-1 and r[0]<=bheight//2-1):
                    cc = board.bot.knowledge[c[0]][c[1]]
                    rr = board.bot.knowledge[r[0]][r[1]]
                    p = board.bot.prob2(cc,rr)
                elif(all(l)>=0 and l[1]<=bwidth//2-1 and l[0]<=bheight//2-1):
                    cc = board.bot.knowledge[c[0]][c[1]]
                    ll = board.bot.knowledge[l[0]][l[1]]
                    p = board.bot.prob2(cc,ll)
                else:
                    cc = board.bot.knowledge[c[0]][c[1]]
                    p = board.bot.prob1(cc)
                
                #down    
                c , l , r = (board.bot.row,board.bot.col),(board.bot.row,board.bot.col+1),(board.bot.row,board.bot.col-1)
                if(all(l)>=0 and l[1]<=bwidth//2-1 and l[0]<=bheight//2-1 and all(r)>=0 and r[1]<=bwidth//2-1 and r[0]<=bheight//2-1):
                    cc = board.bot.knowledge[c[0]][c[1]]
                    ll = board.bot.knowledge[l[0]][l[1]]
                    rr = board.bot.knowledge[r[0]][r[1]]
                    p.extend(board.bot.prob3(cc,ll,rr))
                elif(all(r)>=0 and r[1]<=bwidth//2-1 and r[0]<=bheight//2-1):
                    cc = board.bot.knowledge[c[0]][c[1]]
                    rr = board.bot.knowledge[r[0]][r[1]]
                    p.extend(board.bot.prob2(cc,rr))
                elif(all(l)>=0 and l[1]<=bwidth//2-1 and l[0]<=bheight//2-1):
                    cc = board.bot.knowledge[c[0]][c[1]]
                    ll = board.bot.knowledge[l[0]][l[1]]
                    p.extend(board.bot.prob2(cc,ll))
                else:
                    cc = board.bot.knowledge[c[0]][c[1]]
                    p.extend(board.bot.prob1(cc))
                
                #left   
                c , l , r = (board.bot.row,board.bot.col),(board.bot.row+1,board.bot.col),(board.bot.row-1,board.bot.col)
                if(all(l)>=0 and l[1]<=bwidth//2-1 and l[0]<=bheight//2-1 and all(r)>=0 and r[1]<=bwidth//2-1 and r[0]<=bheight//2-1):
                    cc = board.bot.knowledge[c[0]][c[1]]
                    ll = board.bot.knowledge[l[0]][l[1]]
                    rr = board.bot.knowledge[r[0]][r[1]]
                    p.extend(board.bot.prob3(cc,ll,rr))
                elif(all(r)>=0 and r[1]<=bwidth//2-1 and r[0]<=bheight//2-1):
                    cc = board.bot.knowledge[c[0]][c[1]]
                    rr = board.bot.knowledge[r[0]][r[1]]
                    p.extend(board.bot.prob2(cc,rr))
                elif(all(l)>=0 and l[1]<=bwidth//2-1 and l[0]<=bheight//2-1):
                    cc = board.bot.knowledge[c[0]][c[1]]
                    ll = board.bot.knowledge[l[0]][l[1]]
                    p.extend(board.bot.prob2(cc,ll))
                else:
                    cc = board.bot.knowledge[c[0]][c[1]]
                    p.extend(board.bot.prob1(cc))
                
                #right 
                c , l , r = (board.bot.row,board.bot.col),(board.bot.row-1,board.bot.col),(board.bot.row+1,board.bot.col)
                if(all(l)>=0 and l[1]<=bwidth//2-1 and l[0]<=bheight//2-1 and all(r)>=0 and r[1]<=bwidth//2-1 and r[0]<=bheight//2-1):
                    cc = board.bot.knowledge[c[0]][c[1]]
                    ll = board.bot.knowledge[l[0]][l[1]]
                    rr = board.bot.knowledge[r[0]][r[1]]
                    p.extend(board.bot.prob3(cc,ll,rr))
                elif(all(r)>=0 and r[1]<=bwidth//2-1 and r[0]<=bheight//2-1):
                    cc = board.bot.knowledge[c[0]][c[1]]
                    rr = board.bot.knowledge[r[0]][r[1]]
                    p.extend(board.bot.prob2(cc,rr))
                elif(all(l)>=0 and l[1]<=bwidth//2-1 and l[0]<=bheight//2-1):
                    cc = board.bot.knowledge[c[0]][c[1]]
                    ll = board.bot.knowledge[l[0]][l[1]]
                    p.extend(board.bot.prob2(cc,ll))
                else:
                    cc = board.bot.knowledge[c[0]][c[1]]
                    p.extend(board.bot.prob1(cc))
                    
                if(p.index(max(p))%2 == 0):
                    random.choice([board.bot.up,board.bot.down,board.bot.right,board.bot.left])(window)
                else:
                    ind = p.index(max(p))
                    if(ind == 5 and board.bot.col != 0):
                        board.bot.left(window)
                    elif(ind == 3 and board.bot.row != bheight//2-1):
                        board.bot.down(window)                        
                    elif(ind == 1 and board.bot.row != 0):
                        board.bot.up(window)                   
                    elif(ind == 7 and board.bot.col != bheight//2-1):
                        board.bot.right(window)   
                    else:
                        random.choice([board.bot.up,board.bot.down,board.bot.right,board.bot.left])(window)  
                board.turn = 0          
                
                manpos = board.bot.row,board.bot.col
                if("T" in board.board_status[manpos[0]][manpos[1]]):
                    board.bot.T += 100
                    board.board_status[manpos[0]][manpos[1]] = "".join([x for x in board.board_status[manpos[0]][manpos[1]] if x!='T'])
                    for i in range(len(board.treas)):
                        t = board.treas[i]
                        if(t.row == board.bot.row and t.col == board.bot.col and not t.collected):
                            board.treas[i].collected = True
                if("P" in board.board_status[manpos[0]][manpos[1]]):
                    board.bot.T = 0
                    board.bot.row, board.bot.col = 0,board.board_status[0].index("")
                    board.bot.y, board.bot.x = board.bot.row*room_size, board.bot.col*room_size
                if("M" in board.board_status[manpos[0]][manpos[1]]):
                    board.bot.T = 0
                    board.bot.row, board.bot.col = 0,board.board_status[0].index("")
                    board.bot.y, board.bot.x = board.bot.row*room_size, board.bot.col*room_size
                if(board.man.row == board.bot.row and board.man.col == board.bot.col):
                    winner = con_start()
                    pg.display.set_mode(board_dim)
                    board.draw(window)
                    if(winner == 1):
                        board.man.T += board.bot.T/2
                        board.bot.T /= 2
                    else:
                        board.bot.T += board.man.T/2
                        board.man.T /= 2
                    board.man.row, board.man.col = [board.man.row,board.man.row-1][board.man.row != 0], [board.man.col,board.man.col-1][board.man.col != 0]
                    board.man.y, board.man.x = board.man.row*room_size, board.man.col*room_size
                    board.bot.row, board.bot.col = [board.bot.row,board.bot.row+1][board.bot.row < bheight//2-1], [board.bot.col,board.bot.col+1][board.bot.col < bwidth//2-1]
                    board.bot.y, board.bot.x = board.bot.row*room_size, board.bot.col*room_size    
                board.turn = 0
                    
                    
    
        pg.display.update()

    pg.quit()
    sys.exit()
        
main()