#!/usr/bin/python3

#last mod: corrected SFEN-List to contain "-" for empty captured list 26.5.17

from tkinter import  *
from tkinter import filedialog
from tkinter import messagebox
from copy import deepcopy
import array


import sys
import time
# 4.6.17: 王 added as Kanji for King
# 11.9.18 bugfix: korrekte Erstellung von Listen genommener Steine
class App:


    def __init__(self, master):
        # Board and Encoding
        #Files
        self.F ={'一':1, '二':2,'三':3,'四':4,'五':5, '六':6,'七':7,'八':8,'九':9}
        self.G ={1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h',9:'i'}
        #Kanji are unique!!
        #Pieces  
        self.P = {  '歩':'P', '香':'L', '桂': 'N', '銀':'S', '金':'G', '飛':'R', '角':'B', '玉':'K', '王':'K','龍':'+R', '竜':'+R', '馬':'+B', '全':'+S',\
                    '圭':'+N', '杏':'+L', 'と':'+P'}
        #Terms
        self.T = {'打': 'Drop', '上':'Forward',"行":'Forward','引':'Backward','寄':'Sideward','左':'Left','右':'Right','成':'Promotion','直':'Upright','不成':'Without Promotion',\
                  '同': 'Same', '投':'Resign','了':'Resign', "千":'Repetition', "待":'Draw','中':'Interrupted','▲': 'Sente', '△':'Gote'}
                #, "千日手":'Repetition', "待将棋":'Draw','中断':'Interrupted' }
        #Board normal notation: P3g entspr. P36
        self.B =  ['L','N','S','G','K','G','S','N','L'],[' ','B',' ',' ',' ',' ',' ','R',' '], ['P','P','P','P','P','P','P','P','P'],[' ',' ',' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ',' ',' '],\
            [' ',' ',' ',' ',' ',' ',' ',' ',' '],['p','p','p','p','p','p','p','p','p'], [' ','r',' ',' ',' ',' ',' ','b',' '],['l','n','s','g','k','g','s','n','l']
        y = 2
        x = 2 #bishop white
        #print('yx:',y,x,'  ',B[9-y][9-x],'board:',9-y,' ',9-x,' Notation: bishop 72= 7b board 77,  File: 7(bishop, white)')
        # x: file   y: line B(line,file)
        y = 3
        x = 2 #pawn white
        #print('yx:',y,x,'  ',B[9-y][9-x],'board:',9-y,' ',9-x,' Notation: Pawn 73= 7c, board 76 File: 7(pawn, white)')
        # x: file   y: line B(line,file)
        y = 9
        x = 2  #Knight black
        #print('yx:',y,x,'  ',B[9-y][9-x],'board:',9-y,' ',9-x,' Notiation: Knight 29= 2i, board 07 File: 2(Knight, black)')
        y = 8
        x = 2  #Rook black
        #print('yx:',y,x,'  ',B[9-y][9-x],'board:',9-y,' ',9-x,' Notiation: Rook 28= 2g, board 17 File: 2(rook, black)')
        #print('Representation: B(File,Line) = B(y,x), B(a,b), Jap 91..11  Euro. 1a..9a  Koord: 08..88')
        #print('                                                99  19        1i..9i         00..08')
        #print('fieldat: File,Line Nr,Kanji')
        #  9 8 7 6 5 4 3 2 1 :         1 x
        #  l n s g k g s n l : a : 1 - 8 v
        #....
        #..  B           R         8
        #  L N S G K G S N L : h : 9 - 0
        # <-
        # y
        #-------------------Routines
        # 
        # Made for Files written by Shogikodoro and most Kifu programs, File in line[5], 0..4 movenr, 
        # Insert provisions for white and black triangles when convenient
        # 4.5. Position and Captures/drops o.k., quirks removed by switching xy in move-output and writing of occ-list. Would have to
        # rewrite whole program to fix logic- provided as is.
        # left and right depend on player!
        # will read Kifu with multiple variants, still has a problem in heavily bracketed variants --- find it!
        # reads modern kifu with startfield in brackets automatically even from 81-Dojo
        # 9.5.17 B.Wille
        # reads 81-Dojo Files with slightly modified form 23.5.18 b.wille
        # tbd: check moves in modern form with "move" routine
        
        
        root.minsize(400,250)
        root.maxsize(1400,850)
        #root.geometry(200,150)
        self.datafile = ""
        self.myList = []   
        self.outList = []
        self.recentfile = ""
        self.meldung = StringVar()
        self.holen = StringVar()
        self.times = IntVar()
        self.times.set = 1
        self.meldung.set( "    ")
        self.title="Kifu to Psn"
        self.v = IntVar()
        self.v.set(1)    
        decodings = [("UTF-8",1),("shift-jin (Japanese)",2)]        
        self.label=Label(master,text="""Decoding:""",justify = LEFT)
        for txt, val in decodings:
            self.radiobutton= Radiobutton(master,text=txt,padx = 20,variable=self.v, value=val)       #command=ShowChoice, 
            self.radiobutton.grid(column=1,row = 7+val, sticky = W) #,padx =20)

        self.button = Button(master, text="QUIT",command=master.quit)
        self.messageErgebnis = Message(master,relief=SUNKEN, fg="red",width= 250, text="Translation of Kifu files (Shogi)")
        self.messageMeldung = Message(master, relief=SUNKEN, textvariable=self.meldung,  text="                 ", fg ="red",  width=250)
        self.messageMeldung.grid(column=1,  row=3,  sticky = E,  padx= 5)
        self.messageErgebnis.grid(column=1,  row =0)
        self.button.grid(column=5,  row=10,  padx=20,  pady = 5)
        self.label.grid(column = 1, row = 5, sticky = W)
        
                 #Menu       
        self.menubar = Menu(root)
        self.helpmenu = Menu(self.menubar,  tearoff=1)
        self.helpmenu.add_command(labe='Info',  command=self.box)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open" ,command=self.neueinlesen)
        self.filemenu.add_command(label="Save As", command=self.ausgeben)
        self.filemenu.add_command(label="Retranslate", command=self.neuberechnen)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Quit!", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        root.config(menu=self.menubar)   
        self.checkmenu()


    def neueinlesen(self):
        self.einlesen(False)

    def neuberechnen(self):
        self.einlesen(True)

    def checkmenu(self):
            if  self.outList==[]:  #self.filemenu.entrycget(1,"state")=="normal" and
                self.filemenu.entryconfig(1,state=DISABLED)
                self.filemenu.entryconfig(1,label="-----")

            else:
                self.filemenu.entryconfig(1,state=NORMAL)
                self.filemenu.entryconfig(1,label="Save As")

            if self.datafile == "":
                self.filemenu.entryconfig(2, state=DISABLED)
                self.filemenu.entryconfig(2, label="-------")
            else:
                self.filemenu.entryconfig(2, state=NORMAL)
                self.filemenu.entryconfig(2, label="Retranslate")
            
    def box(self):
                messagebox.showinfo("Kifu-Translator V 1.1", "Translates Kifu (even multivariant) in PSN for Gshogi \n Bernd Wille May 2018,\n routines for ancient files do not work (yet).", icon='info')
                
    def capture(self,piece, movenr, drop, fieldat, b1,a1, board, captured, instr):
        #piece  is uppercase
        comment = ''
        mv ='-'
        z = (((int(movenr)-1)/2) - int((int(movenr)-1)/2))*2-1 # uneven: -1, even: 0
        if z ==  0:
            z = 1	#not really needed, for ancient format
                #lower case for white moves piece1 is to be written in board
            piece1 = piece.lower()  #black-white
        else:
            piece1 = piece
        a = fieldat[1]
        b = fieldat[0]
        y = 9-a #Board-Coordinates
        x = 9-b
        y1 = 9-b1 #Board-Coordinates, hier rotiert! analog move-Routine
        x1 = 9-a1        
        #print(x, '  ',y)
            # captured piece swaps color - 1st char only
        if board[y][x] != ' ':
            if len(board[y][x])>1:
                piecec = board[y][x][1].swapcase()
            else:
                piecec = board[y][x].swapcase()
            captured.append(piecec)   #different color after capture!
            mv ='x'
        #startfield
        #Promote 
        if '成' in instr:  # 'Promote' in inst:
            if piece != 'G' and piece != 'K':
                piece1 = '+'+piece  
        board[y][x]=piece1
        if drop == '*':
            x1 = -1
            y1 = -1 
            mv = ''
            
            if piece1 in captured:
                captured.remove(piece1)          
            else:
                #print('wrong Drop in move ' ,movenr, ' :',piece)
                comment = ' {wrong Drop in move ' + str(movenr) + ' :'+piece + '}' 
        else:
            board[int(y1)][int(x1)] = ' ' 
        #print(y1,'  ',str(instr))
        #a = 9-int(x1)      #Kifu-Coordinates ###3.5.17 provisionally rotated!!!!!!!!!!!!!!!!!!1
        #b = 9-int(y1)
        
        return mv, board, captured
    
    def move(self,piece, movenr, drop, fieldat, board, captured, instr):
        #not sufficiently tested: this is for traditional synthax in kifu notation
        comment = ''
        mv ='-'
        z = (((int(movenr)-1)/2) - int((int(movenr)-1)/2))*2-1 # uneven: -1, even: 0
        if z ==  0:
            z = 1
            piece1 = piece.lower()  #black-white
        else:
            piece1 = piece
        a = fieldat[1]
        b = fieldat[0]
        y = 9-a ##Board-Coordinates
        x = 9-b
        #print(x, '  ',y)
        if board[y][x] != ' ':
            if len(board[y][x])>1:
                piecec = board[y][x][1].swapcase()
            else:
                piecec = board[y][x].swapcase()
            captured.append(piecec)   #different color after capture!
            mv ='x'
    
        possfields = self.fieldsfrom(piece, movenr, fieldat)
        occ = []
        if drop == '' :
            for a in range(9):
                for b in range(9):
                    #print('o ',board[a][b])
                    if board[b][a] == piece1:
                        occ.append([int(a),int(b)])    #rotated 
        #print(board[3][4])
        #print(board[4][3])
        if '成' in instr:
            piece1 = '+' + piece1
            instr.remove('成')
        board[y][x] = piece1
        #print(y,x,'s')
        if '不' in instr:
            instr.remove('不')
            instr.remove(    '成')
        if drop == '*':
            x1 = -1
            y1 = -1 
            mv = ''
            
            if piece1 in captured:
                captured.remove(piece1)          
            else:
                #print('wrong Drop in move ' ,movenr, ' :',piece)
                comment = ' {wrong Drop in move ' + str(movenr) + ' :'+piece + '}'
    
    
        #see if there is a piece to be moved
        deletions = []
        for p in possfields:  #Error: deleting in the same cycle would have side-effects
            #print(p)
            if p not in occ:
                deletions.append(p)  
                #print(p,'r')
        for p in deletions:
            possfields.remove(p)
    
        if len(possfields) == 0 and drop !='*':
            comment = ' {Assumed drop}'
            x1 = -1
            y1 = -1
            mv = ''
            drop = '*'
        #print(len(possfields))
        if len(possfields) == 1:
            x1 = possfields[0][0]
            y1 = possfields[0][1]
            board[int(y1)][int(x1)] = ' '  
            #print(y1,x1,'r')                
        else:
            x1 = -1
            y1 = -1        
    
            #special commands
            if len(instr) > 1:
                comment = ' {Don\'t know how to do that!}'
            else:
                for s in instr:   # x,y rotated
                    if self.T[s] == 'Upright':  #p[0]  File, x
                        rem = []
                        for p in possfields:
                            if p[0] != x:
                                rem.append(p)
                        for p in rem:
                            possfields.remove(p)
                    if self.T[s] == 'Forward':
                        rem = []
                        for p in possfields:
                            if p[1] <= y:
                                rem.append(p)
                        for p in rem:
                            possfields.remove(p)  
                    if self.T[s] == 'Sideward':
                        rem = []
                        for p in possfields:
                            if p[1] != y:
                                rem.append(p)
                        for p in rem:
                            possfields.remove(p)  
                    if self.T[s] == 'Backward':
                        rem = []
                        for p in possfields:
                            if p[1] >= y:
                                rem.append(p)
                        for p in rem:
                            possfields.remove(p)                      
                    if self.T[s] == 'Left':            #p[0] is File, x
                        if z == -1:                 #depends on black/white
                            rem = []
                            pmax = possfields[0]
                            for p in possfields:
                                if p[0] < pmax[0]: 
                                    pmax = p
                            possfields =[pmax]
                        if z == 1:
                            rem = []
                            pmax = possfields[0]
                            for p in possfields:
                                if p[0] > pmax[0]: 
                                    pmax = p
                            possfields =[pmax]                    
                    if self.T[s] == 'Right':
                        if z == -1:
                            rem = []
                            pmax = possfields[0]
                            for p in possfields:
                                if p[0] > pmax[0]:
                                    pmax = p
                            possfields =[pmax]  
                        if z == 1:
                            rem = []
                            pmax = possfields[0]
                            for p in possfields:
                                if p[0] < pmax[0]:
                                    pmax = p
                            possfields =[pmax]                          
                if len(possfields) == 1:
                    x1 = possfields[0][0]
                    y1 = possfields[0][1]
                    board[int(y1)][int(x1)] = ' '              
                else:
                    if len(possfields)>0:
                        comment = ' {Don\'t know how to do that}'
       
        #Promote 
        if '成' in instr:  # 'Promote' in inst:
            if piece != 'G' and piece != 'K':
                piece1 = '+'+piece  
        #print(y1,'  ',str(instr))
        a = 9-int(x1)      #Kifu-Coordinates ###3.5.17 provisionally rotated!!!!!!!!!!!!!!!!!!1
        b = 9-int(y1)
        #comment = comment + str(captured)
        return a,b, mv, comment, drop, board, captured
    
    def fieldsfrom(self,piece, movenr, fieldat):
        possfields = []
        z = (((int(movenr)-1)/2) - int((int(movenr)-1)/2))*2-1 
        if z == 0:
            z = 1
        a = fieldat[1]
        b = fieldat[0]
        x = 9-a  #Board-coordinates
        y = 9-b
        #[File,Line]
        if piece == 'P':
            possfields.append([y ,x + z])
        if piece == 'N':
            possfields.append([y + 1,x + z*2])
            possfields.append([y - 1,x + z*2])
        if piece == 'L':
            if z == -1:
                for i in range(0 ,x-1):
                    possfields.append([y,i])
            else:
                for i in range(8, x+1):
                    possfields.append([y,i])
        if piece == 'S':
            possfields.append([y , x + z])
            possfields.append([y - 1, x - z])
            possfields.append([y + 1, x + z])
            possfields.append([y + 1, x - z])
            possfields.append([y - 1, x + z])
        if piece == 'G' or piece == 'L+' or piece == '+N' or piece == '+S' or piece =='+P':
            possfields.append([y , x - z])
            possfields.append([y + 1, x + z])
            possfields.append([y - 1, x + z]) 
            possfields.append([y , x + z])
            possfields.append([y + 1, x])
            possfields.append([y - 1, x])             
        if piece == 'K':
            possfields.append([y , x - 1])
            possfields.append([y , x + 1])
            possfields.append([y + 1, x + 1])
            possfields.append([y - 1, x + 1])  
            possfields.append([y + 1, x])
            possfields.append([y - 1, x])  
            possfields.append([y + 1, x - 1])
            possfields.append([y - 1, x - 1])
        if piece == 'B':
            for i in range(9):
                possfields.append([i,x-y+i]) #gedreht
            for i in range(9):
                possfields.append([i,y+x-i])  
    
        if piece == 'R':
            for i in range(9):
                possfields.append([i,x])
            for i in range(9):
                possfields.append([y,i])  
        if piece == '+B':
            for i in range(9):
                possfields.append([x-y+i,i])
            for i in range(9):
                possfields.append([i,y+x-i]) 
            possfields.append([y , x - 1])
            possfields.append([y , x + 1])
            possfields.append([y + 1, x])
            possfields.append([y - 1, x])  
        if piece == '+R':
            for i in range(9):
                possfields.append([i,x])
            for i in range(9):
                possfields.append([y,i])     
            possfields.append([y +1, x +1])
            possfields.append([y -1, x -1])
            possfields.append([y -1, x +1])
            possfields.append([y +1, x -1])                
        #Cleanup
        for t in possfields:
            if t[0] > 8 or t[0] < 0:
                possfields.remove(t)
                if t[1] > 8 or t[1] < 0:
                    #print(t, '\n')
                    possfields.remove(t)  
            if t == [y,x]:
                    possfields.remove(t)
        return possfields
    
    
    def einlesen(self, reprocess):
        Sel = 0
        erl = False
        self.outList = []
        short = False
        self.checkmenu()
        if reprocess == False:
            hole = filedialog.askopenfilename(title = "Ausgangsfile", defaultextension = 'kif')
            self.datafile = hole
        else:
            hole = self.datafile

        if self.v.get()==2:
                f = open(hole,"r", encoding="shift-jis")
        else:
                f = open(hole,"r")
        self.meldung.set("translated:  \n" + hole )
        try:
        #if 1:
            board = deepcopy(self.B)
            Ende = False
            captured = deepcopy([])
            out = []
            BO = deepcopy({})
            blist = {}
            branch = 0
            #branches = {0:[]}
            lastmove = 0
            #branchlist = [0]
            lastfield = [0,0]
            lset = 0
            goteset = 0
            senteset = 0
            timeset = 0
            locset = 0
            same = 0
            for line in f :
                #e = line[0]
                if line[0] != ' ' and line[0] not in ('1','2','3','4','5','6','7','8','9'):
                    #print(line[0:3])
                    if line.find('開始日時',0,6) != -1:
                        if timeset == 0:
                            Time = line[5:]
                            out.append('[Time: '+Time[:-1]+']')
                            timeset = 1
                        else:
                            if len(line[2:-1]) > 2:
                                out.append(' {'+ line[2:-1] + '}')                        
                    if line.find('場所',0,5) != -1:
                        if locset == 0:
                            Location = line[3:]
                            out.append('[Location: '+Location[:-1]+ ']')
                            locset = 1
                        else:
                            if len(line[2:-1]) > 2:
                                out.append(' {'+ line[2:-1] + '}')                           
                    if line.find('先手',0,5) != -1:
                        if senteset == 0:
                            Sente = line[3:]
                            if len(Sente) <2:
                                Sente = '??'
                            out.append('[Sente: '+ Sente[:-1]+ ']')
                            senteset = 1
                        else:
                            if len(line[2:-1]) > 2:
                                out.append(' {'+ line[2:-1] + '}')                           
                    if line.find('後手',0,3) != -1:
                        if goteset == 0:
                            Gote = line[3:]
                            if len(Gote) < 2:
                                Gote = '??'                    
                            out.append('[Gote: '+ Gote[:-1]+ ']')
                            goteset = 1
                        else:
                            if len(line[2:-1]) > 2:
                                out.append(' {'+ line[2:-1] + '}')                           
                    if line.find('*',0,5) != -1:
                        if len(line[:-1]) > 2:
                            out.append(' {'+ line[:-1] + '}')
    
                elif  line.find('投了') != -1:
                    stim = ""
                    if  line[3]  in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        tim = int(line[0:4])
                        stim = str(tim)+ ".   "
                    out.append(stim + '\n{' + line[0:5] + "Resign }")
                elif  line.find('待将棋') != -1:
                    stim = ""
                    if line[3] in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        tim = int(line[0:4])
                        stim = str(tim) + ".   "
                    out.append(stim +'\n{' + line[0:5] + "Draw }")
                elif  line.find('千日手') != -1:
                    stim = ""
                    if line[3] in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        tim = int(line[0:4]);
                        stim = str(tim) + ".   "
                    out.append(stim + '\n{' + line[0:5] + "Repetition }")
                else:
                    movenr = int(line[0:4])
                    #if movenr == 22:##Debug to stop at given move
                        #i = i                       
                    #branchnew = 0
                    ##########saves Board and creates new branch
                    #if movenr != lastmove+1: #new Branch
                    #if movenr == 26 and lastmove == 37:
                            #xx = 0                       
    
    #  we are in old branch and note state for start of new one
    #which is o.k. if we are in a variant. Otherwise there is still the move from the old branch!! so we have to get the relevant data first!!                    
                    if movenr != lastmove+1: # now switch to new Branch      
                        branch = movenr
                        #search for Board
                        li = []
                        for p in blist:
                            if blist[p][1]==True:
                                if blist[p][0]==movenr:
                                    li.append(p)
                        if len(li)<1:
                            raise ValueError('Read-error in Branches')
                            
                        else:
                            p=li.pop()
                            blist[p][1]= False
    
                        if  BO.get(p,None)==None:
                            raise ValueError('Error at ',p,' ',str(li))
                        board = deepcopy(BO[p][0])
                        captured = deepcopy(BO[p][1])
                        lastfield = BO[p][2] 
                        ##########enter a check here for number of pieces
                        
                        out.append('\n[Branch, starting at move '+str(movenr) +' from move '+str(p)+' ]') #O[str(p)+'/'+str(movenr)]')
                        #if movenr == 22:  #Debug
                            #i = i
                        cap1 = []
                        npieces = 0
                        last = ''
                        z = 0
                        captured.sort()
                        for  c in captured:
                            npieces += 1
                            if c == last:
                                z = z + 1
                            else:
                                if z != 0:
                                    c1 = cap1.pop()
                                    cap1.append(str(z+1)+c1)  #Änderung: +1
                                    z = 0
                                cap1.append(c)
                                last = c
                        last = ''
                        if z!= 0:
                            c1 = cap1.pop()
                            cap1.append(str(z + 1) + c1)
                        for c in cap1:
                            last = last + c
                        boardpos = ''
                        for a in [8,7,6,5,4,3,2,1,0]:
                            z = 0
                            for b in range(9):
                                if board[a][b]==' ': 
                                    z = z + 1
                                else:
                                    if z != 0:
                                        boardpos = boardpos + str(z)
                                        z = 0
                                    boardpos = boardpos + board[a][b]
                            if z != 0:
                                boardpos = boardpos + str(z) 
                            boardpos = boardpos +'/'
                        boardpos = boardpos[:-1]
                        n = 0
                        for cc in boardpos:
                            if cc not in ['1', '2','3','4','5','6','7','8','9','/','+']:
                                n += 1
                        if movenr/2 -int(movenr/2)>0:
                            c = 'b'
                        else:
                            c = 'w'
                        # put - in empty list of captured pieces
                        if last =="":
                            last = "-"
                        boardpos = boardpos  + ' ' + c +' ' + last+ ' ' + str(movenr)
                    
                    
                        out.append('[SFEN  \"'+ boardpos + '\"]')
                        if npieces + n != 40:
                            raise ValueError('error ',npieces + n,' pieces: ', p, 'captured = ', n, ' on board = ', npieces,\
                                             ' move: ', movenr)
                        #else:
                         #   print( p, ' ok')
                        ###################puts in new Branch                 
                    #now note data for new branch
    
                    if line.find(')+') != -1: 
                            out.append('{Branch at Move ' + str(movenr) + ' from move '+ str(branch) +'}')
                            blist[str(branch)+'/'+str(movenr)]= [movenr,True]
                            #Deepcopy to avoid side effects!!!!!!!!!!!!11
                            BO[str(branch)+'/'+str(movenr)] = [deepcopy(board),deepcopy(captured), lastfield]  #Board before move
                            #for debugging
                            #self.sfen(BO[str(branch)+'/'+str(movenr)][0],str(branch)+'/'+str(movenr))
                            #print(str(branch)+'/'+str(movenr))                    
    
     
      
                    lastmove = movenr
                    #print(movenr)
                    #if movenr >29:
                        #print(BO['0/28'][1])
                    prom = ''
                    sh = 0
                    if movenr == 10:
                        sh2 = sh2 +1
                        if line[6+sh2] not in self.F.keys():
                            sh2 = sh2 - 1
                    if movenr == 100:
                        if sh2 != 0:
                            sh2 = sh2 +1
                            if line[6+sh2] not in F.keys():
                                sh2 = sh2 - 1                            
                    if movenr == 1:
                        sh2 = 0
                        #and line[8]=='(' and line[11]==')': special case!!!
                        klam = line.find("(")
                        mer = line.find(")")
                        if mer-klam ==3 and (line[mer+1]==" " or line[mer+1]=="\n") :
                            short = True
                            sh2 = klam-8
                            sh3 = mer-11
                            if sh2 != sh3:
                                v=self.meldung.get()
                                self.meldung.set(v + "\n" + "Can't read format!!")
                    #if movenr == 37:
                        #xx = 0 #to stop in line                    
                    if (line[5+sh2]) in self.T:
                        if self.T[line[5+sh2]] == "Same":
                            fieldat = lastfield
                            if line.find('成')!= -1:
                                if line.find('成') == 7+sh2:
                                    piece = self.P[line[8+sh2]]
                                    piece = '+'+ piece 
                                    sh = 1
                                else: #Promotion
                                    if line.find('不') == -1:
                                        prom = '+'
                                        piece = self.P[line[7+sh2]]
                                    else:
                                        piece = self.P[line[7+sh2]]
                                        sh = 2
                            else:
                                piece = self.P[line[7+sh2]] 
                        else:
                            out.append(' {' + line[5+sh2:] + self.T[line[5+sh2]] +'}')
                            #print('[' + line[5:] + self.T[line[5]] +']')
                            Ende = True                
                    else:
                        try:
                                if movenr == 9:##Debug to stop at given move
                                    i = i                             
                                fieldat = [int(line[5+sh2]),int(self.F[line[6+sh2]])]  #Read normal line
                                lastfield = fieldat
                                if line.find('成')!= -1:
                                    if line.find('成') == 7+sh2:
                                        piece = self.P[line[8+sh2]]
                                        piece = '+'+ piece 
                                        sh = 1
                                    else: #Promotion
                                        if line.find('不') == -1:
                                            prom = '+'
                                            piece = self.P[line[7+sh2]]
                                        else:
                                            piece = self.P[line[7+sh2]]
                                            sh = 2
                                else:
                                    piece = self.P[line[7+sh2]] 
                        except:
                                out.append(' {'+ line[5+sh2:-1] +'}')
                                Ende = True
                            
                    instr =[]
                    #read prom etc.
                    if Ende == False:  #23.5.18
                        for i in ( 8+sh2,len(line)-1):
                            w = line[i]
                            if line[i] in self.T:
                                instr.append(line[i])
                        if '打' in instr:   #Drop
                            drop = '*'
                            instr.remove('打')
                        else:
                            drop =''  
                        if ('不' not in instr) and ('成' in instr):
                            prom = '+'
                            instr.remove('成')
                        
                        else :
                            prom = ''
                        comment = ''
                       
                    #print(line)  #成銀
                    if Ende == False:
                        if short:       #westl. Ausgangsfeld
                            if drop != '*' and prom != '+':
                                y1 = int(line[9 +sh+sh2])
                                x1 = int(line[10+sh+sh2])
                            else:
                                y1 = 10
                                x1 = 10
                            if prom == '+':
                                y1 = int(line[10+sh+sh2])
                                x1 = int(line[11+sh+sh2])                            

                         
                            mv, board, captured = self.capture(piece, movenr, drop, fieldat, x1,y1, board[:], captured[:], instr)
                        #Direct detection of moves for older format
                        else:
                            y1,x1, mv, comment, drop, board, captured = self.move(piece, movenr, drop, fieldat, board[:], captured[:], instr)
                    
                    
                    
                    if len(instr) > 0:
                        ist = ' {'+str(instr)
                        for p in instr:
                            ist = ist + ' ' + self.T[p]
                        if len(instr)>0:
                            ist = ist + '}'
                    else:
                        ist = ''
                    if Ende == False:
                        if y1 == 10:
                            ys =''
                        else:
                            ys = str(y1)
                        if x1 == 10:
                            xs=''
                        else:
                            xs = self.G[x1]
                        if drop =='*':
                            mv = ''
                            
                        outline = str(movenr)+ '. '+piece + drop + ys + xs + mv +str(fieldat[0])+self.G[fieldat[1]]+ prom +  ist + comment
                        out.append( outline)
                        #for debugging
                        #print(outline)
                    Ende = False
            
            #for p in BO:
              #  self.sfen(BO[p][0],p)
            lastl = 0
            for  line in out:
                at = -1
                if line.find('{')!= -1 and lastl == 1:
                    at = line.find('{')
                    line1 = self.outList.pop()
                    ate = line1.find('}')
                    self.outList.append(line1[:ate])
                    lastl = 0
                if line.find('}')!= -1:
                    lastl = 1
                else:
                    lastl = 0
                self.outList.append(line[at+1:])
            erl = True
        except BaseException as e:
            if e != '':
                self.meldung.set(hole +'  Error: '+ str(e))            
            else:
                self.meldung.set(hole +'  Error!')
            
        finally:
            pass
        if erl == False:
                lastl = 0
                for  line in out:
                    at = -1
                    if line.find('{')!= -1 and lastl == 1:
                        at = line.find('{')
                        line1 = self.outList.pop()
                        ate = line1.find('}')
                        self.outList.append(line1[:ate])
                        lastl = 0
                    if line.find('}')!= -1:
                        lastl = 1
                    else:
                        lastl = 0
                    self.outList.append(line[at+1:])                

            #print(str(branches))
        self.checkmenu()
            
        def sfen(self, board, label):
            boardpos = ''
            for a in [8,7,6,5,4,3,2,1,0]:
                z = 0
                for b in range(9):
                    if board[a][b]==' ': 
                        z = z + 1
                    else:
                        if z != 0:
                            boardpos = boardpos + str(z)
                            z = 0
                        boardpos = boardpos + board[a][b]
                if z != 0:
                   boardpos = boardpos + str(z) 
                boardpos = boardpos +'/'
     
            print(label+' '+'[SFEN  \"'+ boardpos + '\"]') 
        
        return
    

    def ausgeben(self):
        #if self.recentfile == "":
        f=filedialog.asksaveasfilename(title = "Save", defaultextension = 'psn')

        file = open(f, "w") # Sicherheitsabfrage!!

        #liste=self.myList.get(0, END)
        
        for line in self.outList:
            file.write(line+"\n")
            
          
        file.close()
        self.outList=[]
        self.checkmenu()
     


        self.meldung.set("saved " + f ) # + "Typ" )#+ self.warn)







if __name__ == '__main__':
    root = Tk()
    root.wm_title("Kifu to psn")
    app = App(root)
    root.mainloop()




