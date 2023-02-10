import os,io
import re
import cv2
from tkinter import *
import threading as th
from tkinter import ttk,font
import SQL_Queries as sql
import Scrollable_Window as sw
import Customize_Treeview as ct
from tkcalendar import DateEntry
from PIL import Image,ImageTk
import Generate_ID as gid
from tkinter import filedialog as fd
from datetime import datetime as dt
from tkinter import messagebox as msg


class main:
    
    Width = 1330
    Height = 720
    gui_obj = {
        'menu_bar':{},
        'middle_obj':{},
    }
    data_obj = {}
    colors = [
        '#171f26',#0
        '#1d262f',#1
        '#202932',#2
        '#121a23',#3
        '#191a21',#4
        '#21222c',#5
        '#282a36',#6
        '#343746',#7
        '#484950',#8
        '#5971a1',#9
        '#8be9fd',#10
        '#5a8a9a',#11
        '#55e5c5',#12
        '#5d6b99',#13
        '#D1D1D1',#14
        '#E8E8E8',#15
        '#BABABA',#16
        '#F9F6EE',#17
        '#EDEADE'#18
    ]
    db = {
        'db':"Inventory_Management.db",
        
        'admin_table':"Admins_Table",
        'admin_columns':"First_Name,Last_Name,Gender,Phone_No,Email_ID,Password,Security_Que,Security_Ans",
        'admin_columns2':"First_Name=? ,Last_Name=? ,Gender=? ,Phone_No=? ,Email_ID=? ,Password=? ,Security_Que=? ,Security_Ans=? ",
        
        'employe_table':"Employees_Table",
        'employe_columns':"Image, Name, Gender, D_O_B, Email_ID, Phone_No, Address, Proof_Type, Proof_No, Job_Type, Joining_Date",
        'employe_columns2':"Image=?, Name=?, Gender=?, D_O_B=?, Email_ID=?, Phone_No=?, Address=?, Proof_Type=?, Proof_No=?, Job_Type=?, Joining_Date=?",
        
        'items_table':"Items_Table",
        'items_columns':"Product_Name, Product_Type, Quantity, Rate_Per_Quantity, Entry_Date, Entered_By",
        'items_columns2':"Product_Name=?, Product_Type=?, Quantity=?, Rate_Per_Quantity=?, Entry_Date=?, Entered_By=?",
        
        'history_table':"Items_History_Table",
        'history_columns':"Product_Name, Product_Type, Quantity, Rate_Per_Quantity, Entry_Date, Entered_By, Added_Or_Updated",
    }
    cv2_obj = {}
    frame = None
    img_cond = False
    Username = None


    def __init__(self,window):
        #####========[ Creating Admins Table ]========#####
        heading = ("First_Name","Last_Name","Gender","Phone_No","Email_ID","Password","Security_Que","Security_Ans")
        data_types = ("TEXT","TEXT","TEXT","INT","TEXT","TEXT","TEXT","TEXT")
        sql.Create_Table(table_name=self.db['admin_table'],database_name=self.db['db'],heading=heading,data_types=data_types,primary_key="Phone_No")

        #####========[ Creating Employees Table ]========#####
        heading = ("Image","Name","Gender","D_O_B","Email_ID","Phone_No","Address","Proof_Type","Proof_No","Job_Type","Joining_Date")
        data_types = ("BLOB","TEXT","TEXT","TEXT","TEXT","INT","TEXT","TEXT","TEXT","TEXT","TIMESTAMP")
        sql.Create_Table(table_name=self.db['employe_table'],database_name=self.db['db'],heading=heading,data_types=data_types,primary_key="Phone_No")

        #####========[ Creating Items Table ]========#####
        heading = ("Product_Name","Product_Type","Quantity","Rate_Per_Quantity","Entry_Date","Entered_By")
        data_types = ("TEXT","TEXT","INT","REAL","TIMESTAMP","Text")
        sql.Create_Table(table_name=self.db['items_table'],database_name=self.db['db'],heading=heading,data_types=data_types)

        #####========[ Creating Items Table ]========#####
        heading = ("Product_Name","Product_Type", "Quantity", "Rate_Per_Quantity", "Entry_Date", "Entered_By", "Added_Or_Updated")
        data_types = ("TEXT","TEXT","INT","REAL","TIMESTAMP","TEXT","TEXT")
        sql.Create_Table(table_name=self.db['history_table'],database_name=self.db['db'],heading=heading,data_types=data_types)

        try:
            os.mkdir("Employees_ID_Cards")
        except:
            pass

        self.style = ttk.Style()
        self.window = window
        self.window.geometry(f"{self.Width}x{self.Height}+5+5")
        self.window.config(bg=self.colors[7])
        self.window.resizable(0,0)
        self.window.title("Inventory Management ( Develop By NightDevilPT )...")

        self.gui_obj['left_f'] = Frame(self.window,bg=self.colors[0],width=200)
        self.gui_obj['left_f'].pack(side=LEFT,fill=BOTH,padx=2,pady=2)

        self.gui_obj['top_f'] = Frame(self.window,bg=self.colors[0],height=60)
        self.gui_obj['top_f'].pack(side=TOP,fill=BOTH,padx=2,pady=2)

        self.gui_obj['middle_f'] = Frame(self.window,bg=self.colors[0],height=60)
        self.gui_obj['middle_f'].place(x=206,y=78,width=self.Width-208,height=self.Height-80)

        self.gui_obj['title_name_l'] = Label(self.gui_obj['top_f'],text="Inventery Management System")
        self.gui_obj['title_name_l'].config(fg="white",font=("aristotelica small caps",45,"bold"),bg=self.colors[0])
        self.gui_obj['title_name_l'].pack(side=LEFT,padx=10,pady=9,fill=BOTH)

        self.gui_obj['time_l'] = Label(self.gui_obj['top_f'],text="00:00:00")
        self.gui_obj['time_l'].config(font=("arial",14,"bold"),bg=self.colors[0],fg="white")
        self.gui_obj['time_l'].pack(side=RIGHT,fill=BOTH,padx=10)
        self.gui_obj['time_l'].after(1000,lambda:self.time_update())

        data = sql.Select_All_Data(database_name="Inventory_Management.db",table_name="Admins_Table")

        # if len(data)==0:
        #     self.Registration_Form(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
        # else:
        #     self.Login_Form(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])

        # self.Registration_Form(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
        # self.Login_Form(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
        # self.Forget_Password_Form(window=self.gui_obj['middle_f'],obj={})
        self.Home_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
        # self.Employess_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
        # self.Add_Items_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
        self.Menu_Bar_Function(window=self.gui_obj['left_f'],obj=self.gui_obj['menu_bar'])
        # self.Generate_ID_Window(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
        

    def Validation_Inputs(self,data=[]):
        lst = ['firstname', 'lastname', 'phone_no', 'email', 'password', 'security_q', 'security_ans','proof_type','proof_no','name','dob','product_type','product_name',"quantity","rate_per_quantity"]
        ['image','email','phone_no','address']
        
        for i in data:
            if i in lst:
                if self.data_obj[i].get()=="":
                    msg.showerror("Empty Error",f"{i} Entry Box is Empty...")
                    return False
            
            if i=="gender":
                if self.data_obj[i].get()=="":
                    msg.showerror("Empty Error",f"{i} Select Admin Gender...")
                    return False

            ###====== [ Validation For Email ] ======###
            if i=="email":
                regex = r"\b[A-Za-z0-9._%+-]+@[A-za-z0-9.-]+\.[A-z|a-z]{2,}\b"
                
                if re.fullmatch(regex,self.data_obj[i].get()):
                    pass
                else:
                    msg.showerror("InValid Email",f"Enter Valid Email-ID")
                    return False

            ###====== [ Validation For Phone No ] ======###
            if i=="phone_no" or i=="user":
                pattern = re.compile("(0|91)?[6-9][0-9]{9}")
                if pattern.match(self.data_obj[i].get()):
                    pass
                else:
                    msg.showerror("Invalid Phone No","Enter Valid Phone No...")
                    return False
            
            if i=="image":
                if self.img_cond==False:
                    msg.showerror("Image Error","Please Click Employee Image...")
                    return False
            
            if i=='address':
                if self.gui_obj['middle_obj'][f'{i}.e'].get(1.0,END)=="" or self.gui_obj['middle_obj'][f'{i}.e'].get(1.0,END)=="\n":
                    msg.showerror("Empty Box","Enter Employees Address...")
                    return False
            
            if i=="quantity":
                try:
                    da = int(self.data_obj[i].get())
                except:
                    msg.showerror("Data Error","Quantity Should Be In Integer Value...")
                    return False
            
            if i=="rate_per_quantity":
                try:
                    da = float(self.data_obj[i].get())
                except:
                    msg.showerror("Data Error","Rate Per Quantity Should Be In Float Value...")
                    return False
        return True


    ####=============[ Registration Form Function Start ]=============####
    def Registration_Form(self,window=None,obj={},bool=True):
        self.Delete_widgets(obj=obj)
        self.Delete_widgets(obj=self.data_obj)
        w = self.Width-208
        h = self.Height-80
        obj['frame'] = Frame(window,bg=self.colors[2])
        obj['frame'].place(x=w/2-300,y=h/2-550/2,width=600,height=550)

        obj['title'] = Label(obj['frame'],text="Add Admin",pady=4,font=("aristotelica small caps",20,"bold"),fg="white",bg=self.colors[4])
        obj['title'].pack(side=TOP,fill=BOTH)

        ##====== First Name Label Entry Widget
        self.data_obj['firstname'] = StringVar()
        self.data_obj['firstname'].set("")
        obj['firstname_l'] = Label(obj['frame'],text="First Name",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['firstname_l'].place(x=20,y=50,width=150,height=30)
        
        obj['firstname_e'] = Entry(obj['frame'],justify=LEFT,textvariable=self.data_obj['firstname'])
        obj['firstname_e'].place(x=25,y=80,width=250,height=30)
        obj['firstname_e'].config(font=("arial",14,"bold"),bg=self.colors[2],relief=FLAT,bd=0,fg="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])
        
        obj['firstname_f'] = Frame(obj['frame'],bg="white")
        obj['firstname_f'].place(x=20,width=260,height=2,y=111)

        ##====== Last Name Label Entry Widget
        self.data_obj['lastname'] = StringVar()
        self.data_obj['lastname'].set("")
        obj['lastname_l'] = Label(obj['frame'],text="Last Name",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['lastname_l'].place(x=320,y=50,width=150,height=30)
        
        obj['lastname_e'] = Entry(obj['frame'],justify=LEFT,textvariable=self.data_obj['lastname'])
        obj['lastname_e'].place(x=325,y=80,width=250,height=30)
        obj['lastname_e'].config(font=("arial",14,"bold"),bg=self.colors[2],relief=FLAT,bd=0,fg="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])

        obj['lastname_f'] = Frame(obj['frame'],bg="white")
        obj['lastname_f'].place(x=320,width=260,height=2,y=111)
        
        #### Gender Label / Radio Button ####
        obj['gender_label'] = Label(obj['frame'],text="Gender",anchor=W)
        obj['gender_label'].config(bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"))
        obj['gender_label'].place(x=20,y=130)

        self.data_obj['gender'] = StringVar()       #### Gender Variable
        obj['male'] = Radiobutton(obj['frame'],text="Male",variable=self.data_obj['gender'],value='Male',selectcolor=self.colors[2])
        obj['male'].config(font=("aristotelica small caps",14,"bold"),relief=FLAT,bg=self.colors[2],activebackground=self.colors[2],fg="white",activeforeground="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])
        obj['male'].place(x=60,y=160)

        obj['female'] = Radiobutton(obj['frame'],text="Female",variable=self.data_obj['gender'],value='Female',selectcolor=self.colors[2])
        obj['female'].config(font=("aristotelica small caps",14,"bold"),relief=FLAT,bg=self.colors[2],activebackground=self.colors[2],fg="white",activeforeground="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])
        obj['female'].place(x=200,y=160)

        obj['other'] = Radiobutton(obj['frame'],text="Other",variable=self.data_obj['gender'],value='Other',selectcolor=self.colors[2])
        obj['other'].config(font=("aristotelica small caps",14,"bold"),relief=FLAT,bg=self.colors[2],activebackground=self.colors[2],fg="white",activeforeground="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])
        obj['other'].place(x=360,y=160)

        ##====== Phone Number Label Entry Widget
        self.data_obj['phone_no'] = StringVar()
        obj['phone_number_l'] = Label(obj['frame'],text="Phone Number : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['phone_number_l'].place(x=20,y=210,width=150,height=30)
        
        obj['phone_number_e'] = Entry(obj['frame'],justify=LEFT,textvariable=self.data_obj['phone_no'])
        obj['phone_number_e'].place(x=190,y=210,width=350,height=30)
        obj['phone_number_e'].config(font=("arial",14,"bold"),bg=self.colors[2],relief=FLAT,bd=0,fg="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])

        obj['phone_number_f'] = Frame(obj['frame'],bg="white")
        obj['phone_number_f'].place(x=190,width=390,height=2,y=240)

        ##====== Email Label Entry Widget
        self.data_obj['email'] = StringVar()
        obj['email_l'] = Label(obj['frame'],text="Email - ID : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['email_l'].place(x=20,y=260,width=150,height=30)
        
        obj['email_e'] = Entry(obj['frame'],justify=LEFT,textvariable=self.data_obj['email'])
        obj['email_e'].place(x=190,y=260,width=350,height=30)
        obj['email_e'].config(font=("arial",14,"bold"),bg=self.colors[2],relief=FLAT,bd=0,fg="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])

        obj['email_f'] = Frame(obj['frame'],bg="white")
        obj['email_f'].place(x=190,width=390,height=2,y=290)

        ##====== Password Label Entry Widget
        self.data_obj['password'] = StringVar()
        obj['password_l'] = Label(obj['frame'],text="Password : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['password_l'].place(x=20,y=310,width=150,height=30)
        
        obj['password_e'] = Entry(obj['frame'],justify=LEFT,textvariable=self.data_obj['password'],show="")
        obj['password_e'].place(x=190,y=310,width=350,height=30)
        obj['password_e'].config(font=("arial",14,"bold"),bg=self.colors[2],relief=FLAT,bd=0,fg="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])

        hide2 = Image.open("icons/hide.png")
        hide1 = hide2.resize((25,25),Image.ANTIALIAS)
        hide = ImageTk.PhotoImage(hide1)

        show2 = Image.open("icons/show.png")
        show1 = show2.resize((25,25),Image.ANTIALIAS)
        show = ImageTk.PhotoImage(show1)

        def Hide_Unhide_fun(obj={},name=None):
            if obj[name]['show']=='*':
                obj[name]['show']=''
                obj['pass_btn'].config(image = hide)
            else:
                obj[name]['show']='*'
                obj['pass_btn'].config(image = show)

        obj['pass_btn'] = Button(obj['frame'],image=hide,highlightbackground=self.colors[2],highlightcolor=self.colors[2])
        obj['pass_btn'].config(bg=self.colors[2],activebackground=self.colors[2],bd=0,relief=FLAT)
        obj['pass_btn'].config(command=lambda:Hide_Unhide_fun(obj=obj,name="password_e"))
        obj['pass_btn'].place(x=550,y=310,width=25,height=25)

        obj['password_f'] = Frame(obj['frame'],bg="white")
        obj['password_f'].place(x=190,y=340,width=390,height=2)
        
        ##====== Security Question / Answer Widget
        self.data_obj['security_q'] = StringVar()
        obj['security_q_l'] = Label(obj['frame'],text="Security Que : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['security_q_l'].place(x=20,y=360,width=150,height=30)

        self.style.configure("TOptionMenu",font=("aristotelica small caps",14,"bold"))
        # proof_type = ['','Manager','Waiter','Receptinist','Driver']
        proof_type = ['','Favorite Place','Favorite Food']
        self.data_obj['security_q'].set(proof_type[1])
        obj['security_q_entry'] = ttk.OptionMenu(obj['frame'],self.data_obj['security_q'],*proof_type)
        obj['security_q_entry']['menu'].config(bg=self.colors[2],fg="white",font=("arial",14,"bold"),bd=0)
        obj['security_q_entry'].place(x=190,y=360,width=250,height=30)
        
        self.data_obj['security_ans'] = StringVar()
        obj['security_ans_l'] = Label(obj['frame'],text="Security Ans : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['security_ans_l'].place(x=20,y=410,width=150,height=30)
    
        obj['security_ans_e'] = Entry(obj['frame'],justify=LEFT,textvariable=self.data_obj['security_ans'],show="")
        obj['security_ans_e'].place(x=190,y=410,width=350,height=30)
        obj['security_ans_e'].config(font=("arial",14,"bold"),bg=self.colors[2],relief=FLAT,bd=0,fg="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])
        
        obj['security_ans_f'] = Frame(obj['frame'],bg="white")
        obj['security_ans_f'].place(x=190,y=440,width=390,height=2)

        data_names = ("firstname","lastname","gender","phone_no","email","password","security_q","security_ans")
        

        def Insert_Data(bool):
            condition = self.Validation_Inputs(data_names)
            if condition:
                data_val = []
                for i in data_names:
                    if i=="phone_no":
                        data_val.append(int(self.data_obj[i].get()))
                    else:
                        data_val.append(self.data_obj[i].get())
                
                column_name = self.db['admin_columns']
                table_name = self.db['admin_table']

                data_entered_condition = sql.Insert_Data(database_name=self.db['db'],table_name=table_name,columns=column_name,values=data_val)

                if data_entered_condition:
                    msg.showinfo("Data Save","Admin Data Sucessfully Saved...")
                    msg.showinfo("","Now Admin Can Login...")
                    if bool:
                        self.Login_Form(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
                    else:
                        self.Registration_Form(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
                    return
                else:
                    msg.showerror("Data Error","Admin Data Not Saved...")
                    return
            

        ##====== Registration Button Widget
        obj['register_bd'] = Frame(obj['frame'],bg="#03e9f4")
        obj['register_bd'].place(x=320,y=480,width=250,height=34)
        obj['register_btn'] = Button(obj['register_bd'],text="Register Employee",bg=self.colors[2],fg="#03e9f4",relief=FLAT,bd=0)
        obj['register_btn'].config(activebackground="#03e9f4",activeforeground="black",font=("aristotelica small caps",13,"bold"),highlightbackground="#03e9f4")
        obj['register_btn'].place(x=2,y=2,width=246,height=30)
        obj['register_btn'].config(command=lambda:Insert_Data(bool))
    ####=============[ Registration Form Function End ]=============####


    ####=============[ Login Form Function Start ]=============####
    def Login_Form(self,window=None,obj={}):
        self.Delete_widgets(obj=obj)
        self.Delete_widgets(obj=self.data_obj)
        w = self.Width-308
        h = self.Height-150
        obj['frame'] = Frame(window,bg=self.colors[2])
        obj['frame'].place(x=w/2-250,y=h/2-200,width=500,height=400)

        obj['title'] = Label(obj['frame'],text="Employee Login",pady=4,font=("aristotelica small caps",20,"bold"),fg="white",bg=self.colors[4])
        obj['title'].pack(side=TOP,fill=BOTH)

        ##====== Email Label Entry Widget
        self.data_obj['phone_no'] = StringVar()
        obj['user_l'] = Label(obj['frame'],text="Phone No : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['user_l'].place(x=20,y=130,width=250,height=30)
        
        obj['user_e'] = Entry(obj['frame'],justify=LEFT,textvariable=self.data_obj['phone_no'])
        obj['user_e'].place(x=20,y=160,width=350,height=30)
        obj['user_e'].config(font=("arial",14,"bold"),bg=self.colors[2],relief=FLAT,bd=0,fg="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])

        obj['userf'] = Frame(obj['frame'],bg="white")
        obj['userf'].place(x=20,y=190,width=460,height=2)

        ##====== Password Label Entry Widget
        self.data_obj['password'] = StringVar()
        obj['password_l'] = Label(obj['frame'],text="Password : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['password_l'].place(x=20,y=220,width=250,height=30)
        
        obj['password_e'] = Entry(obj['frame'],justify=LEFT,textvariable=self.data_obj['password'],show="")
        obj['password_e'].place(x=20,y=250,width=350,height=30)
        obj['password_e'].config(font=("arial",14,"bold"),bg=self.colors[2],relief=FLAT,bd=0,fg="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])

        obj['password_f'] = Frame(obj['frame'],bg="white")
        obj['password_f'].place(x=20,y=280,width=460,height=2)

        hide2 = Image.open("icons/hide.png")
        hide1 = hide2.resize((25,25),Image.ANTIALIAS)
        hide = ImageTk.PhotoImage(hide1)

        show2 = Image.open("icons/show.png")
        show1 = show2.resize((25,25),Image.ANTIALIAS)
        show = ImageTk.PhotoImage(show1)

        def Hide_Unhide_fun(obj={},name=None):
            if obj[name]['show']=='*':
                obj[name]['show']=''
                obj['pass_btn'].config(image = hide)
            else:
                obj[name]['show']='*'
                obj['pass_btn'].config(image = show)

        obj['pass_btn'] = Button(obj['frame'],image=hide,highlightbackground=self.colors[2],highlightcolor=self.colors[2])
        obj['pass_btn'].config(bg=self.colors[2],activebackground=self.colors[2],bd=0,relief=FLAT)
        obj['pass_btn'].config(command=lambda:Hide_Unhide_fun(obj=obj,name="password_e"))
        obj['pass_btn'].place(x=450,y=250,width=25,height=25)

        ##====== Registration Button Widget
        obj['forget_btn'] = Button(obj['frame'],text="Forget Password",bg=self.colors[2],fg="#03e9f4",relief=FLAT,bd=0)
        obj['forget_btn'].config(activebackground=self.colors[2],activeforeground="#03e9f4",font=font.Font(family="aristotelica small caps",size=12,weight="bold"),highlightbackground=self.colors[2],highlightcolor=self.colors[2])
        obj['forget_btn'].config(command=lambda:self.Forget_Password_Form(window=window,obj=obj))
        obj['forget_btn'].place(x=300,y=290,width=200,height=30)

        def Login_Select_Data_Function():
            lst = ['phone_no','password']
            condition = self.Validation_Inputs(data=lst)
            
            if condition==False:
                return

            user_data = sql.Select_Specified_Data(database_name=self.db['db'],select_data="First_Name,Last_Name",table_name=self.db['admin_table'],key_columns="Phone_No=? and Password=?",key_values=(int(self.data_obj['phone_no'].get()),self.data_obj['password'].get()))

            if len(user_data)==0:
                msg.showerror("Unautorized Error","This User Not Present In Our Database...")
                return

            self.Username = user_data[0][0]+" "+user_data[0][1]

            msg.showinfo("Admin Login",f"Welecom {self.Username}\nHave a Nice Day...")
            
            self.Home_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
            self.Menu_Bar_Function(window=self.gui_obj['left_f'],obj=self.gui_obj['menu_bar'],username=self.Username)                    

        ##====== Registration Button Widget
        obj['login_bd'] = Frame(obj['frame'],bg="#03e9f4")#,highlightbackground=self.colors[2],highlightcolor=self.colors[2])
        obj['login_bd'].place(x=250,y=345,width=200,height=34)
        obj['login_btn'] = Button(obj['login_bd'],text="Login User",bg=self.colors[2],fg="#03e9f4",relief=FLAT,bd=0)
        obj['login_btn'].config(command=lambda:Login_Select_Data_Function())
        obj['login_btn'].config(activebackground="#03e9f4",activeforeground="black",font=("aristotelica small caps",12,"bold"),highlightcolor="#03e9f4",highlightbackground="#03e9f4")
        obj['login_btn'].place(x=2,y=2,width=196,height=30)
    ####=============[ Login Form Function End ]=============####


    ####=============[ Forget Password Form Function Start ]=============####
    def Forget_Password_Form(self,window=None,obj={}):
        self.Delete_widgets(obj=obj)
        self.Delete_widgets(obj=self.data_obj)
        
        w = self.Width-308
        h = self.Height-150
        obj['frame'] = Frame(window,bg=self.colors[2])
        obj['frame'].place(x=w/2-450/2,y=h/2-250/2,width=450,height=300)
        
        obj['title'] = Label(obj['frame'],text="Forget Password Form",pady=4,font=("aristotelica small caps",20,"bold"),fg="white",bg=self.colors[4])
        obj['title'].pack(side=TOP,fill=BOTH)

        ##====== Email Label Entry Widget
        self.data_obj['phone_no'] = StringVar()
        obj['user_l'] = Label(obj['frame'],text="Phone No : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['user_l'].place(x=20,y=80,width=150,height=30)
        
        obj['user_e'] = Entry(obj['frame'],justify=LEFT,textvariable=self.data_obj['phone_no'])
        obj['user_e'].place(x=170,y=80,width=250,height=30)
        obj['user_e'].config(font=("arial",14,"bold"),bg=self.colors[2],relief=FLAT,bd=0,fg="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])

        obj['userf'] = Frame(obj['frame'],bg="white")
        obj['userf'].place(x=170,y=110,width=250,height=2)

        ##====== Security Question / Answer Widget
        self.data_obj['security_q'] = StringVar()
        obj['security_q_l'] = Label(obj['frame'],text="Security Que : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['security_q_l'].place(x=20,y=130,width=150,height=30)

        self.style.configure("TOptionMenu",font=("aristotelica small caps",14,"bold"))
        # proof_type = ['','Manager','Waiter','Receptinist','Driver']
        proof_type = ['','Favorite Place','Favorite Food']
        self.data_obj['security_q'].set(proof_type[1])
        obj['security_q_entry'] = ttk.OptionMenu(obj['frame'],self.data_obj['security_q'],*proof_type)
        obj['security_q_entry']['menu'].config(bg=self.colors[2],fg="white",font=("arial",14,"bold"),bd=0)
        obj['security_q_entry'].place(x=170,y=130,width=250,height=30)
        
        self.data_obj['security_ans'] = StringVar()
        obj['security_ans_l'] = Label(obj['frame'],text="Security Ans : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['security_ans_l'].place(x=20,y=180,width=150,height=30)
        
        obj['security_ans_e'] = Entry(obj['frame'],justify=LEFT,textvariable=self.data_obj['security_ans'],show="")
        obj['security_ans_e'].place(x=170,y=180,width=250,height=30)
        obj['security_ans_e'].config(font=("arial",14,"bold"),bg=self.colors[2],relief=FLAT,bd=0,fg="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])
        
        obj['security_ans_f'] = Frame(obj['frame'],bg="white")
        obj['security_ans_f'].place(x=170,y=210,width=250,height=2)

        hide2 = Image.open("icons/hide.png")
        hide1 = hide2.resize((25,25),Image.ANTIALIAS)
        hide = ImageTk.PhotoImage(hide1)

        show2 = Image.open("icons/show.png")
        show1 = show2.resize((25,25),Image.ANTIALIAS)
        show = ImageTk.PhotoImage(show1)

        def Hide_Unhide_fun(obj={},name=None):
            if obj[name]['show']=='*':
                obj[name]['show']=''
                obj['pass_btn'].config(image = hide)
            else:
                obj[name]['show']='*'
                obj['pass_btn'].config(image = show)

        def Fetch_Data():
            lst = ['phone_no','security_q','security_ans']
            condition = self.Validation_Inputs(data=lst)
            
            if condition==False:
                return

            user_data = sql.Select_Specified_Data(database_name=self.db['db'],table_name=self.db['admin_table'],key_columns="Phone_No=? and Security_Que=? and Security_Ans=?",key_values=(int(self.data_obj['phone_no'].get()),self.data_obj['security_q'].get(),self.data_obj['security_ans'].get()))

            if user_data==False:
                msg.showerror("Error","This User Not Present In Our DataBase...")
                return
            else:
                Show_Password()

        ##====== Fetch Data Button Widget
        obj['fetch_bd'] = Frame(obj['frame'],bg="#03e9f4")#,highlightbackground=self.colors[2],highlightcolor=self.colors[2])
        obj['fetch_bd'].place(x=250,y=230,width=150,height=34)
        obj['fetch_btn'] = Button(obj['fetch_bd'],text="Fetch User",bg=self.colors[2],fg="#03e9f4",relief=FLAT,bd=0,highlightbackground="#03e9f4",highlightcolor="#03e9f4")
        obj['fetch_btn'].config(activebackground="#03e9f4",activeforeground="black",font=("aristotelica small caps",12,"bold"))
        obj['fetch_btn'].config(command=lambda:Fetch_Data())
        obj['fetch_btn'].place(x=2,y=2,width=146,height=30)

        obj['back_btn'] = Button(obj['frame'],text="Login Page",bg=self.colors[2],fg="#03e9f4",relief=FLAT,bd=0,highlightbackground=self.colors[2],highlightcolor="#03e9f4")
        obj['back_btn'].config(activebackground=self.colors[2],activeforeground="#03e9f4",font=("aristotelica small caps",12,"bold"))
        obj['back_btn'].config(command=lambda:self.Login_Form(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj']))
        obj['back_btn'].place(x=20,y=232,width=146,height=30)

        def Show_Password():
            w = self.Width-308
            h = self.Height-150
            obj['frame'].place(x=w/2-450/2,y=h/2-300/2,width=450,height=350)

            obj['fetch_bd'].destroy()
            obj['fetch_btn'].destroy()

            ##====== Password Label Entry Widget
            self.data_obj['password'] = StringVar()
            obj['password_l'] = Label(obj['frame'],text="New Password : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
            obj['password_l'].place(x=20,y=240,width=150,height=30)

            obj['password_e'] = Entry(obj['frame'],justify=LEFT,textvariable=self.data_obj['password'],show="")
            obj['password_e'].place(x=170,y=240,width=250,height=30)
            obj['password_e'].config(font=("arial",14,"bold"),bg=self.colors[2],relief=FLAT,bd=0,fg="white",highlightbackground=self.colors[2],highlightcolor=self.colors[2])

            obj['password_f'] = Frame(obj['frame'],bg="white")
            obj['password_f'].place(x=170,y=270,width=250,height=2)

            obj['pass_btn'] = Button(obj['frame'],image=hide,highlightbackground=self.colors[2],highlightcolor=self.colors[2])
            obj['pass_btn'].config(bg=self.colors[2],activebackground=self.colors[2],bd=0,relief=FLAT)
            obj['pass_btn'].config(command=lambda:Hide_Unhide_fun(obj=obj,name="password_e"))
            obj['pass_btn'].place(x=400,y=240,width=25,height=25)

            def Update_Password():
                lst = ['phone_no','security_q','security_ans','password']
                condition = self.Validation_Inputs(data=lst)
                
                if condition==False:
                    return
                
                user_data = sql.Select_Specified_Data(database_name=self.db['db'],select_data="Phone_No",table_name=self.db['admin_table'],key_columns="Phone_No=? and Security_Que=? and Security_Ans=?",key_values=(int(self.data_obj['phone_no'].get()),self.data_obj['security_q'].get(),self.data_obj['security_ans'].get()))
                key_value = ""

                if len(user_data)==0 or user_data==False:
                    msg.showinfo("Error","Password Not Updated\nPlease Try Again...")
                    self.Forget_Password_Form(window=self.gui_obj['middle_f'],obj=obj)
                    return
                
                key_value = user_data[0][0]
                key_column = "Phone_No"
                update_column = "Password=?"
                update_value = (self.data_obj['password'].get(),)
                table_name = self.db['admin_table']

                condition = sql.Update_Data(database_name=self.db['db'],table_name=table_name,update_column=update_column,update_value=update_value,key_column=key_column,key_value=key_value)
                if condition:
                    msg.showinfo("Admin Login","Your Password Sucessfully Updated")
                    msg.showinfo("Admin Login","Now You Can Login With Your New Password...")
                    self.Login_Form(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
                    return
                

            ##====== Update Password Button Widget
            obj['update_bd'] = Frame(obj['frame'],bg="#03e9f4")#,highlightbackground=self.colors[2],highlightcolor=self.colors[2])
            obj['update_bd'].place(x=250,y=290,width=150,height=34)
            obj['update_btn'] = Button(obj['update_bd'],text="Update Password",bg=self.colors[2],fg="#03e9f4",relief=FLAT,bd=0,highlightbackground="#03e9f4",highlightcolor="#03e9f4")
            obj['update_btn'].config(activebackground="#03e9f4",activeforeground="black",font=font.Font(family="aristotelica small caps",size=12,weight="bold"),highlightbackground="#03e9f4")
            obj['update_btn'].config(command=lambda:Update_Password())
            obj['update_btn'].place(x=2,y=2,width=146,height=30)

            obj['back_btn'].place(x=20,y=292,width=146,height=30)
    ####=============[ Forget Password Form Function End ]=============####


    ####=============[ Employee Window Function Start ]=============####
    def Employess_Window_Function(self,window=None,obj={}):
        w = self.Width-208
        h = self.Height-80
        self.img_cond = False
        F = ("arial",12,"bold")
        self.Delete_widgets(obj=obj)
        self.Delete_widgets(obj=self.data_obj)

        obj['frame'] = Frame(window,width=w-20,bg=self.colors[2])
        obj['frame'].place(x=15,y=15,width=w-30,height=h-30)

        obj['title'] = Label(obj['frame'],text="Employee Registration",pady=4)
        obj['title'].config(font=("aristotelica small caps",20,"bold"),fg="white",bg=self.colors[4])
        obj['title'].pack(side=TOP,fill=BOTH)

        #####================= Name Label / Entry Widget
        self.data_obj['name'] = StringVar()
        self.data_obj['name'].set("")
        obj['name.l'] = Label(obj['frame'],text="Name :",anchor=W)
        obj['name.l'].config(bg=self.colors[2],fg="white",font=F)
        obj['name.l'].place(x=20,y=60,width=100,height=30)

        obj['name.e'] = Entry(obj['frame'],textvariable=self.data_obj['name'],highlightcolor="white")
        obj['name.e'].config(bg=self.colors[2],fg="white",font=F)
        obj['name.e'].place(x=150,y=60,width=200,height=30)
        
        #####================= Gender Label / Entry Widget
        obj['gender.l'] = Label(obj['frame'],text="Gender : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['gender.l'].place(x=20,y=110,width=100,height=30)

        self.style.configure("TOptionMenu",font=("aristotelica small caps",14,"bold"))
        
        gender = ['',"Male","Female","Other"]
        self.data_obj['gender'] = StringVar()
        self.data_obj['gender'].set(gender[1])
        obj['gender.e'] = ttk.OptionMenu(obj['frame'],self.data_obj['gender'],*gender)
        obj['gender.e']['menu'].config(bg=self.colors[2],fg="white",font=F,bd=0)
        obj['gender.e'].place(x=150,y=110,width=200,height=30)
        
        #####================= D.O.B Label / Entry Widget
        self.data_obj['dob'] = StringVar()
        obj['dob.l'] = Label(obj['frame'],text="D.O.B : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['dob.l'].place(x=20,y=160,width=100,height=30)
        
        obj['dob.e'] = DateEntry(obj['frame'],textvariable=self.data_obj['dob'],background=self.colors[2],fg="white")
        obj['dob.e'].place(x=150,y=160,width=200,height=30)

        #####================= Email-ID Label / Entry Widget
        self.data_obj['email'] = StringVar()
        obj['email.l'] = Label(obj['frame'],text="Email-ID : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['email.l'].place(x=20,y=210,width=100,height=30)

        obj['email.e'] = Entry(obj['frame'],textvariable=self.data_obj['email'],highlightcolor="white")
        obj['email.e'].config(bg=self.colors[2],fg="white",font=F,bd=0)
        obj['email.e'].place(x=150,y=210,width=200,height=30)
        
        #####================= Contact-No Label / Entry Widget
        self.data_obj['phone_no'] = StringVar()
        obj['phone_no.l'] = Label(obj['frame'],text="Phone No : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['phone_no.l'].place(x=20,y=260,width=100,height=30)

        obj['phone_no.e'] = Entry(obj['frame'],textvariable=self.data_obj['phone_no'],highlightcolor="white")
        obj['phone_no.e'].config(bg=self.colors[2],fg="white",font=F,bd=0)
        obj['phone_no.e'].place(x=150,y=260,width=200,height=30)
        
        #####================= Address Label / Entry Widget
        self.data_obj['address'] = StringVar()
        obj['address.l'] = Label(obj['frame'],text="Address : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['address.l'].place(x=370,y=60,width=100,height=30)

        obj['address.e'] = Text(obj['frame'],highlightcolor="white",)
        obj['address.e'].config(bg=self.colors[2],fg="white",font=F,bd=0)
        obj['address.e'].place(x=490,y=60,width=200,height=80)
        
        #####================= Proof Type Label / Entry Widget
        obj['proof_type.l'] = Label(obj['frame'],text="Proof Type : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['proof_type.l'].place(x=370,y=160,width=100,height=30)

        proof_type = ['',"Aadhar Card","PAN Card","Driving Licence"]
        self.data_obj['proof_type'] = StringVar()
        self.data_obj['proof_type'].set(proof_type[1])
        obj['proof_type.e'] = ttk.OptionMenu(obj['frame'],self.data_obj['proof_type'],*proof_type)
        obj['proof_type.e']['menu'].config(bg=self.colors[2],fg="white",font=F,bd=0)
        obj['proof_type.e'].place(x=490,y=160,width=200,height=30)

        #####================= Proof No Label / Entry Widget
        self.data_obj['proof_no'] = StringVar()
        obj['proff_no.l'] = Label(obj['frame'],text="Proof No : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['proff_no.l'].place(x=370,y=210,width=100,height=30)

        obj['proff_no.e'] = Entry(obj['frame'],highlightcolor="white",textvariable=self.data_obj['proof_no'])
        obj['proff_no.e'].config(bg=self.colors[2],fg="white",font=F,bd=0)
        obj['proff_no.e'].place(x=490,y=210,width=200,height=30)

        #####================= Job Type Label / Entry Widget
        obj['job_type.l'] = Label(obj['frame'],text="Job Type : ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['job_type.l'].place(x=370,y=260,width=100,height=30)

        job_type = ['',"Manager","Seller"]
        self.data_obj['job_type'] = StringVar()
        self.data_obj['job_type'].set(job_type[1])
        obj['job_type.e'] = ttk.OptionMenu(obj['frame'],self.data_obj['job_type'],*job_type)
        obj['job_type.e']['menu'].config(bg=self.colors[2],fg="white",font=F,bd=0)
        obj['job_type.e'].place(x=490,y=260,width=200,height=30)

        #####================= User Image Label / Button Widget
        obj['user_img'] = Label(obj['frame'],bg="lightblue")
        obj['user_img'].place(x=710,y=60,width=150,height=150)

        obj['user_img_btn'] = Button(obj['frame'],text="Take Image",bg="lightblue",font=("arial",12,"bold"))
        obj['user_img_btn'].config(activebackground="lightblue",activeforeground="black",highlightbackground="lightblue",bd=0,relief=FLAT)
        obj['user_img_btn'].config(command=lambda:self.Take_Image_Window(obj=self.cv2_obj))
        obj['user_img_btn'].place(x=710,y=230,width=150,height=30)
        
        data_name = ['image','name','gender','dob','email','phone_no','address','proof_type','proof_no','job_type']

        ####========= [ Inserting Data In DataBase Function ]
        def Insert_Data():
            print("Insert")
            conditions = self.Validation_Inputs(data=data_name)
            print(conditions)
            if conditions==False:
                return
            
            values = []
            self.Append_Values(values=values,data_name=data_name)
            join_date = dt.now().strftime("%d/%m/%Y-%I:%M:%S %p")
            values.append(join_date)

            conditions = sql.Insert_Data(database_name=self.db['db'],table_name=self.db['employe_table'],columns=self.db['employe_columns'],values=values)

            if conditions:
                msg.showinfo("Data Saved","Employee Data Sucessfully Saved...")
                self.Employess_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
                return
            else:
                msg.showerror("Error","Employee Data Not Saved\nPlease Try Again...")
                return

        #####================= Add Employee Button
        obj['add.btn'] = Button(obj['frame'],text="Add Employee",font=("arial",12,"bold"))
        obj['add.btn'].config(bg="green",fg="white",activebackground="green",activeforeground="white",highlightbackground="green",relief=FLAT,bd=0)
        obj['add.btn'].config(command=lambda:Insert_Data())
        obj['add.btn'].place(x=890,y=60,width=170,height=30)

        ####========= [ Updating Data In DataBase Function ]
        def Update_Data():
            conditions = self.Validation_Inputs(data=data_name)
            
            if conditions==False:
                return

            join_date = self.data_obj['data'][-1]
            key_val = self.data_obj['data'][5]
            
            values = []
            self.Append_Values(values=values,data_name=data_name)
            values.append(join_date)

            condition = sql.Update_Data(database_name=self.db['db'],table_name=self.db['employe_table'],update_column=self.db['employe_columns2'],update_value=tuple(values),key_column="Phone_No",key_value=key_val)
            
            if condition:
                msg.showinfo("Update Data","Employee Data Sucessfully Updated...")
                self.Employess_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
            else:
                msg.showerror("Error","Employee Data Not Updated...")
            self.data_obj['data'] = []

        #####================= Add Employee Button
        obj['update.btn'] = Button(obj['frame'],text="Update Employee",font=("arial",12,"bold"))
        obj['update.btn'].config(bg="blue",fg="white",activebackground="blue",activeforeground="white",highlightbackground="blue",bd=0,relief=FLAT)
        obj['update.btn'].config(command=lambda:Update_Data())
        obj['update.btn'].place(x=890,y=125,width=170,height=30)

        ####========= [ Deleting / Removing Data In DataBase Function ]
        def Remove_data():
            ind = obj['cc'].Return
            if ind==None:
                return
            
            key_val = ind[4]
            condition = sql.Delete_Data(database_name=self.db['db'],table_name=self.db['employe_table'],key_column="Phone_No",key_value=key_val)
            
            if condition:
                msg.showinfo("Delete Data","Employee Data Sucessfully Deleted...")
                self.Employess_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
            else:
                msg.showerror("Delete Error","Employee Data Not Deleted...")
                return

        #####================= Delete Employee Button
        obj['delete.btn'] = Button(obj['frame'],text="Delete Employee",font=("arial",12,"bold"))
        obj['delete.btn'].config(bg="red",fg="white",activebackground="red",activeforeground="white",highlightbackground="red",relief=FLAT,bd=0)
        obj['delete.btn'].config(command=lambda:Remove_data())
        obj['delete.btn'].place(x=890,y=195,width=170,height=30)

        ####========= [ Clearing Inputs / Widgets Function ]
        def Clear_Inputs():
            self.data_obj['name'].set("")
            self.data_obj['gender'].set(gender[1])
            self.data_obj['dob'].set("")
            self.data_obj['job_type'].set(job_type[1])
            self.data_obj['phone_no'].set("")
            self.data_obj['proof_no'].set("")
            self.data_obj['email'].set("")
            obj['address.e'].delete(1.0,END)
            self.data_obj['proof_type'].set(proof_type[1])
            self.img_cond = False
            obj['user_img'].config(image="")

        #####================= Add Employee Button
        obj['clear.btn'] = Button(obj['frame'],text="Clear",font=("arial",12,"bold"))
        obj['clear.btn'].config(bg="grey",fg="white",activebackground="grey",activeforeground="white",highlightbackground="grey",bd=0,relief=FLAT)
        obj['clear.btn'].config(command=lambda:Clear_Inputs())
        obj['clear.btn'].place(x=890,y=260,width=170,height=30)


        obj['frame2'] = Frame(obj['frame'],bg=self.colors[7])
        obj['frame2'].place(x=20,y=310,width=w-80,height=280)

        obj['title2'] = Label(obj['frame2'],text="Employee Registration Details",pady=4)
        obj['title2'].config(font=("aristotelica small caps",20,"bold"),fg="white",bg=self.colors[4])
        obj['title2'].pack(side=TOP,fill=BOTH)

        fetched_data = sql.Select_All_Data(database_name=self.db['db'],table_name=self.db['employe_table'])

        #####========== Creating Custom TreeView
        def Create_Treeview(fetched_data=[]):
            obj['cc'] = ct.Customize_Treeview()
            obj['cc'].customize_treeview(window=obj['frame2'],WIDTH=1030,HEIGHT=185,BG=self.colors[2],X=5,Y=85)
            
            obj['cc'].Heading(heading=("Name","Gender","D.O.B","Email-ID","Phone No","Address","Proof Type","Proof No","Job Type","Joining Date"),BG="black",FG="white",FONT=("arial",13,"bold"))
            obj['cc'].Heading_Config(IND=0,WIDTH=20,WRAP=200)
            obj['cc'].Heading_Config(IND=1,WIDTH=15,WRAP=150)
            obj['cc'].Heading_Config(IND=2,WIDTH=15,WRAP=150)
            obj['cc'].Heading_Config(IND=3,WIDTH=40,WRAP=400)
            obj['cc'].Heading_Config(IND=4,WIDTH=20,WRAP=200)
            obj['cc'].Heading_Config(IND=5,WIDTH=40,WRAP=400)
            obj['cc'].Heading_Config(IND=6,WIDTH=20,WRAP=200)
            obj['cc'].Heading_Config(IND=7,WIDTH=25,WRAP=250)
            obj['cc'].Heading_Config(IND=8,WIDTH=25,WRAP=250)
            obj['cc'].Heading_Config(IND=9,WIDTH=25,WRAP=250)

            fetched_data = list(fetched_data)

            for i in fetched_data:
                DF = fetched_data.index(i)
                BG = ""
                if DF%2==0:
                    BG = self.colors[4]
                else:
                    BG = self.colors[6]
                
                selected_data = []
                selected_data = [i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]]

                obj['cc'].Insert_Data(data=selected_data,BG=BG,FG="white",ACTIVE_BG="green",ACTIVE_FG="white")
        

        #####========== Uploading Selected Data In Entry Widgets Function
        def Upload_Data():
            ind = obj['cc'].Return
            if ind==None:
                return

            data = sql.Select_Specified_Data(database_name=self.db['db'],table_name=self.db['employe_table'],key_columns="Phone_No=?",key_values=(int(ind[4]),))
            data = data[0]
            
            self.data_obj['data'] = data

            self.img_cond = True
            self.frame_rb = data[0]

            img_rb = io.BytesIO(data[0])
            img = Image.open(img_rb)
            img2 = img.resize((150,150),Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(img2)

            obj['user_img'].config(image=imgtk)
            obj['user_img'].image=imgtk

            self.data_obj['name'].set(data[1])
            self.data_obj['gender'].set(data[2])
            self.data_obj['dob'].set(data[3])
            self.data_obj['email'].set(data[4])
            self.data_obj['phone_no'].set(data[5])
            obj['address.e'].delete(1.0,END)
            obj['address.e'].insert(0.0,data[6])
            self.data_obj['proof_type'].set(data[7])
            self.data_obj['proof_no'].set(data[8])
            self.data_obj['job_type'].set(data[9])

        obj['upload.btn'] = Button(obj['frame2'],text="Upload Data",font=("arial",12,"bold"))
        obj['upload.btn'].config(bg="seagreen",fg="white",activebackground="seagreen",activeforeground="white",highlightbackground="seagreen",bd=0,relief=FLAT)
        obj['upload.btn'].config(command=lambda:Upload_Data())
        obj['upload.btn'].place(x=880,y=45,width=150,height=30)

        obj['select.lbl'] = Label(obj['frame2'],text="Select Column :",font=("arial",13,"bold"),bg=self.colors[7],fg="white")
        obj['select.lbl'].place(x=10,y=45,width=150,height=30)

        ####========= [ Fetching Specified Data In DataBase Function ]
        def Select_Column_Data():
            os.system("clear")
            column = self.data_obj['select_column'].get()
            data = self.data_obj['column_data'].get()
            
            data = sql.Select_Data_Using_Like(database_name=self.db['db'],Table_Name=self.db['employe_table'],ID=column,Values=data)

            if data=="":
                Create_Treeview(fetched_data)
                return
            
            Create_Treeview(data)

        select_column = ['',"Name","Gender","D_O_B","Email_ID","Phone_No","Address","Proof_Type","Proof_No"]
        self.data_obj['select_column'] = StringVar()
        self.data_obj['select_column'].set(select_column[1])
        obj['select_column.e'] = ttk.OptionMenu(obj['frame2'],self.data_obj['select_column'],*select_column)
        obj['select_column.e']['menu'].config(bg=self.colors[2],fg="white",font=F,bd=0)
        obj['select_column.e'].place(x=170,y=45,width=150,height=30)

        obj['column_data.lbl'] = Label(obj['frame2'],text="Column data :",font=("arial",13,"bold"),bg=self.colors[7],fg="white")
        obj['column_data.lbl'].place(x=340,y=45,width=150,height=30)

        self.data_obj['column_data'] = StringVar()
        self.data_obj['column_data'].set("")
        obj['select_column.e'] = Entry(obj['frame2'],highlightcolor="white",textvariable=self.data_obj['column_data'])
        obj['select_column.e'].config(bg="grey",fg="black",font=F,bd=0)
        obj['select_column.e'].place(x=490,y=45,width=200,height=30)

        obj['show.btn'] = Button(obj['frame2'],text="Show",font=("arial",12,"bold"))
        obj['show.btn'].config(bg="green",fg="white",activebackground="green",activeforeground="white",highlightbackground="green",bd=0,relief=FLAT)
        obj['show.btn'].config(command=lambda:Select_Column_Data())
        obj['show.btn'].place(x=710,y=45,width=100,height=30)

        Create_Treeview(fetched_data)
    ####=============[ Employee Window Function End ]=============####


    ####=============[ Add Iteams Window Function Start ]=============####
    def Add_Items_Window_Function(self,window=None,obj={}):
        w = self.Width-208
        h = self.Height-80
        F = ("arial",15,"bold")
        self.Delete_widgets(obj=obj)
        self.Delete_widgets(obj=self.data_obj)
        
        product_type = ['']
        data = sql.Select_All_Data(database_name=self.db['db'],table_name=self.db['items_table'])
        
        for i in data:
            if i[1] not in product_type:
                product_type.append(i[1])
      

        obj['frame'] = Frame(window,width=w-20,bg=self.colors[2])
        obj['frame'].place(x=15,y=15,width=w-30,height=h-30)

        obj['title'] = Label(obj['frame'],text="Add Items",pady=4)
        obj['title'].config(font=("aristotelica small caps",20,"bold"),fg="white",bg=self.colors[4])
        obj['title'].pack(side=TOP,fill=BOTH)

        #####================= Product Type Label / Entry Widget
        obj['product_type.l'] = Label(obj['frame'],text="Product Type ",bg=self.colors[2],fg="white",font=("aristotelica small caps",14,"bold"),anchor=W)
        obj['product_type.l'].place(x=30,y=60,width=150,height=30)

        
        self.data_obj['product_type'] = StringVar()
        self.data_obj['product_type'].set(product_type[0])
        obj['product_type.e'] = ttk.Combobox(obj['frame'],textvariable=self.data_obj['product_type'],values=product_type,font=F,justify=CENTER)
        obj['product_type.e'].place(x=200,y=60,width=300,height=30)

        #####================= Product Name Label / Entry Widget
        self.data_obj['product_name'] = StringVar()
        self.data_obj['product_name'].set("")
        obj['productname.l'] = Label(obj['frame'],text="Product Name",bg=self.colors[2])
        obj['productname.l'].config(font=("aristotelica small caps",15,"bold"),anchor=W,fg="white")
        obj['productname.l'].place(x=30,y=110,width=180,height=30)

        obj['productname.e'] = Entry(obj['frame'],textvariable=self.data_obj['product_name'],bg=self.colors[2],highlightcolor="white")
        obj['productname.e'].config(font=F,justify=CENTER,fg="white")
        obj['productname.e'].place(x=200,y=110,width=300,height=30)
        
        #####================= Quantity Label / Entry Widget
        self.data_obj['quantity'] = StringVar()
        self.data_obj['quantity'].set("")
        obj['quantity.l'] = Label(obj['frame'],text="Quantity",bg=self.colors[2])
        obj['quantity.l'].config(font=("aristotelica small caps",15,"bold"),anchor=W,fg="white")
        obj['quantity.l'].place(x=550,y=60,width=180,height=30)

        obj['quantity.e'] = Entry(obj['frame'],textvariable=self.data_obj['quantity'],bg=self.colors[2],highlightcolor="white")
        obj['quantity.e'].config(font=F,justify=CENTER,fg="white")
        obj['quantity.e'].place(x=750,y=60,width=300,height=30)

        #####================= Rate / Quantity Label / Entry Widget
        self.data_obj['rate_per_quantity'] = StringVar()
        self.data_obj['rate_per_quantity'].set("")
        obj['rate_per_quantity.l'] = Label(obj['frame'],text="Rate Per Quantity",bg=self.colors[2])
        obj['rate_per_quantity.l'].config(font=("aristotelica small caps",15,"bold"),anchor=W,fg="white")
        obj['rate_per_quantity.l'].place(x=550,y=110,width=180,height=30)

        obj['rate_per_quantity.e'] = Entry(obj['frame'],textvariable=self.data_obj['rate_per_quantity'],bg=self.colors[2],highlightcolor="white")
        obj['rate_per_quantity.e'].config(font=F,justify=CENTER,fg="white")
        obj['rate_per_quantity.e'].place(x=750,y=110,width=300,height=30)
        
        data = ['product_name','product_type','quantity','rate_per_quantity']

        ######=============== [ Inserting Items Data ]
        def Insert_Data():
            condition = self.Validation_Inputs(data=data)

            if condition==False:
                return

            values = []
            self.Append_Values(values=values,data_name=data)
            values.append(dt.now().strftime("%d/%m/%Y-%I:%M:%S"))
            values.append(self.Username)

            history_values = values.copy()

            datas = sql.Select_Specified_Data(database_name=self.db['db'],table_name=self.db['items_table'],select_data="Product_Name,Quantity",key_columns="Product_Name=?",key_values=(self.data_obj['product_name'].get(),))
            itemcondition = None
            historycondition = None

            if len(datas)!=0:
                datas = datas[0]
                values[2] = values[2]+int(datas[1])
                history_values.append("Added")
                itemcondition = sql.Update_Data(database_name=self.db['db'],table_name=self.db['items_table'],update_column=self.db['items_columns2'],update_value=tuple(values),key_column="Product_Name",key_value=datas[0])
                historycondition = sql.Insert_Data(database_name=self.db['db'],table_name=self.db['history_table'],columns=self.db['history_columns'],values=history_values)                
            else:
                history_values.append("Added")
                itemcondition = sql.Insert_Data(database_name=self.db['db'],table_name=self.db['items_table'],columns=self.db['items_columns'],values=values)
                historycondition = sql.Insert_Data(database_name=self.db['db'],table_name=self.db['history_table'],columns=self.db['history_columns'],values=history_values)

            if itemcondition==True and historycondition==True:
                msg.showinfo("Data Info","Item Sucessfully Saved in DataBase...")
                self.Add_Items_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
                return
            else:
                msg.showerror("Error","Item Not Saved or Added in DataBase...")
                return
        
        #####================= Add Button Widget
        obj['add.btn'] = Button(obj['frame'],text="Add Item",bg="green",fg="white",font=("arial",14,"bold"),)
        obj['add.btn'].config(activebackground="green",activeforeground="white",highlightbackground=self.colors[2],relief=FLAT,bd=0)
        obj['add.btn'].config(command=lambda:Insert_Data())
        obj['add.btn'].place(x=30,width=200,height=35,y=160)

        ######=============== [ Updating Items Data ]
        def Update_Data():
            input_condition = self.Validation_Inputs(data)

            if input_condition==False:
                return
            
            val = obj['cc'].Return

            if len(val)==0:
                return
            
            key_column = "Product_Name"
            key_val = val[1]
            
            values = []
            self.Append_Values(values=values,data_name=data)
            values.append(dt.now().strftime("%d/%m/%Y-%I:%M:%S"))
            values.append(self.Username)

            history_values = values.copy()
            history_values.append("Updated")

            condition = sql.Update_Data(database_name=self.db['db'],table_name=self.db['items_table'],update_column=self.db['items_columns2'],update_value=tuple(values),key_column=key_column,key_value=key_val)
            historycondition = sql.Insert_Data(database_name=self.db['db'],table_name=self.db['history_table'],columns=self.db['history_columns'],values=history_values)
            
            if condition and historycondition:
                msg.showinfo("Update Data","Data Sucessfully Updated...")
                self.Add_Items_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
                return
            else:
                msg.showerror("Update Error","Data Not Updated...")
                return

        #####================= Update Button Widget
        obj['update.btn'] = Button(obj['frame'],text="Update Item",bg="blue",fg="white",font=("arial",14,"bold"),)
        obj['update.btn'].config(activebackground="blue",activeforeground="white",highlightbackground=self.colors[2],relief=FLAT,bd=0)
        obj['update.btn'].config(command=lambda:Update_Data())
        obj['update.btn'].place(x=310,width=200,height=35,y=160)

        ######=============== [ Deleting Items Data ]
        def Delete_Data():
            val = obj['cc'].Return
            
            if len(val)==0:
                return

            key_col = "Product_Name"
            key_val = val[1]

            values = [val[1],val[2],val[3],val[4],dt.now().strftime("%d/%m/%Y-%I:%M:%S"),self.Username,"Deleted"]
            
            delete_condition = sql.Delete_Data(database_name=self.db['db'],table_name=self.db['items_table'],key_column=key_col,key_value=key_val)
            historycondition = sql.Insert_Data(database_name=self.db['db'],table_name=self.db['history_table'],columns=self.db['history_columns'],values=values)
            
            if delete_condition and historycondition:
                msg.showinfo("Delete Data","Data Sucessfully Deleted...")
                self.Add_Items_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'])
                return
            else:
                msg.showerror("Delete Error","Data Not Deleted...")
                return


        #####================= Update Button Widget
        obj['delete.btn'] = Button(obj['frame'],text="Delete Item",bg="red",fg="white",font=("arial",14,"bold"),)
        obj['delete.btn'].config(activebackground="red",activeforeground="white",highlightbackground=self.colors[2],relief=FLAT,bd=0)
        obj['delete.btn'].config(command=lambda:Delete_Data())
        obj['delete.btn'].place(x=580,width=200,height=35,y=160)

        ######=============== [ Clearing Widgets Data ]
        def Clear_Inputs():
            self.data_obj['quantity'].set("")
            self.data_obj['rate_per_quantity'].set("")
            self.data_obj['product_name'].set("")
            self.data_obj['product_type'].set("")
            obj['cc'].Return = []

        #####================= Clear Button Widget
        obj['clear.btn'] = Button(obj['frame'],text="Clear Boxes",bg="#555555",fg="white",font=("arial",14,"bold"),)
        obj['clear.btn'].config(activebackground="grey",activeforeground="white",highlightbackground=self.colors[2],relief=FLAT,bd=0)
        obj['clear.btn'].config(command=lambda:Clear_Inputs())
        obj['clear.btn'].place(x=850,width=200,height=35,y=160)
        
        obj['frame2'] = Frame(obj['frame'],bg=self.colors[7])
        obj['frame2'].place(x=20,y=240,width=w-80,height=350)

        obj['title2'] = Label(obj['frame2'],text="Items Entry Details",pady=4)
        obj['title2'].config(font=("aristotelica small caps",20,"bold"),fg="white",bg=self.colors[4])
        obj['title2'].pack(side=TOP,fill=BOTH)

        #####================= Custome Treeview 
        def Custome_Treeview(fetched_data):
            obj['cc'] = ct.Customize_Treeview()
            obj['cc'].customize_treeview(window=obj['frame2'],BG=self.colors[0],WIDTH=1030,HEIGHT=250,X=5,Y=90)

            obj['cc'].Heading(heading=("S No.","Product Name","Product Type","Quantity","Rate Per Quantity","Entry Data","Entry Date By"),BG="black",FG="white",FONT=("arial",14,"bold"))

            obj['cc'].Heading_Config(IND="0",WIDTH=10,WRAP=100)
            obj['cc'].Heading_Config(IND="1",WIDTH=40,WRAP=400)
            obj['cc'].Heading_Config(IND="2",WIDTH=20,WRAP=200)
            obj['cc'].Heading_Config(IND="3",WIDTH=20,WRAP=200)
            obj['cc'].Heading_Config(IND="4",WIDTH=20,WRAP=200)
            obj['cc'].Heading_Config(IND="5",WIDTH=30,WRAP=300)
            obj['cc'].Heading_Config(IND="6",WIDTH=30,WRAP=300)            

            # fetched_data = list(fetched_data)

            for i in fetched_data:
                DF = fetched_data.index(i)
                BG = ""
                if DF%2==0:
                    BG = self.colors[4]
                else:
                    BG = self.colors[6]
                
                obj['cc'].Insert_Data(data=[fetched_data.index(i)+1,i[0],i[1],i[2],i[3],i[4],i[5]],BG=BG,FG="white",ACTIVE_BG="green",ACTIVE_FG="white")

        #####================= Select Column Label and Entry Widget
        obj['select.lbl'] = Label(obj['frame2'],text="Select Column :",font=("arial",13,"bold"),bg=self.colors[7],fg="white")
        obj['select.lbl'].place(x=10,y=45,width=150,height=30)

        select_column = ['',"Product_Type","Product_Name"]
        self.data_obj['select_column'] = StringVar()
        self.data_obj['select_column'].set(select_column[1])
        obj['select_column.e'] = ttk.OptionMenu(obj['frame2'],self.data_obj['select_column'],*select_column)
        obj['select_column.e']['menu'].config(bg=self.colors[2],fg="white",font=F,bd=0)
        obj['select_column.e'].place(x=170,y=45,width=150,height=30)

        #####================= Column Data Label and Entry Widget
        obj['column_data.lbl'] = Label(obj['frame2'],text="Column data :",font=("arial",13,"bold"),bg=self.colors[7],fg="white")
        obj['column_data.lbl'].place(x=340,y=45,width=150,height=30)

        self.data_obj['column_data'] = StringVar()
        self.data_obj['column_data'].set("")
        obj['select_column.e'] = Entry(obj['frame2'],highlightcolor="white",textvariable=self.data_obj['column_data'])
        obj['select_column.e'].config(bg="grey",fg="black",font=F,bd=0)
        obj['select_column.e'].place(x=490,y=45,width=200,height=30)
            
        ####========= [ Fetching Specified data ]
        def Select_Column_Data():
            column_name = self.data_obj['select_column'].get()
            column_data = self.data_obj['column_data'].get()
            msg.showerror("",f"{column_data}")
            if column_data=="":
                return

            fetch_data = sql.Select_Data_Using_Like(database_name=self.db['db'],Table_Name=self.db['items_table'],ID=column_name,Values=column_data)

            Custome_Treeview(fetch_data)

        #####================= Show Data In Custome Treeview
        obj['show.btn'] = Button(obj['frame2'],text="Show",font=("arial",12,"bold"))
        obj['show.btn'].config(bg="green",fg="white",activebackground="green",activeforeground="white",highlightbackground="green",bd=0,relief=FLAT)
        obj['show.btn'].config(command=lambda:Select_Column_Data())
        obj['show.btn'].place(x=710,y=45,width=100,height=30)
        
        def Upload_Data():
            ind = obj['cc'].Return
            
            if len(ind)==0:
                return
            
            self.data_obj['product_name'].set(ind[1])
            self.data_obj['product_type'].set(ind[2])
            self.data_obj['quantity'].set(ind[3])
            self.data_obj['rate_per_quantity'].set(str(ind[4]))
            pass

        #####================= Upload Data In Entry Widgets Button
        obj['upload.btn'] = Button(obj['frame2'],text="Upload Data",font=("arial",12,"bold"))
        obj['upload.btn'].config(bg="seagreen",fg="white",activebackground="seagreen",activeforeground="white",highlightbackground="seagreen",bd=0,relief=FLAT)
        obj['upload.btn'].config(command=lambda:Upload_Data())
        obj['upload.btn'].place(x=880,y=45,width=150,height=30)

        fetched_data = sql.Select_All_Data(database_name=self.db['db'],table_name=self.db['items_table'])

        Custome_Treeview(fetched_data)
    ####=============[ Add Iteams Window Function End ]=============####


    ####=============[ Menu Bar Function Start ]=============####
    def Menu_Bar_Function(self,window=None,obj={},username=None):
        self.window.title(f"Stock Management ( Develop By NightDevilPT )...                    Username :- {username}")

        logo2 = Image.open("icons/logo.png")
        logo1 = logo2.resize((100,100),Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo1)

        obj['logo'] = Label(window,bg=self.colors[0],image=logo)
        obj['logo'].image = logo
        obj['logo'].place(x=0,y=20,width=200,height=100)

        def Enter_Widget(event=None,name=None):
            obj[f'{name}_bd'].config(bg="#03e9f4")
            obj[name].config(fg="#03e9f4",highlightbackground="#03e9f4")

        def Leave_Widget(event=None,name=None):
            obj[f'{name}_bd'].config(bg=self.colors[0])
            obj[name].config(fg="white",highlightbackground=self.colors[0])

        Y = 150
        menu = ['DashBoard','Employess',"Add Items","Add Admins","Generate ID"]
        
        for i in menu:
            obj[f'{i}_bd'] = Frame(window,bg=self.colors[0])
            obj[f'{i}_bd'].place(x=5,y=Y+menu.index(i)*50,width=190,height=34)

            obj[f'{i}'] = Button(obj[f"{i}_bd"],text=i,bg=self.colors[0],fg="white",font=font.Font(family="aristotelica small caps",size=14,weight="bold"))
            obj[f'{i}'].config(activebackground="#03e9f4",activeforeground="black",bd=0,relief=FLAT,highlightbackground=self.colors[0]) 
            obj[f'{i}'].place(x=2,y=2,width=186,height=30)
            obj[f'{i}'].bind("<Enter>",lambda event=None, name=i:Enter_Widget(event=event,name=name))
            obj[f'{i}'].bind("<Leave>",lambda event=None, name=i:Leave_Widget(event=event,name=name))

        obj['DashBoard'].config(command=lambda :self.Home_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj']))
        obj['Employess'].config(command=lambda :self.Employess_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj']))
        obj['Add Items'].config(command=lambda :self.Add_Items_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj']))
        obj['Add Admins'].config(command=lambda :self.Registration_Form(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj'],bool=False))
        obj['Generate ID'].config(command=lambda :self.Generate_ID_Window(window=self.gui_obj['middle_f'],obj=self.gui_obj['middle_obj']))
    ####=============[ Menu Bar Function End ]=============####


    ####=============[ Delete Widgets Start ]=============####
    def Delete_widgets(self,obj={}):
        for i in obj:
            try:
                obj[i].destroy()
            except:
                pass
        obj.clear()
    ####=============[ Delete Widgets End ]=============####


    #=============== [ Time Update Window Start ] ================#
    def time_update(self):
        os.system("clear")
        # print()
        self.gui_obj['time_l'].config(text=(dt.now().strftime("%I:%M:%S %p\n%d %h %Y %a")))
        self.gui_obj['time_l'].after(1000,lambda:self.time_update())
    #=============== [ Time Update Window End ] ================#


    ####=============[ Take Image Window Start ]=============####
    def Take_Image_Window(self,obj={}):
        self.Delete_widgets(obj=obj)
        obj['vid'] = cv2.VideoCapture(0)
        obj['img'] = True

        obj['window'] = Toplevel()
        obj['window'].title("Employee Image Select")
        obj['window'].config(bg=self.colors[7])
        obj['window'].geometry(f"{int(5*50+180)}x{int(5*50+20)}+{int(self.Width/2-(5*50)/2)}+100")
        
        obj['img.l'] = Label(obj['window'])
        obj['img.l'].place(x=10,y=10,width=5*50,height=5*50)

        def take_image_function():
            obj['img']=False
            obj['vid'].release()
            obj['window'].destroy()
            self.Delete_widgets(obj)

            self.img_cond = True

            img = self.frame
            img2 = Image.fromarray(img)
            img3 = img2.resize((150,150),Image.ANTIALIAS)
            img4 = ImageTk.PhotoImage(img3)
            self.frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
            cv2.imwrite("employee.jpg",self.frame)

            with open("employee.jpg","rb") as f:
                self.frame_rb = f.read()
            
            os.remove("employee.jpg")

            self.gui_obj['middle_obj']['user_img'].config(image=img4)
            self.gui_obj['middle_obj']['user_img'].image=img4

        obj['ok'] = Button(obj['window'],text="Take SnapShot",bg="green",fg="white",relief=FLAT,bd=0,font=("arial",12,"bold"))
        obj['ok'].config(activebackground="green",activeforeground="white",highlightbackground=self.colors[7])
        obj['ok'].config(command=lambda:take_image_function())
        obj['ok'].place(x=5*50+20,y=10,width=150,height=30)
        
        def call_cancel():
            obj['img']=False
            obj['vid'].release()
            obj['window'].destroy()
            self.Delete_widgets(obj)

        obj['cancel'] = Button(obj['window'],text="Cancel",bg="blue",fg="white",relief=FLAT,bd=0,font=("arial",12,"bold"))
        obj['cancel'].config(activebackground="blue",activeforeground="white",highlightbackground=self.colors[7])
        obj['cancel'].config(command=lambda:call_cancel())
        obj['cancel'].place(x=5*50+20,y=50,width=150,height=30)

        def Call_CV2():
            obj['ff'],obj['frame'] = obj['vid'].read()
            
            while obj['ff']==False:
                obj['vid'].release()
                obj['vid'] = cv2.VideoCapture(0)
                obj['ff'],obj['frame'] = obj['vid'].read()

            if obj['ff']:
                obj['frame'] = cv2.flip(obj['frame'],1)
                rgb_img = cv2.cvtColor(obj['frame'],cv2.COLOR_BGR2RGB)
                self.frame = rgb_img
                img = Image.fromarray(rgb_img)
                res = img.resize((5*50,6*50),Image.ANTIALIAS)
                img2 = ImageTk.PhotoImage(res)

                obj['img.l'].config(image=img2)
                obj['img.l'].image=img2

                if obj['img']:
                    obj['img.l'].after(10,lambda:Call_CV2())

        Call_CV2()
        obj['window'].protocol("WM_DELETE_WINDOW",call_cancel)
        obj['window'].mainloop()
    ####=============[ Take Image Window Function End ]=============####


    ####=============[ Apeending Values Window Function Start ]=============####
    def Append_Values(self,values=[],data_name=[]):
        for i in data_name:
            if i=="phone_no" or i=="quantity":
                values.append(int(self.data_obj[i].get()))
            elif i=="rate_per_quantity":
                values.append(float(self.data_obj[i].get()))
            elif i=="image":
                values.append(self.frame_rb)
            elif i=="address":
                values.append(self.gui_obj['middle_obj']['address.e'].get(1.0,END)[0:-1])
                print(self.gui_obj['middle_obj']['address.e'].get(1.0,END)[0:-1])
            else:
                values.append(self.data_obj[i].get())
    ####=============[ Apeending Values Window Function End ]=============####


    ####=============[ Generate ID Card Window Function Start ]=============####
    def Generate_ID_Window(self,window=None,obj={}):
        w = self.Width-208
        h = self.Height-80
        self.img_cond = False
        F = ("arial",12,"bold")
        self.Delete_widgets(obj=obj)
        self.Delete_widgets(obj=self.data_obj)

        obj['frame'] = Frame(window,width=w-20,bg=self.colors[2])
        obj['frame'].place(x=15,y=15,width=w-30,height=h-30)

        obj['title'] = Label(obj['frame'],text="Generate ID Card",pady=4)
        obj['title'].config(font=("aristotelica small caps",20,"bold"),fg="white",bg=self.colors[4])
        obj['title'].pack(side=TOP,fill=BOTH)

        #####================= Name Label / Entry Widget
        self.data_obj['name'] = StringVar()
        self.data_obj['name'].set("None")
        obj['name.l'] = Label(obj['frame'],text="Employee Name : ",anchor=W)
        obj['name.l'].config(bg=self.colors[2],fg="white",font=F)
        obj['name.l'].place(x=30,y=60,width=150,height=30)

        obj['name.e'] = Label(obj['frame'],textvariable=self.data_obj['name'],highlightcolor="white",anchor=W,padx=2)
        obj['name.e'].config(bg=self.colors[4],fg="white",font=F)
        obj['name.e'].place(x=180,y=60,width=250,height=30)

        #####================= Name Label / Entry Widget
        self.data_obj['gender'] = StringVar()
        self.data_obj['gender'].set("None")
        obj['gender.l'] = Label(obj['frame'],text="Gender : ",anchor=W)
        obj['gender.l'].config(bg=self.colors[2],fg="white",font=F)
        obj['gender.l'].place(x=30,y=100,width=150,height=30)

        obj['gender.e'] = Label(obj['frame'],textvariable=self.data_obj['gender'],highlightcolor="white",anchor=W,padx=2)
        obj['gender.e'].config(bg=self.colors[4],fg="white",font=F)
        obj['gender.e'].place(x=180,y=100,width=250,height=30)

        #####================= Name Label / Entry Widget
        self.data_obj['dob'] = StringVar()
        self.data_obj['dob'].set("00/00/00")
        obj['dob.l'] = Label(obj['frame'],text="D.O.B : ",anchor=W)
        obj['dob.l'].config(bg=self.colors[2],fg="white",font=F)
        obj['dob.l'].place(x=30,y=140,width=150,height=30)

        obj['dob.e'] = Label(obj['frame'],textvariable=self.data_obj['dob'],highlightcolor="white",anchor=W,padx=2)
        obj['dob.e'].config(bg=self.colors[4],fg="white",font=F)
        obj['dob.e'].place(x=180,y=140,width=250,height=30)

        #####================= Name Label / Entry Widget
        self.data_obj['email'] = StringVar()
        self.data_obj['email'].set("none@gmail.com")
        obj['email.l'] = Label(obj['frame'],text="Email-ID : ",anchor=W)
        obj['email.l'].config(bg=self.colors[2],fg="white",font=F)
        obj['email.l'].place(x=30,y=180,width=150,height=30)

        obj['email.e'] = Label(obj['frame'],textvariable=self.data_obj['email'],highlightcolor="white",anchor=W,padx=2)
        obj['email.e'].config(bg=self.colors[4],fg="white",font=F)
        obj['email.e'].place(x=180,y=180,width=250,height=30)

        #####================= Name Label / Entry Widget
        self.data_obj['phone_no'] = StringVar()
        self.data_obj['phone_no'].set("9999999999")
        obj['phone_no.l'] = Label(obj['frame'],text="Phone No : ",anchor=W)
        obj['phone_no.l'].config(bg=self.colors[2],fg="white",font=F)
        obj['phone_no.l'].place(x=30,y=220,width=150,height=30)

        obj['phone_no.e'] = Label(obj['frame'],textvariable=self.data_obj['phone_no'],highlightcolor="white",anchor=W,padx=2)
        obj['phone_no.e'].config(bg=self.colors[4],fg="white",font=F)
        obj['phone_no.e'].place(x=180,y=220,width=250,height=30)

        #####================= Name Label / Entry Widget
        self.data_obj['address'] = StringVar()
        self.data_obj['address'].set("None")
        obj['address.l'] = Label(obj['frame'],text="Address :",anchor=W)
        obj['address.l'].config(bg=self.colors[2],fg="white",font=F)
        obj['address.l'].place(x=30,y=260,width=150,height=30)

        obj['address.e'] = Label(obj['frame'],textvariable=self.data_obj['address'],highlightcolor="white",anchor=W,padx=2)
        obj['address.e'].config(bg=self.colors[4],fg="white",font=F)
        obj['address.e'].place(x=180,y=260,width=250,height=30)

        #####================= Name Label / Entry Widget
        self.data_obj['job'] = StringVar()
        self.data_obj['job'].set("None")
        obj['job.l'] = Label(obj['frame'],text="Job Type :",anchor=W)
        obj['job.l'].config(bg=self.colors[2],fg="white",font=F)
        obj['job.l'].place(x=30,y=300,width=150,height=30)

        obj['job.e'] = Label(obj['frame'],textvariable=self.data_obj['job'],highlightcolor="white",anchor=W,padx=2)
        obj['job.e'].config(bg=self.colors[4],fg="white",font=F)
        obj['job.e'].place(x=180,y=300,width=250,height=30)

        #####================= User Image Label / Button Widget
        obj['user_img'] = Label(obj['frame'],bg="lightblue")
        obj['user_img'].place(x=460,y=60,width=150,height=150)

        obj['ID'] = Label(obj['frame'],bg="white")
        obj['ID'].place(x=650,y=60,width=410,height=280)

        def Generate_ID():
            if self.data_obj['name'].get()=="None":
                return
            
            ### Generating ID According Conditions
            img = None
            if self.data_obj['template'].get()=="ID1.png":
                val = [self.data_obj['name'].get(),self.data_obj['gender'].get(),self.data_obj['phone_no'].get(),self.data_obj['email'].get(),self.data_obj['img']]
                img = gid.Call_ID_Template1(val)
            else:
                val = [self.data_obj['name'].get(),self.data_obj['gender'].get(),self.data_obj['phone_no'].get(),self.data_obj['email'].get(),self.data_obj['img']]
                img = gid.Call_ID_Template2(val)
            
            ### Saving ID Cards
            img.save(f"Employees_ID_Cards/{self.data_obj['name'].get()}_{self.data_obj['phone_no'].get()}.png")

            emp2 = Image.open(f"Employees_ID_Cards/{self.data_obj['name'].get()}_{self.data_obj['phone_no'].get()}.png")
            emp1 = emp2.resize((410,280),Image.ANTIALIAS)
            emp = ImageTk.PhotoImage(emp1)

            obj['ID'].config(image=emp)
            obj['ID'].image = emp

        self.style.configure("TOptionMenu",font=("aristotelica small caps",14,"bold"))
        
        data = os.listdir("ID Templates/")
        data.remove("mask.png")
        template = ['']
        [template.append(i) for i in data]

        self.data_obj['template'] = StringVar()
        self.data_obj['template'].set(template[1])
        obj['template.e'] = ttk.OptionMenu(obj['frame'],self.data_obj['template'],*template)
        obj['template.e']['menu'].config(bg=self.colors[2],fg="white",font=F,bd=0)
        obj['template.e'].place(x=460,y=220,width=150,height=30)

        obj['generate_id.btn'] = Button(obj['frame'],text="Generate ID",bg="blue",fg="white",font=("arial",12,"bold"))
        obj['generate_id.btn'].config(activebackground="blue",activeforeground="white",highlightbackground="blue",bd=0,relief=FLAT)
        obj['generate_id.btn'].config(command=lambda:Generate_ID())
        obj['generate_id.btn'].place(x=460,y=260,width=150,height=30)

        def Clear_Label():
            self.data_obj['address'].set("None")
            self.data_obj['name'].set("None")
            self.data_obj['gender'].set("None")
            self.data_obj['dob'].set("00/00/00")
            self.data_obj['email'].set("none@gmail.com")
            self.data_obj['phone_no'].set("9999999999")
            self.data_obj['job'].set("None")
            obj['user_img'].config(image="")
            obj['ID'].config(image="")
            obj['cc'].Return = []

        obj['clear.btn'] = Button(obj['frame'],text="Clear",bg="#454545",fg="white",font=("arial",12,"bold"))
        obj['clear.btn'].config(activebackground="#454545",activeforeground="white",highlightbackground="#454545",bd=0,relief=FLAT)
        obj['clear.btn'].config(command=lambda:Clear_Label())
        obj['clear.btn'].place(x=460,y=300,width=150,height=30)
        

        ######========== [ Treeview Frame and Title ]
        obj['frame2'] = Frame(obj['frame'],bg=self.colors[7])
        obj['frame2'].place(x=25,y=360,width=w-80,height=240)

        obj['title2'] = Label(obj['frame2'],text="Employees Details",pady=4)
        obj['title2'].config(font=("aristotelica small caps",20,"bold"),fg="white",bg=self.colors[4])
        obj['title2'].pack(side=TOP,fill=BOTH)

        fetched_data = sql.Select_All_Data(database_name=self.db['db'],table_name=self.db['employe_table'])

        #####========== Creating Custom TreeView
        def Create_Treeview(fetched_data=[]):
            obj['cc'] = ct.Customize_Treeview()
            obj['cc'].customize_treeview(window=obj['frame2'],WIDTH=1030,HEIGHT=145,BG=self.colors[2],X=5,Y=85)
            
            obj['cc'].Heading(heading=("Name","Gender","D.O.B","Email-ID","Phone No","Address","Proof Type","Proof No","Job Type","Joining Date"),BG="black",FG="white",FONT=("arial",13,"bold"))
            obj['cc'].Heading_Config(IND=0,WIDTH=20,WRAP=200)
            obj['cc'].Heading_Config(IND=1,WIDTH=15,WRAP=150)
            obj['cc'].Heading_Config(IND=2,WIDTH=15,WRAP=150)
            obj['cc'].Heading_Config(IND=3,WIDTH=40,WRAP=400)
            obj['cc'].Heading_Config(IND=4,WIDTH=20,WRAP=200)
            obj['cc'].Heading_Config(IND=5,WIDTH=40,WRAP=400)
            obj['cc'].Heading_Config(IND=6,WIDTH=20,WRAP=200)
            obj['cc'].Heading_Config(IND=7,WIDTH=25,WRAP=250)
            obj['cc'].Heading_Config(IND=8,WIDTH=25,WRAP=250)
            obj['cc'].Heading_Config(IND=9,WIDTH=25,WRAP=250)

            fetched_data = list(fetched_data)

            for i in fetched_data:
                DF = fetched_data.index(i)
                BG = ""
                if DF%2==0:
                    BG = self.colors[4]
                else:
                    BG = self.colors[6]
                
                selected_data = []
                selected_data = [i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]]

                obj['cc'].Insert_Data(data=selected_data,BG=BG,FG="white",ACTIVE_BG="green",ACTIVE_FG="white")

        #####========== Uploading Selected Data In Entry Widgets Function
        def Upload_Data():
            ind = obj['cc'].Return
            if ind==None:
                return

            data = sql.Select_Specified_Data(database_name=self.db['db'],table_name=self.db['employe_table'],key_columns="Phone_No=?",key_values=(int(ind[4]),))
            data = data[0]
            
            self.data_obj['data'] = data

            self.img_cond = True
            self.frame_rb = data[0]

            img_rb = io.BytesIO(data[0])
            img = Image.open(img_rb)
            img2 = img.resize((150,150),Image.ANTIALIAS)
            self.data_obj['img'] = img
            imgtk = ImageTk.PhotoImage(img2)

            obj['user_img'].config(image=imgtk)
            obj['user_img'].image=imgtk

            lst = ['name','gender','dob','email','phone_no','address','job']

            self.data_obj['name'].set(ind[0])
            self.data_obj['gender'].set(ind[1])
            self.data_obj['dob'].set(ind[2])
            self.data_obj['email'].set(ind[3])
            self.data_obj['phone_no'].set(ind[4])
            self.data_obj['address'].set(ind[5])
            self.data_obj['job'].set(ind[8])

        obj['upload.btn'] = Button(obj['frame2'],text="Upload Data",font=("arial",12,"bold"))
        obj['upload.btn'].config(bg="seagreen",fg="white",activebackground="seagreen",activeforeground="white",highlightbackground="seagreen",bd=0,relief=FLAT)
        obj['upload.btn'].config(command=lambda:Upload_Data())
        obj['upload.btn'].place(x=880,y=45,width=150,height=30)

        obj['select.lbl'] = Label(obj['frame2'],text="Select Column :",font=("arial",13,"bold"),bg=self.colors[7],fg="white")
        obj['select.lbl'].place(x=10,y=45,width=150,height=30)

        ####========= [ Fetching Specified Data In DataBase Function ]
        def Select_Column_Data():
            os.system("clear")
            column = self.data_obj['select_column'].get()
            data = self.data_obj['column_data'].get()
            
            data = sql.Select_Data_Using_Like(database_name=self.db['db'],Table_Name=self.db['employe_table'],ID=column,Values=data)

            if data=="":
                Create_Treeview(fetched_data)
                return
            
            Create_Treeview(data)

        select_column = ['',"Name","Gender","D_O_B","Email_ID","Phone_No","Address","Proof_Type","Proof_No"]
        self.data_obj['select_column'] = StringVar()
        self.data_obj['select_column'].set(select_column[1])
        obj['select_column.e'] = ttk.OptionMenu(obj['frame2'],self.data_obj['select_column'],*select_column)
        obj['select_column.e']['menu'].config(bg=self.colors[2],fg="white",font=F,bd=0)
        obj['select_column.e'].place(x=170,y=45,width=150,height=30)

        obj['column_data.lbl'] = Label(obj['frame2'],text="Column data :",font=("arial",13,"bold"),bg=self.colors[7],fg="white")
        obj['column_data.lbl'].place(x=340,y=45,width=150,height=30)

        self.data_obj['column_data'] = StringVar()
        self.data_obj['column_data'].set("")
        obj['select_column.e'] = Entry(obj['frame2'],highlightcolor="white",textvariable=self.data_obj['column_data'])
        obj['select_column.e'].config(bg="grey",fg="black",font=F,bd=0)
        obj['select_column.e'].place(x=490,y=45,width=200,height=30)

        obj['show.btn'] = Button(obj['frame2'],text="Show",font=("arial",12,"bold"))
        obj['show.btn'].config(bg="green",fg="white",activebackground="green",activeforeground="white",highlightbackground="green",bd=0,relief=FLAT)
        obj['show.btn'].config(command=lambda:Select_Column_Data())
        obj['show.btn'].place(x=710,y=45,width=100,height=30)

        Create_Treeview(fetched_data)
    ####=============[ Generate ID Card Window Function End ]=============####


    ####=============[ DashBoard Window Function Start ]=============####
    def Home_Window_Function(self,window=None,obj={}):
        # self.window.title(f"Stock Management ( Develop By NightDevilPT )...\t\t\tUserName :- {self.db['un']}")
        self.Delete_widgets(obj=obj)
        self.Delete_widgets(obj=self.data_obj)

        clr = ["#a3c86e","#ff7460","#7ccaee","#ffd863"]
        self.data_obj['user'] = StringVar()
        self.data_obj['user'].set("0")
        self.data_obj['categories'] = StringVar()
        self.data_obj['categories'].set("0")
        self.data_obj['sale'] = StringVar()
        self.data_obj['sale'].set("0")
        
        ##============== Total User Frame
        obj['user_f'] = Frame(window,bg=clr[0],pady=10,padx=10)
        obj['user_f'].place(x=25,y=30,width=250,height=100)

        user3 = Image.open('icons/user.png')
        user2 = user3.resize((80,80),Image.ANTIALIAS)
        user = ImageTk.PhotoImage(user2)

        obj['user_img'] = Label(obj['user_f'],image=user,bg=clr[0])
        obj['user_img'].pack(side=LEFT,fill=BOTH)
        obj['user_img'].image = user

        user_data = sql.Select_All_Data(database_name=self.db['db'],table_name=self.db['employe_table'])

        obj['user_t1'] = Label(obj['user_f'],text=f"Users\n{len(user_data)}",bg=clr[0])
        obj['user_t1'].config(font=font.Font(family="Source Sans Pro Black",size=18,weight="bold"))
        obj['user_t1'].pack(side=TOP,fill=BOTH,pady=10)

        obj['user_t2'] = Label(obj['user_f'],textvariable=self.data_obj['user'],bg=clr[0])
        obj['user_t2'].config(font=font.Font(family="arial",size=18,weight="bold"))
        obj['user_t2'].pack(side=TOP,fill=BOTH)
        
        ##============== Total Productt Frame
        data = sql.Select_All_Data(database_name=self.db['db'],table_name=self.db['items_table'])

        obj['product_f'] = Frame(window,bg=clr[1],pady=10,padx=10)
        obj['product_f'].place(x=300,y=30,width=250,height=100)

        product3 = Image.open('icons/product.png')
        product2 = product3.resize((80,80),Image.ANTIALIAS)
        product = ImageTk.PhotoImage(product2)

        obj['product_img'] = Label(obj['product_f'],image=product,bg=clr[1])
        obj['product_img'].pack(side=LEFT,fill=BOTH)
        obj['product_img'].image = product

        obj['product_t1'] = Label(obj['product_f'],text=f"Product\n{len(data)}",bg=clr[1])
        obj['product_t1'].config(font=font.Font(family="Source Sans Pro Black",size=17,weight="bold"))
        obj['product_t1'].pack(side=TOP,fill=BOTH,pady=10)

        obj['product_t2'] = Label(obj['product_f'],textvariable=self.data_obj['categories'],bg=clr[1])
        obj['product_t2'].config(font=font.Font(family="arial",size=18,weight="bold"))
        obj['product_t2'].pack(side=TOP,fill=BOTH)
        

        ##============== Total Categories Frame
        product_type = []

        for i in data:
            if i[1] not in product_type:
                product_type.append(i[1])

        obj['categories_f'] = Frame(window,bg=clr[2],pady=10,padx=10)
        obj['categories_f'].place(x=575,y=30,width=250,height=100)

        categories3 = Image.open('icons/category.png')
        categories2 = categories3.resize((80,80),Image.ANTIALIAS)
        categories = ImageTk.PhotoImage(categories2)

        obj['categories_img'] = Label(obj['categories_f'],image=categories,bg=clr[2])
        obj['categories_img'].pack(side=LEFT,fill=BOTH)
        obj['categories_img'].image = categories

        obj['categories_t1'] = Label(obj['categories_f'],text=f"Categories\n{len(product_type)}",bg=clr[2])
        obj['categories_t1'].config(font=font.Font(family="Source Sans Pro Black",size=17,weight="bold"))
        obj['categories_t1'].pack(side=TOP,fill=BOTH,pady=10)

        obj['categories_t2'] = Label(obj['categories_f'],textvariable=self.data_obj['categories'],bg=clr[2])
        obj['categories_t2'].config(font=font.Font(family="arial",size=18,weight="bold"))
        obj['categories_t2'].pack(side=TOP,fill=BOTH)
        
        ##============== Total Categories Frame
        obj['amount_f'] = Frame(window,bg=clr[3],pady=10,padx=10)
        obj['amount_f'].place(x=850,y=30,width=250,height=100)

        amount3 = Image.open('icons/amount.png')
        amount2 = amount3.resize((80,80),Image.ANTIALIAS)
        amount = ImageTk.PhotoImage(amount2)

        obj['amount_img'] = Label(obj['amount_f'],image=amount,bg=clr[3])
        obj['amount_img'].pack(side=LEFT,fill=BOTH,padx=2)
        obj['amount_img'].image = amount

        obj['amount_t1'] = Label(obj['amount_f'],text="Total Sale",bg=clr[3])
        obj['amount_t1'].config(font=font.Font(family="aristotelica small caps",size=18,weight="bold"))
        obj['amount_t1'].pack(side=TOP,fill=BOTH,pady=10)

        obj['amount_t2'] = Label(obj['amount_f'],textvariable=self.data_obj['sale'],bg=clr[3])
        obj['amount_t2'].config(font=font.Font(family="arial",size=18,weight="bold"))
        obj['amount_t2'].pack(side=TOP,fill=BOTH)
    ####=============[ DashBoard Window Function End ]=============####
    

window = Tk()
main(window)
window.mainloop()