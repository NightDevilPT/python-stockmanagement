from tkinter import *
from tkinter import messagebox as msg
import os

os.system("clear")

OBJ = {

}

def Scrollable_Window(window,BG="red",V_SCROLL=True,H_SCROLL=True,WIDTH=200,HEIGHT=200,INNER_WIDTH=1000,INNER_HEIGHT=1000,X=0,Y=0):
    global OBJ

    OBJ['frame'] = Frame(window,width=WIDTH,height=HEIGHT,bg=BG)
    OBJ['frame'].place(x=X,y=Y,width=WIDTH,height=HEIGHT)

    OBJ['canvas'] = Canvas(OBJ['frame'],bg=BG)
    
    if V_SCROLL:
        OBJ['v_scroll'] = Scrollbar(OBJ['frame'],orient=VERTICAL,width=15,command=OBJ['canvas'].yview)
        OBJ['v_scroll'].pack(side=RIGHT,fill=BOTH)
        OBJ['canvas'].config(yscrollcommand=OBJ['v_scroll'].set)
    
    if H_SCROLL:
        OBJ['h_scroll'] = Scrollbar(OBJ['frame'],orient=HORIZONTAL,width=15,command=OBJ['canvas'].xview)
        OBJ['h_scroll'].pack(side=BOTTOM,fill=BOTH)
        OBJ['canvas'].config(xscrollcommand=OBJ['h_scroll'].set)

    OBJ['canvas'].pack(side=LEFT,fill=BOTH,expand=1)

    # OBJ['canvas'].bind("<Configure>",lambda event : OBJ['canvas'].configure(scrollregion=OBJ['canvas'].bbox("all")))
    # OBJ['scrollable_frame'] = Frame(OBJ['canvas'],bg=BG)
    # OBJ['canvas'].create_window((0,0),width=INNER_WIDTH,height=INNER_HEIGHT,window=OBJ['scrollable_frame'],anchor=NW)
    OBJ['scrollable_frame'] = Frame(OBJ['canvas'],bg=BG)
    OBJ['canvas'].create_window((0,0),window=OBJ['scrollable_frame'],anchor=NW)

    OBJ['scrollable_frame'].bind("<Configure>",lambda event : OBJ['canvas'].configure(scrollregion=OBJ['canvas'].bbox("all")))
    
    return OBJ['scrollable_frame']