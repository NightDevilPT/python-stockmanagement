import os,re
import threading
from tkinter import *
from tkinter import messagebox as msg
from datetime import datetime as dt
from tkinter import ttk,font
import Customize_Treeview as ct
import Scrollable_Window as sw
from PIL import Image,ImageTk
import SQL_Queries as sql
from ttkwidgets.autocomplete import AutocompleteCombobox



class Billing_System_GUI:

    Width = 1330
    Height = 720
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
    gui_obj = {
        'bill_obj':{},
        'recipt_obj':{}
    }
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
    Username = None
    data_obj = {}
    data_obj2 = {
        'all':[]
    }
    quantity = {}

    def __init__(self,window=None):
        self.window = window
        self.style = ttk.Style()
        window.geometry(f"{self.Width}x{self.Height}+10+0")
        window.config(bg=self.colors[7])
        self.window.title("Billing Management ( Develop By NightDevilPT )...")

        self.gui_obj['top_f'] = Frame(self.window,bg=self.colors[0],height=60)
        self.gui_obj['top_f'].pack(side=TOP,fill=BOTH,padx=2,pady=2)

        self.gui_obj['title_name_l'] = Label(self.gui_obj['top_f'],text="Billing System Software")
        self.gui_obj['title_name_l'].config(fg="white",font=("aristotelica small caps",45,"bold"),bg=self.colors[0])
        self.gui_obj['title_name_l'].pack(side=LEFT,padx=10,pady=9,fill=BOTH)

        self.gui_obj['time_l'] = Label(self.gui_obj['top_f'],text="00:00:00")
        self.gui_obj['time_l'].config(font=("arial",14,"bold"),bg=self.colors[0],fg="white")
        self.gui_obj['time_l'].pack(side=RIGHT,fill=BOTH,padx=10)
        self.gui_obj['time_l'].after(1000,lambda:self.time_update())

        self.gui_obj['middle_f'] = Frame(self.window,bg=self.colors[0],height=self.Height-90)
        self.gui_obj['middle_f'].pack(side=TOP,fill=BOTH,padx=2,pady=2)

        # self.Login_Form(window=window,obj=self.gui_obj['bill_obj'])
        self.Billing_Window_Function(window=self.gui_obj['middle_f'],obj=self.gui_obj['bill_obj'])


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


    ####=============[ Login Form Function Start ]=============####
    def Login_Form(self,window=None,obj={}):
        self.Delete_widgets(obj=obj)
        self.Delete_widgets(obj=self.data_obj)
        w = self.Width
        h = self.Height
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
            self.Billing_Window_Function(window=window,obj=self.gui_obj['bill_obj'])
            
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
        
        w = self.Width
        h = self.Height
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
        obj['back_btn'].config(command=lambda:self.Login_Form(window=window,obj=self.gui_obj['bill_obj']))
        obj['back_btn'].place(x=20,y=232,width=146,height=30)

        def Show_Password():
            w = self.Width
            h = self.Height
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
                    self.Login_Form(window=window,obj=self.gui_obj['bill_obj'])
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


    ####=============== [ Billing Window Start ] ================####
    def Billing_Window_Function(self,window=None,obj={}):
        self.Delete_widgets(obj=obj)
        self.Delete_widgets(obj=self.data_obj)
        self.window.title(f"Billing Management ( Develop By NightDevilPT )...                      User : {self.Username}")

        obj['bill_frame'] = Frame(window,width=self.Width-550,bg=self.colors[2])
        obj['bill_frame'].place(x=10,y=10,width=self.Width-450,height=self.Height-110)

        F = ("arial",15,"bold")

        ######===== [ Product Name and ComboBox Widget ]
        obj['product_name.l'] = Label(obj['bill_frame'],text="Product Name ",font=F,bg=self.colors[2],fg="white")
        obj['product_name.l'].place(x=20,y=20)

        data = sql.Select_All_Data(database_name=self.db['db'],table_name=self.db['items_table'])
        items = ['']
        [items.append(i[0]) for i in data]

        self.data_obj['product_name'] = StringVar()
        self.data_obj['product_name'].set(items[0])

        obj['product_name.e'] = AutocompleteCombobox(obj['bill_frame'],textvariable=self.data_obj['product_name'],completevalues=items,font=F,justify=CENTER)
        obj['product_name.e'].place(x=210,y=20,width=250,height=30)

        ######===== [ Product Type and ComboBox Widget ]
        self.data_obj['product_type'] = StringVar()
        self.data_obj['product_type'].set("")

        obj['product_type.l'] = Label(obj['bill_frame'],text="Product Type ",font=F,bg=self.colors[2],fg="white")
        obj['product_type.l'].place(x=20,y=80)

        obj['product_type.e'] = Label(obj['bill_frame'],textvariable=self.data_obj['product_type'],font=F,bg="white")
        obj['product_type.e'].place(x=210,y=80,width=250,height=30)

        ######===== [Quantity Label and Entry Widget ]
        self.data_obj['quantity'] = StringVar()
        self.data_obj['quantity'].set("")

        obj['quantity.l'] = Label(obj['bill_frame'],text="Quantity No ",font=F,bg=self.colors[2],fg="white")
        obj['quantity.l'].place(x=20,y=140)

        def Total_Price():
            if self.data_obj['product_type'].get()=="":
                return
            
            if self.data_obj['quantity'].get()=="" or self.data_obj['quantity'].get()=="0":
                self.data_obj['total'].set("0")
                return
            
            rate = float(self.data_obj['rate'].get())
            q = int(self.data_obj['quantity'].get())
            total = rate * q

            self.data_obj['total'].set(total)

        obj['quantity.e'] = Entry(obj['bill_frame'],justify=CENTER,textvariable=self.data_obj['quantity'],font=F,relief=FLAT,bd=0,highlightcolor="white")
        obj['quantity.e'].bind("<KeyRelease>",lambda event:Total_Price())
        obj['quantity.e'].place(x=210,y=140,width=250,height=30)

        ######===== [ Price Per Quantity Label and Entry Widget ]
        self.data_obj['rate'] = StringVar()
        self.data_obj['rate'].set("")

        obj['rate.l'] = Label(obj['bill_frame'],text="Price Per Quantity ",font=F,bg=self.colors[2],fg="white")
        obj['rate.l'].place(x=20,y=200)

        obj['rate.e'] = Label(obj['bill_frame'],textvariable=self.data_obj['rate'],font=F,bg="white")
        obj['rate.e'].place(x=210,y=200,width=250,height=30)

        ######===== [ Total Price Label and Entry Widget ]
        self.data_obj['total'] = StringVar()
        self.data_obj['total'].set("")

        obj['total.l'] = Label(obj['bill_frame'],text="Total Price ",font=F,bg=self.colors[2],fg="white")
        obj['total.l'].place(x=20,y=260)

        obj['total.e'] = Label(obj['bill_frame'],textvariable=self.data_obj['total'],font=F,bg="white")
        obj['total.e'].place(x=210,y=260,width=250,height=30)
        
        def Fetch_Data():
            if self.data_obj['product_name'].get()=="":
                msg.showerror("Empty Error","Product Name Field Empty..")
                return

            key_val = (self.data_obj['product_name'].get(),)
            key_col = "Product_Name=?"
            data = sql.Select_Specified_Data(database_name=self.db['db'],table_name=self.db['items_table'],select_data="Product_Name,Product_Type,Quantity,Rate_Per_Quantity",key_columns=key_col,key_values=key_val)
            data = data[0]

            if len(data)==0:
                msg.showerror("Error","This Item Is Out Of Stock...")
                return

            self.data_obj['product_type'].set(data[1])
            self.data_obj['rate'].set(data[3])
            self.data_obj['quantity'].set("")
            

        #####================= Add Item Button Widget
        obj['fetch.btn'] = Button(obj['bill_frame'],text="Fetch Item",bg="blue",fg="white",font=("arial",14,"bold"),)
        obj['fetch.btn'].config(activebackground="blue",activeforeground="white",highlightbackground=self.colors[2],relief=FLAT,bd=0)
        obj['fetch.btn'].config(command=lambda:Fetch_Data())
        obj['fetch.btn'].place(x=20,width=130,height=35,y=320)

        def Insert_Data():
            if self.data_obj['quantity'].get()=="" or self.data_obj['quantity'].get()=="0":
                msg.showerror("Error","Empty Quantity Box...")
                return
            
            if self.data_obj['product_name'].get()=="":
                msg.showerror("Error","Product Name Field is Empty...")
                return
            
            data = [self.data_obj['product_name'].get(),
                self.data_obj['product_type'].get(),
                self.data_obj['quantity'].get(),
                self.data_obj['rate'].get(),
                self.data_obj['total'].get()
            ]
            name = f"{self.data_obj['product_name'].get()}"

            if name not in self.data_obj2:
                self.data_obj2[name] = data
                self.data_obj2['all'].append(self.data_obj2[name])
            else:
                q1 = int(self.data_obj2[name][2])
                q2 = int(data[2])
                q = q1+q2
                r = float(self.data_obj['rate'].get())
                total = r*q
                self.data_obj2[name][2] = q
                self.data_obj2[name][4] = total
                
            Custome_Treeview(fetched_data=self.data_obj2['all'])
            Clear_Inputs()

        #####================= Add Item Button Widget
        obj['add.btn'] = Button(obj['bill_frame'],text="Add Item",bg="green",fg="white",font=("arial",14,"bold"),)
        obj['add.btn'].config(activebackground="green",activeforeground="white",highlightbackground=self.colors[2],relief=FLAT,bd=0)
        obj['add.btn'].config(command=lambda:Insert_Data())
        obj['add.btn'].place(x=175,width=130,height=35,y=320)

        def Clear_Inputs():
            self.data_obj['product_name'].set("")
            self.data_obj['product_type'].set("")
            self.data_obj['quantity'].set("")
            self.data_obj['rate'].set("")
            self.data_obj['total'].set("")

        #####================= Clear Item Button Widget
        obj['clear.btn'] = Button(obj['bill_frame'],text="Clear Inputs",bg="#555555",fg="white",font=("arial",14,"bold"),)
        obj['clear.btn'].config(activebackground="#555555",activeforeground="white",highlightbackground=self.colors[2],relief=FLAT,bd=0)
        obj['clear.btn'].config(command=lambda:Clear_Inputs())
        obj['clear.btn'].place(x=330,width=130,height=35,y=320)

        ####======= [ Calculate Function ]
        def Insert_No(no=""):
            equal = 0
            if no=="=":
                equal = eval(self.data_obj['text'].get())
                self.data_obj['text'].set(equal)
            elif no=="c":
                self.data_obj['text'].set("")
                self.data_obj['result'].set(f"Result : 0")
            else:
                obj['text'].insert(INSERT,no)

            self.data_obj['result'].set(f"Result : {eval(self.data_obj['text'].get())}")

        ######===== [ Calculator Frame ]
        obj['cal'] = Frame(obj['bill_frame'],bg=self.colors[4],highlightthickness=2,highlightbackground="#03e9f4",highlightcolor="#03e9f4")
        obj['cal'].place(x=500,y=15,width=350,height=345)

        obj['dis'] = Frame(obj['cal'],bg=self.colors[5],highlightthickness=2,highlightbackground="#03e9f4",highlightcolor="#03e9f4")
        obj['dis'].place(x=10,y=10,width=325,height=80)

        self.data_obj['text'] = StringVar()
        self.data_obj['text'].set("")

        obj['text'] = Entry(obj['dis'],textvariable=self.data_obj['text'],bg=self.colors[5],insertbackground="#03e9f4")
        obj['text'].config(font=("arial",17,"bold"),justify=RIGHT,fg="#03e9f4",bd=0,relief=FLAT,highlightbackground=self.colors[5],highlightcolor=self.colors[5])
        obj['text'].bind("<KeyRelease>",lambda event:Insert_No())
        obj['text'].place(x=5,y=30,width=315,height=40)

        self.data_obj['result'] = StringVar()
        self.data_obj['result'].set("Result : 0")

        obj['result.e'] = Label(obj['dis'],textvariable=self.data_obj['result'],font=F,anchor=W,fg="grey",bg=self.colors[5])
        obj['result.e'].place(x=5,y=5,width=315,height=30)

        ######===== [ Calculator Frame ]
        ###====== [ 1 Button Widget ]
        obj['1.btn'] = Button(obj['cal'],text="1",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['1.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['1.btn'].config(command=lambda:Insert_No("1"))
        obj['1.btn'].place(x=10,y=100,width=50,height=50)

        ###====== [ 2 Button Widget ]
        obj['2.btn'] = Button(obj['cal'],text="2",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['2.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['2.btn'].config(command=lambda:Insert_No("2"))
        obj['2.btn'].place(x=70,y=100,width=50,height=50)

        ###====== [ 3 Button Widget ]
        obj['3.btn'] = Button(obj['cal'],text="3",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['3.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['3.btn'].config(command=lambda:Insert_No("3"))
        obj['3.btn'].place(x=130,y=100,width=50,height=50)

        ###====== [ 4 Button Widget ]
        obj['4.btn'] = Button(obj['cal'],text="4",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['4.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['4.btn'].config(command=lambda:Insert_No("4"))
        obj['4.btn'].place(x=10,y=160,width=50,height=50)

        ###====== [ 5 Button Widget ]
        obj['5.btn'] = Button(obj['cal'],text="5",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['5.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['5.btn'].config(command=lambda:Insert_No("5"))
        obj['5.btn'].place(x=70,y=160,width=50,height=50)

        ###====== [ 6 Button Widget ]
        obj['6.btn'] = Button(obj['cal'],text="6",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['6.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['6.btn'].config(command=lambda:Insert_No("6"))
        obj['6.btn'].place(x=130,y=160,width=50,height=50)

        ###====== [ 7 Button Widget ]
        obj['7.btn'] = Button(obj['cal'],text="7",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['7.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['7.btn'].config(command=lambda:Insert_No("7"))
        obj['7.btn'].place(x=10,y=220,width=50,height=50)

        ###====== [ 8 Button Widget ]
        obj['8.btn'] = Button(obj['cal'],text="8",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['8.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['8.btn'].config(command=lambda:Insert_No("8"))
        obj['8.btn'].place(x=70,y=220,width=50,height=50)

        ###====== [ 9 Button Widget ]
        obj['9.btn'] = Button(obj['cal'],text="9",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['9.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['9.btn'].config(command=lambda:Insert_No("9"))
        obj['9.btn'].place(x=130,y=220,width=50,height=50)

        ###====== [ 0 Button Widget ]
        obj['0.btn'] = Button(obj['cal'],text="0",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['0.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['0.btn'].config(command=lambda:Insert_No("0"))
        obj['0.btn'].place(x=10,y=280,width=50,height=50)

        ###====== [ = Button Widget ]
        obj['=.btn'] = Button(obj['cal'],text="=",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['=.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['=.btn'].config(command=lambda:Insert_No("="))
        obj['=.btn'].place(x=70,y=280,width=110,height=50)

        ###====== [ / Button Widget ]
        obj['/.btn'] = Button(obj['cal'],text="/",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['/.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['/.btn'].config(command=lambda:Insert_No("/"))
        obj['/.btn'].place(x=225,y=100,width=50,height=50)

        ###====== [ - Button Widget ]
        obj['-.btn'] = Button(obj['cal'],text="-",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['-.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['-.btn'].config(command=lambda:Insert_No("-"))
        obj['-.btn'].place(x=285,y=100,width=50,height=50)

        ###====== [ * Button Widget ]
        obj['*.btn'] = Button(obj['cal'],text="*",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['*.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['*.btn'].config(command=lambda:Insert_No("*"))
        obj['*.btn'].place(x=225,y=160,width=50,height=50)

        ###====== [ + Button Widget ]
        obj['+.btn'] = Button(obj['cal'],text="+",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['+.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['+.btn'].config(command=lambda:Insert_No("+"))
        obj['+.btn'].place(x=285,y=160,width=50,height=110)

        ###====== [ % Button Widget ]
        obj['%.btn'] = Button(obj['cal'],text="%",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['%.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['%.btn'].config(command=lambda:Insert_No("%"))
        obj['%.btn'].place(x=225,y=220,width=50,height=50)

        ###====== [ Clear Button Widget ]
        obj['clear.btn'] = Button(obj['cal'],text="Clear",bg=self.colors[5],fg="#03e9f4",relief=FLAT,bd=0,font=F)
        obj['clear.btn'].config(activebackground=self.colors[5],activeforeground="#03e9f4",highlightthickness=2,highlightbackground="#03e9f4")
        obj['clear.btn'].config(command=lambda:Insert_No("c"))
        obj['clear.btn'].place(x=225,y=280,width=110,height=50)
        
        obj['treeview'] = Frame(obj['bill_frame'],width=830,height=210,bg=self.colors[7])
        obj['treeview'].place(x=20,y=380)

        def Clear_Treeview():
            self.data_obj2['all']=[]
            Custome_Treeview()

        #####================= Clear Button Widget
        obj['clear2.btn'] = Button(obj['treeview'],text="Clear Items",bg="#555555",fg="white",font=("arial",14,"bold"),)
        obj['clear2.btn'].config(activebackground="#555555",activeforeground="white",highlightbackground=self.colors[2],relief=FLAT,bd=0)
        obj['clear2.btn'].config(command=lambda:Clear_Treeview())
        obj['clear2.btn'].place(x=620,width=200,height=35,y=170)

        #####================= Delete Button Widget
        obj['delete.btn'] = Button(obj['treeview'],text="Remove Item",bg="red",fg="white",font=("arial",14,"bold"),)
        obj['delete.btn'].config(activebackground="red",activeforeground="white",highlightbackground=self.colors[2],relief=FLAT,bd=0)
        obj['delete.btn'].config(command=lambda:Custome_Treeview(fetched_data=[]))
        obj['delete.btn'].place(x=310,width=200,height=35,y=170)

        #####================= Generate Total Bill Button Widget
        obj['generatebill.btn'] = Button(obj['treeview'],text="Generate Bill",bg="green",fg="white",font=("arial",14,"bold"),)
        obj['generatebill.btn'].config(activebackground="green",activeforeground="white",highlightbackground=self.colors[2],relief=FLAT,bd=0)
        obj['generatebill.btn'].config(command=lambda:Custome_Treeview(fetched_data=[]))
        obj['generatebill.btn'].place(x=10,width=200,height=35,y=170)

        #####================= Custome Treeview 
        def Custome_Treeview(fetched_data=[]):
            obj['cc'] = ct.Customize_Treeview()
            obj['cc'].customize_treeview(window=obj['treeview'],BG=self.colors[0],WIDTH=820,HEIGHT=160,X=5,Y=5)

            obj['cc'].Heading(heading=("Product Name","Product Type","Quantity","Rate Per Quantity","Total Price"),BG="black",FG="white",FONT=("arial",14,"bold"))

            obj['cc'].Heading_Config(IND="0",WIDTH=40,WRAP=400)
            obj['cc'].Heading_Config(IND="1",WIDTH=20,WRAP=200)
            obj['cc'].Heading_Config(IND="2",WIDTH=20,WRAP=200)
            obj['cc'].Heading_Config(IND="3",WIDTH=20,WRAP=200)
            obj['cc'].Heading_Config(IND="4",WIDTH=20,WRAP=200)

            if len(fetched_data)==0:
                return
            
            for i in fetched_data:
                BG=""
                if fetched_data.index(i)%2==0:
                    BG="#353535"
                else:
                    BG="#555555"
                obj['cc'].Insert_Data(data=tuple(i),BG=BG)

        Custome_Treeview()
    ####=============== [ Billing Window End ] ================####


window = Tk()
Billing_System_GUI(window)
window.mainloop()