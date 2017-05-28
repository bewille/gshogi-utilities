#!/usr/bin/python3



from tkinter import  *
from tkinter import filedialog
from tkinter import messagebox
import array


import sys
import time

class App:


    def __init__(self, master):
        self.myList = []   
        self.outList = []
        self.recentfile = ""
        self.meldung = StringVar()
        self.holen = StringVar()
        self.times = IntVar()
        self.times.set = 1
        self.meldung.set( "    ")
        self.title="Psn to Psn"
        self.button = Button(master, text="QUIT",command=master.quit)
        self.messageErgebnis = Message(master,relief=SUNKEN, fg="red",width= 250, text="Übersetzung von USL-Dateien (Shogi)")
        self.messageMeldung = Message(master, relief=SUNKEN, textvariable=self.meldung,  text="                 ", fg ="red",  width=250)
        #self.checkButton = Checkbutton(master, relief=SUNKEN,  variable= self.times,  text="Datei mit Zeiten").grid(column=1,  row= 4)
        self.messageMeldung.grid(column=1,  row=3,  sticky = E,  padx= 5)
        self.messageErgebnis.grid(column=1,  row =0)
        self.button.grid(column=5,  row=5,  padx=5,  pady = 5)
                 #Menu       
        self.menubar = Menu(root)
        self.helpmenu = Menu(self.menubar,  tearoff=1)
        self.helpmenu.add_command(labe='Info',  command=self.box)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open" ,command=self.einlesen)
        self.filemenu.add_command(label="Save", command=self.ausgeben)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Quit!", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        root.config(menu=self.menubar)   
        self.checkmenu()
   
    def checkmenu(self):
            if  self.outList==[]:  #self.filemenu.entrycget(1,"state")=="normal" and
                self.filemenu.entryconfig(1,state=DISABLED)
                self.filemenu.entryconfig(1,label="-----")
            else:
                self.filemenu.entryconfig(1,state=NORMAL)
                self.filemenu.entryconfig(1,label="Save")   
    def box(self):
                messagebox.showinfo("USL-Translator V0.9", "Translates BCM-Games files (UCL) into PSN bw April 2017", icon='info')

    def board_aufstellen(self):
        # Brett
        startpos = "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL"
        startstate ="b - 1 moves"
        w = 9
        h = 9
        board = [['' for x in range(w)] for y in range(h)] 
        # Routine, die ausgehend von usi-Stellungsformat ein Brett aufbaut
        j = 0 #Index Zeilen
        f = 1 #Leseindex
        i = 1 #Index Spalten
        while j in range(0,9):
            m = 1
            n = startpos[f-1]
            while i in range(1,10):
                if startpos[f-1] in ['1','2','3','4','5','6','7','8','9']:
                    for k in range(1,int(startpos[f-1])+1):  #k-fache Leerstelle
               #         print(i +k -2," ",j, "\n")
                        #print(i,"  ",k,"  ",j,"  ",startpos[f-1],"\n")
                        # print(board)
                        board[i + k -2][j] = ''
                        l = int(startpos[f-1])
                #        print(l)
                        m = k
                    i = i + m  
                    f = f + 1
                else:
                    board[i-1][j] = startpos[f-1]
             #       print(board[i-1][j])
              #      print(startpos[f-1])
                    i = i + 1
                    f = f + 1
            #print(i,"  ",j,"  ","\n")
            #print(">>",board)            
            j = j + 1
            i = 1
            f = f + 1 # Überspringen \
            #print(board)
            #print("Bishop: ",board[1][7]) #row/file  gibt schwarzen Bishop, korrekt row ist Spalte, file ist Zeile
        # Koordinatenumrechnung
        #r = 5
        #fi = 3
        #print("Test p: ",board[9-r][fi-1],"  In:",r,"/",fi," Out:",9-r,"/",fi-1)
        #fi = 9
        #print("Test k: ",board[9-r][fi-1],"  In:",r,"/",fi," Out:",9-r,"/",fi-1        )
        return board
    
    def einlesen(self):
        Sel = 0
        self.checkmenu()
        hole = filedialog.askopenfilename(title = "File to translate", defaultextension = 'usl')
        f = open(hole,"r")
        self.meldung.set("new:  " + hole )
        line = ""
        self.outList=[]
        self.myList=[]
        last = 0
        lastwasheader = 0
        self.warn = ""
        line2 = ""
        fd = False
        item1=""
        line2 = ""
        for line in f:
            #a = line[0:2]
            if line[0:2]=="^*":
                self.myList.append(line[3:])
            if line[0:4]==" Src":
                self.myList.append(line)
        f.close()
        board = self.board_aufstellen()
        
        #Einlesen
        trans = ['a','b','c','d','e','f','g','h','i']
        trans2 = ['A','B','C','D','E','F','G','H','I']
        rowto_c = "  " #muss als String definiert werden wegen Promotion
        piece_moved = "  "
        piece = "  "
        for line in self.myList:
            index1 = self.myList.index(line)
            last2 = 0
            last = len(self.outList)
            n = 0
            outline = ""
            while len(line) > 1 and line[0]!='' and line[0]!=' ':
                n = n + 1
                drop = 0
                prom = 1
                row = 10
                if line[1] == "*":
                    file = 0
                    row = line[0].upper()
                    drop = 1
                    file_c = "*"
                else:
                    row = int(line[0])
                    for ind in range(0,9):
                        if trans[ind] == line[1]:
                            file = ind
                                              
                file_c = line[1]
                # Piece-Lookup
                if drop == 0:
                    #print(">",file)
                    piece = board[9-row][file].upper()
                    piece_moved = board[9-row][file]
                    #Board
                    board[9-row][file] = ""
                    #print("In: ",row,"/",file," Out:",9-row,"/",file, "moved: ",piece_moved)
                else:
                    piece = ""
                    piece_moved = row
                # 1.Koordinate
                line = line[2:]
                rowto = int(line[0])
                fileto =  10
                for ind in range(0,9):
                    if trans[ind] == line[1]:
                        fileto = ind
                        prom = 0
                    if prom == 1:
                        for ind in range(0,9):
                            if trans2[ind] == line[1]:
                                fileto = ind                         
                fileto_c = line[1]
                if prom == 1:
                    fileto_c = fileto_c.lower() + "+" 
                    piece_moved = "+" + piece_moved 
                #Board
                piece_killed = board[9-rowto][fileto]
                #print(9-rowto," ",fileto, "piece ", piece_moved)
                board[9-rowto][fileto] = piece_moved
                #print("In: ",rowto,"/",fileto," Out:",9-rowto,"/",fileto, "moved: ",piece_moved," before: ",piece_killed)
                line = line[2:]      
                #2. Koordinate, 1. Halbzug
                #print(line,"  nach 1. Halbzug")
                outline = str(n) + "." + piece + str(row) + file_c  + str(rowto) + fileto_c
                #print(outline, "  1.Halbzug")
                if len(line) > 2:
                    #self.outList.append(outline)
                    #print("Rest:",line, len(line))
                #else:
                    row = 10
                    drop = 0
                    prom = 1
                    if line[1] == "*":
                        file = 0
                        drop = 1
                        row = line[0].upper()
                        file_c = "*"
                    else:
                        row = int(line[0])
                        for ind in range(0,9):
                            if trans[ind] == line[1]:
                                file = ind
                        file_c = line[1]
                    if drop == 0:
                        #print(">",file)
                        piece = board[9-row][file].upper()
                        piece_moved = board[9-row][file]
                        #print("2. Zug In: ",row,"/",file," Out:",9-row,"/",file, "moved: ",piece_moved)
                        #Board
                        board[9-row][file] = ""
                    else:
                        piece = ""
                        piece_moved = row                     
                    line = line[2:]
                    rowto = int(line[0])
                    fileto =  10
                    for ind in range(0,9):
                        if trans[ind] == line[1]:
                            fileto = ind
                            prom = 0
                        if prom == 1:
                            for ind in range(0,9):
                                if trans2[ind] == line[1]:
                                    fileto = ind                             
                    fileto_c = line[1]
                    if prom == 1:
                        fileto_c = fileto_c.lower() + "+" 
                        piece_moved = "+" + piece_moved 
                    #Board
                    board[9-rowto][fileto] = piece_moved
                    #print("2. Zug In: ",rowto,"/",fileto," Out:",9-rowto,"/",fileto, "moved: ",piece_moved," before: ",piece_killed)
                    line = line[2:]         
                    self.outList.append(outline + " " + piece + str(row) + file_c + str(rowto) + fileto_c)
                    print(outline +" " + piece + str(row) + file_c + str(rowto) + fileto_c)
                    
                #Ende 1. move
            if line.find("Src") == -1:
                self.outList.append("{End}")
                print("{End}")
            line = "[Event "+ self.myList.pop(index1 + 1)+ "]"
            if line.find("Src") != -1:
                self.outList.insert(last,line)
            board = self.board_aufstellen()
        self.myList = []
        self.checkmenu()

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
     


        self.meldung.set("gepeichert" + f  + "Typ" + self.warn)







if __name__ == '__main__':
    root = Tk()
    root.wm_title("usi to psn ")
    app = App(root)
    root.mainloop()




