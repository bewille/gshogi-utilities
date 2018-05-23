#!/usr/bin/python3



from tkinter import  *
from tkinter import filedialog
from tkinter import messagebox
import array


import sys
import time


class Moveerror(KeyError):
    def __init__(self, arg):
        self.args = arg
        
class App:


    def __init__(self, master):
        self.myList = []   
        self.outList = []
        self.board=[["" for i in range(1,11)] for j in range(1,11)]
        ##for some reason this initializes an 0..9,0..9-array...
        self.recentfile = ""
        self.meldung = StringVar()
        self.holen = StringVar()
        self.times = IntVar()
        self.times.set = 1
        self.meldung.set( "    ")
        self.title="ShogiQuest Translator"
        self.button = Button(master, text="QUIT",command=master.quit)
        self.messageErgebnis = Message(master,relief=SUNKEN, fg="red",width= 250, text="Übersetzung ShogiQuest-Exporten")
        self.messageMeldung = Message(master, relief=SUNKEN, textvariable=self.meldung,  text="                 ",\
                                      fg ="red",  width=250)
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
        #self.filemenu.add_command(label="Learn" ,command=self.lernen)  #debug
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
                messagebox.showinfo("ShogiQuest-Translator V0.9", "ShogiQuest-Translator, B.Wille May  2018", icon='info')
     
    def lernen(self):
        hole = filedialog.askopenfilename(title = "Ausgangsfile", defaultextension = '*')
        self.checkmenu()
        f = open(hole,"r")
        self.meldung.set("new:  " + hole )
        line = ""
        self.outList=[]
        self.myList=[]
        self.sfenout=[]
        #self.board=[][]
        for line in f:
            self.myList.append(line)
        f.close()   
        dic = {'KY':'L','KE':'N','GI':'S','KI':'G','OU':'K','FU':'P','HI':'R','KA':'B','UM':'+B','RY':'+R','TO':'+P','NY':'+L',\
               'NK':'+N','NG':'+S','* ':''}
        dic2 = {'1':'a','2':'b','3':'c','4':'d','5':'e','6':'f','7':'g','8':'h','9':'i'}
        self.dic2r = {'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8','i':'9','0':'0'}
        dic3 = {'UM':'C','RY':'T','TO':'Q','NY':'M','NK':'O','NG':'U'}
        dic4 = {'C':'UM','T':'RY','Q':'TO','M':'NY','O':'NK','U':'NG'}
        dic5 = {'+B':'C','+R':'T','+P':'Q','+L':'M','+N':'O','+S':'U'}
        self.outList.append("[Date \"\" ]")
        self.outList.append("[Sente: "+self.myList[1][2:-1] + "]")
        self.outList.append("[Gote: "+self.myList[2][2:-1] + "]")
        ############read position into board
        sfen = []
        proglist = []
        for line in self.myList:
            liste = dic.keys()
            if len(line) == 8:
                fig = line[5:]
                fig = fig.strip('\n')
                if fig not in liste:
                    v = self.meldung.get()
                    self.meldung.set(v + "\n" + "missing:  " + fig +" "+line)
                if fig in dic.keys():
                    proglist.append(fig)
        for fig in dic.keys():
                if fig not in proglist:
                    v=self.meldung.get()
                    self.meldung.set( v+"\n"+ "es fehlt: " + fig)
        
            
            
            
    def einlesen(self):
        hole = filedialog.askopenfilename(title = "Ausgangsfile", defaultextension = '*')
        self.checkmenu()
        f = open(hole,"r")
        self.meldung.set("new:  " + hole )
        line = ""
        self.outList=[]
        self.myList=[]
        self.sfenout=[]
        #self.board=[][]
        for line in f:
            self.myList.append(line)
        f.close()   
        dic = {'KY':'L','KE':'N','GI':'S','KI':'G','OU':'K','FU':'P','HI':'R','KA':'B','UM':'+B','RY':'+R','TO':'+P','NY':'+L',\
               'NK':'+N','NG':'+S','* ':'','*':''}
        dic2 = {'1':'a','2':'b','3':'c','4':'d','5':'e','6':'f','7':'g','8':'h','9':'i'}
        self.dic2r = {'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8','i':'9','0':'0'}
        dic3 = {'UM':'C','RY':'T','TO':'Q','NY':'M','NK':'O','NG':'U'}
        dic4 = {'C':'UM','T':'RY','Q':'TO','M':'NY','O':'NK','U':'NG'}
        self.dic5 = {'+B':'C','+R':'T','+P':'Q','+L':'M','+N':'O','+S':'U'}
        self.outList.append("[Date \"\" ]")
        i = 1
        while self.myList[i][:2].find("N+") == -1: 
            i = i +1
            if i == 5:
                self.outList.append("[Sente: \" \"]")
                self.outList.append("[Gote: \"\"]")   
                break   
        if i <5 :
            self.outList.append("[Sente: "+self.myList[i][2:-1] + "]")
            self.outList.append("[Gote: "+self.myList[i+1][2:-1] + "]")
           
            
        ############read position into board
        sfen = []
        for line in self.myList:
            
            if line[0] == "P":
                for i in range(9,0,-1):
                    prom = 0
                    v = line[2+3*(9-i):3+3*(9-i)]
                    b = line[3+3*(9-i):5+3*(9-i)]
                    b = b.strip("\n")
                    a = dic[b]
                    if a in ['UM','RY','TO','NY','NK','NG']:
                        prom = 1
                        a = dic3(a) #Einzeichen-Code für Board  
                    l = int(line[1])
                    c = a
                    if v == "-":
                        a = a.lower()                  
                    self.board[int(line[1])][i] = a
                    if prom == 1:
                        a = c
                        a = self.dic5[a] #Code für Sfen
                    if v == "-":
                        a = a.lower()
                    sfen.append(a)
                    if i == 1:
                        sfen.append("/")
        i = 0
        self.sfenout = []
        m = 0
        while i < len(sfen):     
            if sfen[i] == "":
                m = m + 1
            elif m > 0:
                self.sfenout.append(str(m))
                m = 0
                self.sfenout.append(sfen[i])
            else:
                self.sfenout.append(sfen[i])
            i= i + 1   
        a = 0 ##DEBUG
        ###############insert treatment of captured
        cap = []
        ##############actually moves must be put to engine to verify to find promotions etc.       
        i=0
        for line in self.myList:
            if len(line) == 8:
                i = i + 1
                #s = dic[line[5:7]]
                if line[5:7] in ['UM','RY','TO','NY','NK','NG']:
                    p = "+"
                    a = dic[line[5:7]]  ###[0] Test
                else:
                    p = ""
                    a = dic[line[5:7]]           
            try:                            
                    if line[1] == "0":
                        self.outList.append(str(i)+". "+ a +"*"+line[3]+dic2[line[4]] + p)
                    else:
                        self.outList.append(str(i)+". "+ a +line[1]+dic2[line[2]]+line[3]+dic2[line[4]] + p)
            except:
                self.meldung.set("new:  " + hole +"\n"+ "Error in Move " + str(i) + " " + line +"\n" + str(sys.exc_info()[0]))
            pass
        ####################check for promotions, captures etc.
        self.outList, self.board, self.cap = self.move(self.outList,self.board, cap)
        self.checkmenu()    
    
    def move(self,List,board, cap):
        outList = []
        prom = 0
        try:
            for line in List:
                if line.find(". ")!=-1:
                    movenr = line[:line.find(".")]
                    if int(int(movenr)/2) == int(movenr)/2:
                        moveblk = False
                    else:
                        moveblk = True
                    if line.find(". ") != -1:
                        movest = line[line.find(". ")+2:]
                        movest = movest.strip("\n")
                        if movest.find("*") != -1:
                            a = movest.find("*")
                            to = movest[a+1:a+3]
                            fr = "00"
                            piece = movest[:movest.find("*")]
                            
                        else:
                            i = 0
                            while movest[i] not in ("0","1","2","3","4","5","6","7","8","9"):
                                i = i + 1
                            fr = movest[i:i+2]
                            to = movest[i+2:i+4]
                            piece = movest[:i]
                        if moveblk == False:
                            piece = piece.lower()                           
                        if movest.find("+") != -1:
                            prom = 1 
                            
                        to=to[0]+self.dic2r[to[1]]
                        fr=fr[0]+self.dic2r[fr[1]] 
                        z = board[3][1]
                        z1 = board[8][5]
                        if fr != "00":
                            mv = "-"
                            fig = ""
                            if board[int(fr[1])][int(fr[0])]!= "":
                                fig = board[int(fr[1])][int(fr[0])]
                                if fig != piece: # must be correct regardless of promotion
                                    err = "wrong piece found at from " +fr +" Mv: "+ movenr
                            else:
                                err = "missing piece in " +fr +" Mv: "+ movenr
                                raise Moveerror(err)
                            board[int(fr[1])][int(fr[0])] = ""
                            if board[int(to[1])][int(to[0])]!= "":
                                found = board[int(to[1])][int(to[0])]
                                if found in ('L','N','S','G','K','P','B','R','+B','+R','+P','+L', '+N','+S') :
                                    if moveblk == False:
                                        cap.append(found)  
                                        board[int(to[1])][int(to[0])]= piece
                                        mv="x"
                                    else:
                                        err= "captured own peace at "+to +" Mv: "+ movenr
                                        raise  Moveerror(err) 
                                else: # piece white
                                    if moveblk == False:
                                        err= "captured own peace at " +to+" Mv: "+ movenr
                                        raise  Moveerror(err)
                            #captured pieces
                                if len(found) == 2:
                                    found = found[1]
                                if moveblk == True:
                                    found = found.upper()
                                else:
                                    found = found.lower()
                                cap.append(found)  # captured piece after change of color
                                board[int(to[1])][int(to[0])]= piece 
                                mv ="x"
                            else:  # leeres Feld
                                    board[int(to[1])][int(to[0])]= piece
                            if prom == 1:
                                if fig.find("+") != -1: # promoted 
                                    if moveblk == True and piece in self.dic5.keys(): #promoted piece moved
                                        line = line[:-1] #delete +
                                        #line = line[:line.find(". ")+2] + "+" + line[line.find(". ")+2:] 
                                    elif moveblk == False and piece.upper() in self.dic5.keys():
                                        line = line[:-1] #delete +
                                        #line = line[:line.find(". ")+2] + "+" + line[line.find(". ")+2:]                                         
                                    else:
                                        if (moveblk == True and (int(to[1]) < 3 and int(fr[1]) < 3)) or \
                                           (moveblk == False and (int(to[1]) < 7  and int(fr[1]) < 7)):
                                            err= "error in promotion " +to+" Mv: "+ movenr
                                            raise  Moveerror(err)
                                prom = 0
                                
                        else: #drop
                            mv = ""
                            if board[int(to[1])][int(to[0])]!= "":
                                err= "drop to occupied field "+to +" Mv: "+ movenr
                                raise Moveerror(err)               
                            else:
                                if piece in cap:
                                    board[int(to[1])][int(to[0])]= piece
                                    cap.remove(piece)
                                else:
                                    err = "drop of piece not available "+fr +" Mv: "+ movenr
                                    raise Moveerror(err)
                        
                        k = 3
                        while line[k] not in ("0","1","2","3","4","5","6","7","8","9"):
                            k = k + 1                    
                        line=line[:k+2] + mv + line[k+2:]
                outList.append(line)
        except Moveerror:
                m = self.meldung.get()
                self.meldung.set(m + "\n" + err)
                pass
                
        return outList, board, cap






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
     


        self.meldung.set("gepeichert" + f  + "Typ" )







if __name__ == '__main__':
    root = Tk()
    root.wm_title("ShogiQuest Translation")
    root.geometry("400x300")
    app = App(root)
    root.mainloop()





