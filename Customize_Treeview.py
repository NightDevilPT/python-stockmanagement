from tkinter import *
from tkinter import messagebox as msg
import os

os.system("clear")

class Customize_Treeview:
    obj={
        'heading':{},
        'data':{}
    }
    Return = None

    def __init__(self):        
        for i in self.obj['heading']:
            try:
                self.obj['heading'][i].destroy()
            except:
                pass
        
        for i in self.obj['data']:
            try:
                self.obj['data'][i].destroy()
            except:
                pass
        
        for i in self.obj:
            try:
                self.obj[i].destroy()
            except:
                pass
        
        self.obj.clear()
        self.obj['heading'] = {}
        self.obj['data'] = {
            'count':0
        }
        
        pass

    
    #####=============[ Scrollable Window Function Start ]=============#####
    def customize_treeview(self,window,V_SCROLL=True,H_SCROLL=True,WIDTH=400,HEIGHT=200,BG="red",X=10,Y=10):
        try:
            self.obj['frame'] = Frame(window,width=WIDTH,height=HEIGHT,bg=BG,highlightbackground=BG)
            self.obj['frame'].place(x=X,y=Y,width=WIDTH,height=HEIGHT)

            self.obj['canvas'] = Canvas(self.obj['frame'],bg=BG,highlightbackground=BG)
            
            if V_SCROLL:
                self.obj['v_scroll'] = Scrollbar(self.obj['frame'],orient=VERTICAL,width=15,command=self.obj['canvas'].yview)
                self.obj['v_scroll'].pack(side=RIGHT,fill=BOTH)
                self.obj['canvas'].config(yscrollcommand=self.obj['v_scroll'].set)
            
            if H_SCROLL:
                self.obj['h_scroll'] = Scrollbar(self.obj['frame'],orient=HORIZONTAL,width=15,command=self.obj['canvas'].xview)
                self.obj['h_scroll'].pack(side=BOTTOM,fill=BOTH)
                self.obj['canvas'].config(xscrollcommand=self.obj['h_scroll'].set)

            self.obj['canvas'].pack(side=LEFT,fill=BOTH,expand=1)

            # self.obj['canvas'].bind("<Configure>",lambda event : self.obj['canvas'].configure(scrollregion=self.obj['canvas'].bbox("all")))
            # self.obj['scrollable_frame'] = Frame(self.obj['canvas'],bg=BG)
            # self.obj['canvas'].create_window((0,0),width=INNER_WIDTH,height=INNER_HEIGHT,window=self.obj['scrollable_frame'],anchor=NW)
            self.obj['scrollable_frame'] = Frame(self.obj['canvas'],bg=BG)
            self.obj['canvas'].create_window((0,0),window=self.obj['scrollable_frame'],anchor=NW)

            self.obj['scrollable_frame'].bind("<Configure>",lambda event : self.obj['canvas'].configure(scrollregion=self.obj['canvas'].bbox("all")))
            
            return self.obj['scrollable_frame']
        except Exception as e:
            print(e)
    #####=============[ Scrollable Window Function End ]=============#####


    #####=============[ Heading Window Function Start ]=============#####
    def Heading(self,heading=(),BG="red",FG="black",FONT=('arial',13,"bold")):
        if len(heading)!=0:
            self.obj['heading']['heading_frame'] = Frame(self.obj['scrollable_frame'],padx=1,pady=1,bg="white")

            for i in heading:
                self.obj['heading'][f"H{heading.index(i)}"] = Label(self.obj['heading']['heading_frame'],text=f"{i}")
                self.obj['heading'][f"H{heading.index(i)}"].config(bg=BG,fg=FG,font=FONT)
                self.obj['heading'][f"H{heading.index(i)}"].pack(side=LEFT,fill=BOTH,padx=1,pady=1)
            
            self.obj['heading']['font'] = FONT
            self.obj['heading']['heading_frame'].pack(side=TOP,fill=BOTH)
    #####=============[ Heading Window Function End ]=============#####


    #####=============[ Heading Config Window Function Start ]=============#####
    def Heading_Config(self,IND=None,WIDTH=20,HEIGHT=1,WRAP=200):
        if IND!=None:
            self.obj['heading'][f'H{IND}'].config(width=WIDTH,height=HEIGHT,pady=5)
            self.obj['heading'][f'H{IND}']['width'] = WIDTH
            self.obj['heading'][f'H{IND}']['height'] = HEIGHT
            self.obj['heading'][f'H{IND}']['wrap'] = WRAP
    #####=============[ Heading Config Window Function End ]=============#####


    #####=============[ Insert Data Window Function End ]=============#####
    def Insert_Data(self,data=(),BG="grey",FG="white",ACTIVE_BG="green",ACTIVE_FG="white"):
        if len(data)!=0:
            ID = self.obj['data']['count']
            self.obj['data'][f"ID{ID}"] = Frame(self.obj['scrollable_frame'],bg="white",padx=1)
            self.obj['data'][f'bg{ID}'] = BG
            self.obj['data'][f'fg{ID}'] = FG

            for i in data:
                self.obj['data'][f'ID{ID}D{data.index(i)}'] = Label(self.obj['data'][f"ID{ID}"],text=f"{i}",bg=BG,fg=FG,font=self.obj['heading']['font'])
                self.obj['data'][f'ID{ID}D{data.index(i)}'].config(width=self.obj['heading'][f'H{data.index(i)}']['width'],wraplength=self.obj['heading'][f'H{data.index(i)}']['wrap'],pady=5)
                self.obj['data'][f'ID{ID}D{data.index(i)}'].bind("<Button-1>",lambda e,ID=ID,total=len(data):self.Active_Frame(ID=ID,total=total,ACTIVE_BG=ACTIVE_BG,ACTIVE_FG=ACTIVE_FG))
                self.obj['data'][f'ID{ID}D{data.index(i)}'].bind("<Double-1>",lambda e,ID=ID,total=len(data):self.Return_Data(ID,total=total))
                self.obj['data'][f'ID{ID}D{data.index(i)}'].pack(side=LEFT,fill=BOTH,padx=1,pady=1)
                # print(f'ID{ID}D{data.index(i)}')
            self.obj['data'][f"ID{ID}"].pack(side=TOP,fill=BOTH)
            self.obj['data']['count'] = self.obj['data']['count'] + 1
    #####=============[ Insert Data Window Function End ]=============#####

    def Return_Data(self,ID=None,total=None):
        if ID!=None:
            lst = []
            for i in range(total):
                lst.append(self.obj['data'][f'ID{ID}D{i}']['text'])
            self.Return = lst
            return self.Return


    def Active_Frame(self,ID=None,total=None,ACTIVE_BG="green",ACTIVE_FG="white"):
        self.Return = None
        if ID!=None:
            for i in range(self.obj['data']['count']):
                if ID==i:
                    # self.obj['data'][f'ID{ID}'].config(bg=ACTIVE_BG)
                    lst = []
                    for j in range(total):
                        self.obj['data'][f'ID{ID}D{j}'].config(bg=ACTIVE_BG,fg=ACTIVE_FG)
                        # self.Return.append(self.obj['data'][f'ID{ID}D{j}']['text'])
                        lst.append(self.obj['data'][f'ID{ID}D{j}']['text'])
                    self.Return = lst
                else:
                    # self.obj['data'][f'ID{i}'].config(bg=self.obj['data'][f'bg{i}'])
                    for j in range(total):
                        self.obj['data'][f'ID{i}D{j}'].config(bg=self.obj['data'][f'bg{i}'],fg=self.obj['data'][f'fg{i}'])
        
        