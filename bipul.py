from tkinter import messagebox
from tkinter import *
from datetime import date
import  pickle, mysql.connector


mydb = mysql.connector.connect(host= "localhost", port="3306",user= "root",password="bipul123", database="project")
mycursor = mydb.cursor()
table = 'items'
subHeadingFont = "Helvetica 10 bold" 
HeadingFont = "Helvetica 13 bold" 
item_Entry_List=[] # [[icode1,qty1],[icode2,qty2],[icode3,qty3]]

# root window
 
root = Tk()
root.title("***HBD Store***")
root.geometry('750x500')
#different screens

sale_Screen= Frame(root)
login_Screen = Frame(root) 
admin_Screen = Frame(root) 
sale_Screen.pack(fill='both', expand=1)
login_Screen.pack_forget()
admin_Screen.pack_forget()


# Default screen functions
def tologin(): 
    login_Screen.pack(fill='both', expand=1) 
    sale_Screen.pack_forget()
    entry_2.focus_set() 
    entry_1.focus_set()  # sets cursor to username field;
    

def backToSale(): 
    login_Screen.pack_forget()
    sale_Screen.pack(fill='both', expand=1) 

def tosale(): 
    sale_Screen.pack(fill='both', expand=1) 
    admin_Screen.pack_forget()


def authenticate():
    uname = entry_1.get()
    password = entry_2.get()
    if(uname == "" and password == "") :
        messagebox.showinfo("", "Blank Not allowed") 
    elif(uname == "hbd123" and password == "hbd123"):
        messagebox.showinfo("","Login Success") 
        admin_Screen.pack(fill='both', expand=1) 
        login_Screen.pack_forget()
        sale_Screen.pack_forget()
        entry_1.delete(0, END) 
        entry_2.delete(0, END)
    else :
        messagebox.showinfo("","Incorrent Username and Password")

   
# main funtions
def insertIntoFrame (t,frame): # t is the data
    Label(frame,text="Product Name",font=subHeadingFont).grid(column=0,row=0,sticky=W)
    Label(frame,text="P Code",font=subHeadingFont).grid(column=1,row=0,sticky=W)
    Label(frame,text="Price",font=subHeadingFont).grid(column=2,row=0,sticky=W)
    Label(frame,text="Stock",font=subHeadingFont).grid(column=3,row=0,sticky=W)
    
    for i in range(len(t)):
        for j in range(4):
            Label(frame, text= str(t[i][j]),padx=10).grid(column=j,row=i+1,sticky = W)

def emptyFrame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()

def fetchall(frame):  #This function fetches all records from a database table and inserts them into a given frame.
    emptyFrame(frame)
    mycursor.execute("select * from "+table) #Executes a SQL query to select all records from the specified table.
    t = mycursor.fetchall() # here "t" stores the data 
    insertIntoFrame(t,frame) # called the above function

def add_More_Entry(): #This function adds more entry fields for item code and quantity to the user interface.
    icEntry = Entry(Icode_col,width= 7)
    icEntry.pack()
    pEntry = Entry(qty_col,width= 4)
    pEntry.pack()
    itemList = []
    itemList.append(icEntry)
    itemList.append(pEntry)
    item_Entry_List.append(itemList) # here added 2 itmes in a list and added that list as an element to the other main list

def delete_Entry():
    item_Entry_List[-1][0].destroy() #removes first element of last list 
    item_Entry_List[-1][1].destroy() #removes second  element of last list 
    item_Entry_List.pop() # removes list 

def edit_text_area(textArea, inputStr): # This function edits a Text widget, either clearing it or inserting new text.
    textArea.configure(state='normal') # Makes the text area editable.
    if inputStr=="":
        textArea.delete("1.0", "end") #Clears the text area if the input string is empty.
    else:
        textArea.insert(END,inputStr) #Inserts the input string at the end of the text area.
        textArea.configure(state='disabled') # Disables editing of the text area after updating it.

def makedayfolder(foldername):#This function creates a directory with the given folder name if it doesn't already exist.
  try:
    os.makedirs(foldername)
  except OSError:
    pass
   
def Billmaker(list1): # This function generates a bill and saves it as a text file.
    orderNo = list1[0]
    data = list1[1]
    noOfItems = list1[2]
    total = list1[3]
    billNo = list1[4]

    makedayfolder("Bills/" + billNo[0:10]) # call above function
    with open("Bills/" + billNo[0:10] + "/" + billNo + ".txt", 'w+') as B:
        B.write("\t\t\t\tBILL\n")
        B.write("-------------------------------------------------\n")
        B.write(f"Bill No. : \t\t\t\t{billNo}\n")
        B.write(f"Order No. : \t\t\t\t{orderNo}\n")
        B.write("-------------------------------------------------\n")
        B.write("\t\t\tHBD Store\n")
        B.write("_________________________________________________\n")
        B.write("{:<15} {:<8} {:<8} {:<10}\n".format("Item Name", "Qty", "Price", "Total"))
        B.write("-------------------------------------------------\n")
        for i in range(noOfItems):
            item_name = str(data[i][0])
            qty = str(data[i][2])
            price = str(data[i][1])
            total_price = str(data[i][2] * data[i][1])
            B.write("{:<15} {:<8} {:<8} {:<10}\n".format(item_name, qty, price, total_price))
        B.write("_________________________________________________\n")
        B.write(f"GRAND TOTAL = {total}\n")
        B.write("_________________________________________________\n") 
   
   
   
   
def update_orderno(): #This function updates the order number for the day.
    f = open("supporting files/lastbill.txt","r+") 
    o = f.read()
    global ON, table
    Date,orderno = o.split('__') # Splits the contents into Date and orderno.
    if str(date.today()) == Date:
            ON = int(orderno) + 1
    else:
            ON = 1
    f.close()

    
class bill(): #The class bill calculates the total bill amount based on item details fetched from a database.
    def __init__(self, orderno, itemsList):  # a constructor
        data = []        #[[IName, price, Qty],...]
        T = 0            # total Bill ammount
        for item in itemsList:
            # mystr = "select IName, price from "+table+" where ICode = "+'"'+str(item[0].get())+'"'
            # print(mystr)
            mycursor.execute("select IName, price from "+table+" where ICode = "+'"'+str(item[0].get())+'"')
            k = mycursor.fetchone()
            li = list(k) #[IName, price]
            qty = int(item[1].get())
            li.append(qty)         #[IName, price, qty]
            data.append(li)
            price = k[1]
            T = T+ qty*price

        self.orderNo = orderno
        self.data = data # [itemName,price, quantity req.] 
        self.noOfItems = len(itemsList)
        self.total = T
        self.billNo = str(date.today())+"__"+str(orderno)

def checkout(orderno, item_Entry_List): #  processes a customer's order, checks if the requested quantities are available in stock, and updates the stock and other relevant records if the bill is valid.
    Bill = bill(orderno, item_Entry_List) # creates a bill object here
    edit_text_area(errorDisplay,"")
    validBill = True

    for i in range(len(item_Entry_List)):
        mycursor.execute("select stock from "+table+" where ICode ="+'"'+str(item_Entry_List[i][0].get())+'"') 
        k = mycursor.fetchone()
        s = int(k[0])               #avilable stock
        q = Bill.data[i][2]         #quantity req.
        if s < q:
            errormsg = str(Bill.data[i][0])+" is out of stock. \n Avialable Stock = "+str(s)+"\n"
            edit_text_area(errorDisplay,errormsg,) 
            validBill = False
    if validBill:
        update_orderno()
        Bill_data = [Bill.orderNo, Bill.data, Bill.noOfItems,Bill.total, Bill.billNo]
        Billmaker(Bill_data)
        G = open("supporting files/billdata.bin","ab") 
        pickle.dump(Bill_data, G)
        G.close
        global ON
        ON += 1
        billNo.config(text ="BILL NO :"+str(date.today())+"__"+str(ON))
        
        # updating last bill no inside the lastbill file ... to store it permanently.
        f = open("supporting files/lastbill.txt","w")
        f.write(Bill.billNo)
        f.close()

        # have to think about it..
        # path = Bill.billNo[0:10]+"/"+Bill.billNo+".txt" 
        # os.startfile(path, "open")

        for i in range(len(item_Entry_List)): #upating stock after bill is paid....
            IC = str(item_Entry_List[i][0].get()) #item code
            ST = int(item_Entry_List[i][1].get()) #stock
            mycursor.execute('UPDATE '+table+' SET stock = stock -'+ str(ST)+' WHERE ICode = "' +IC+'"')
            mydb.commit()

            #empting iCode and Qty entries
            for j in item_Entry_List[i]:
                j.delete(0, END)
        fetchall(table_space)


def update_price(): 
    edit_text_area(errorDisplay,'') 
    T=0
    for item in item_Entry_List:
        mycursor.execute("select price from "+table+" where ICode = "+'"'+str(item[0].get())+'"')
        k = mycursor.fetchone()
        T = T + k[0]*int(item[1].get()) 
    tatal_Label.config(text ="Total = Rs. "+str(T))



# funtions for Admin screen
def fetchonly (frame,a):
    emptyFrame(frame)
    mycursor.execute("select * from "+table+" where stock <= "+ str(a))
    t = mycursor.fetchall()
    insertIntoFrame(t,frame) 
    edit_text_area(statementarea,mycursor.statement+"\n" )


def editStock_Price():
    str1 = 'UPDATE '+table+' SET price = '+str(Price.get())+', stock=  stock +'+str(Stock1.get())+' WHERE ICode ="'+str(ICode.get())+'"'
    mycursor.execute(str1)
    mydb.commit() 
    edit_text_area(statementarea,mycursor.statement+"\n" ) 
    fetchall(frame_0_u)
    for i in [ICode,Price,Stock1]:
            i.delete(0, END)


def additem():
    str1='INSERT INTO '+table+' VALUES("'+str(iName.get())+'","'+str(iCode.get())+'",'+str(iPrice.get())+' ,'+str(stock1.get())+')'
    mycursor.execute(str1)
    mydb.commit() 
    edit_text_area(statementarea,mycursor.statement+"\n" ) 
    fetchall(frame_0_u)
    for i in [iName, iCode,iPrice,stock1]:
            i.delete(0, END)

         
def delete_item(iCode):
    command = 'DELETE FROM '+table+' WHERE ICode = "'+iCode+'"' 
    mycursor.execute(command)
    mydb.commit()
    del_iCode.delete(0,END) 
    edit_text_area(statementarea,mycursor.statement+"\n" ) 
    fetchall(frame_0_u)




# Sale screen UI
table_space = Frame(sale_Screen) 
table_space.grid(column=0,rowspan=10, padx="30") 
update_orderno()
fetchall(table_space)

add_to_cart = Frame(sale_Screen) 
add_to_cart.grid(column=1,row =0, padx="30") 
Label(add_to_cart,text="Add to cart",font=(HeadingFont)).grid(row=0,columnspan=2) 

Icode_col = Frame(add_to_cart) 
Icode_col.grid(column=0,row=1)
Label(Icode_col,text="I Code",font=subHeadingFont).pack() 

qty_col = Frame(add_to_cart) 
qty_col.grid(column=1,row=1) 
Label(qty_col,text="Qty",font=subHeadingFont).pack()
buttons_add_to_cart = Frame(sale_Screen) 
buttons_add_to_cart.grid(column=1,row=3)
Button(buttons_add_to_cart,text="Add More", command= add_More_Entry).grid(column=0,row=0) 
Button(buttons_add_to_cart,text="Delete", command= delete_Entry).grid(column=1,row=0)

Button(sale_Screen,text="Admin Screen", bg="#90EE90", command=tologin).place(x =510, y=10)

errorDisplay= Text(sale_Screen,wrap= NONE,width=35,height=3,state='disabled') 
errorDisplay.place(x=480,y = 45)

action_Frame = Frame(sale_Screen) 
action_Frame.place(x=495, y=170) 
Button(action_Frame,text="Total Amount", bg="#ADD8E6", command=update_price).pack()
Label(action_Frame).pack()
Button(action_Frame,text="Check Out",bg="#ADD8E6",command=lambda:checkout(ON,item_Entry_List)).pack( )
Label(action_Frame).pack()
tatal_Label= Label(action_Frame,text= "Total = Rs. 0",font=("bold", 12))
tatal_Label.pack()
Label(action_Frame).pack()
billNo= Label(action_Frame,text= "BILL NO : "+str(date.today())+"__"+str(ON))
billNo.pack()

for i in range(1):
    add_More_Entry()



# Login screen UI
labl_0 = Label(login_Screen, text="LOGIN", font=("Arial", 30, "bold underline"))
labl_0.place(x=325, y=75)  

labl_1 = Label(login_Screen, text="User-Name:", font=("Arial", 15, "bold"))
labl_1.place(x=150, y=150)

entry_1 = Entry(login_Screen, font=("Arial", 12))
entry_1.place(x=300, y=150)

labl_2 = Label(login_Screen, text="Password:", font=("Arial", 15, "bold"))
labl_2.place(x=150, y=200)

entry_2 = Entry(login_Screen, show="*", font=("Arial", 12))
entry_2.place(x=300, y=200)

Button(login_Screen, text='Submit', command=authenticate, width=10, bg="#ADD8E6").place(x=312.5, y=250)
Button(login_Screen, text='Go Back', command=backToSale, width=10, bg="#ADD8E6").place(x=10, y=10)

# Admin screen UI

# Frame 0_0 (Top Left Controls)
frame_0_0 = Frame(admin_Screen, pady=10, padx=30)
frame_0_0.grid(column=0, row=0, sticky=S)
Button(frame_0_0, text="Show all", bg="#FFB6C1", command=lambda: fetchall(frame_0_u)).grid(column=0, row=0)
stock = Entry(frame_0_0, width=7)
stock.grid(column=0, row=1)
Button(frame_0_0, text=">= only", bg="#FFB6C1", command=lambda: fetchonly(frame_0_u, stock.get())).grid(column=1, row=1)
Button(frame_0_0, text="remove all", bg="#FFB6C1", command=lambda: emptyFrame(frame_0_u)).grid(column=1, row=0)


# Frame 0_u (Main Display Frame)
frame_0_u = Frame(admin_Screen, pady=10, padx=5)
frame_0_u.grid(column=0, columnspan=2, row=1, sticky=N)

# Frame 1_1 (Edit Stock/Price)
frame_1_1 = Frame(admin_Screen)
frame_1_1.grid(column=0, row=2, columnspan=2, sticky=N, padx="30", pady="10")
Label(frame_1_1, text="Edit Stock/Price", font='Helvetica 11 bold').pack()
Coframe_1_1 = Frame(frame_1_1)
Coframe_1_1.pack()
Label(Coframe_1_1, text="Item Code: ").grid(column=0, row=0, sticky=W)
ICode = Entry(Coframe_1_1, width=10)
ICode.grid(column=1, row=0)
Label(Coframe_1_1, text="Stock: ").grid(column=0, row=1, sticky=W)
Stock1 = Entry(Coframe_1_1, width=10)
Stock1.insert(0, "0")
Stock1.grid(column=1, row=1)
Label(Coframe_1_1, text="Price: ").grid(column=0, row=2, sticky=W)
Price = Entry(Coframe_1_1, width=10)
Price.grid(column=1, row=2)
Button(frame_1_1, text="Update", command=editStock_Price, bg="#ADD8E6").pack()

# Frame for Remove Item
frame_1_2 = Frame(admin_Screen)
frame_1_2.grid(column=0, row=3, columnspan=2, sticky=N, padx="30", pady="20")
Label(frame_1_2, text="Remove Item", font='Helvetica 11 bold').pack()
Coframe_1_2 = Frame(frame_1_2)
Coframe_1_2.pack()
Label(Coframe_1_2, text="I Code: ").grid(column=0, row=0, sticky=W)
del_iCode = Entry(Coframe_1_2, width=7)
del_iCode.grid(column=1, row=0)
Button(Coframe_1_2, text="Delete", bg="#ADD8E6", command=lambda: delete_item(del_iCode.get())).grid(column=2, row=0)

# Frame 1_3 (Add Item)
frame_1_3 = Frame(admin_Screen)
frame_1_3.grid(column=0, row=4, columnspan=2, sticky=N, padx="30", pady="20")
Label(frame_1_3, text="Add Item", font='Helvetica 11 bold').pack()
Coframe_1_3 = Frame(frame_1_3)
Coframe_1_3.pack()
Label(Coframe_1_3, text="Item Name: ").grid(column=0, row=0, sticky=W)
iName = Entry(Coframe_1_3, width=10)
iName.grid(column=1, row=0)
Label(Coframe_1_3, text="Item Code: ").grid(column=0, row=1, sticky=W)
iCode = Entry(Coframe_1_3, width=10)
iCode.grid(column=1, row=1)
Label(Coframe_1_3, text="Stock: ").grid(column=0, row=2, sticky=W)
stock1 = Entry(Coframe_1_3, width=10)
stock1.grid(column=1, row=2)
Label(Coframe_1_3, text="Price: ").grid(column=0, row=3, sticky=W)
iPrice = Entry(Coframe_1_3, width=10)
iPrice.grid(column=1, row=3)
Button(frame_1_3, text="Add", command=additem, bg="#ADD8E6").pack()

# Frame u_3 (Statement Area)
frame_u_3 = Frame(admin_Screen, pady=10, height=30, padx=10)
frame_u_3.grid(row=5, columnspan=2)
v_sb = Scrollbar(frame_u_3)
v_sb.pack(side=RIGHT, fill=Y)
statementarea = Text(frame_u_3, wrap=NONE, width=80, height=6)
statementarea.configure(state='disabled')
statementarea.pack(side=TOP, fill=X)
v_sb.config(command=statementarea.yview)

# Sale Screen Button
Button(admin_Screen, text="Sale Screen", bg="#90EE90", command=tosale).place(x=330, y=10)

fetchall(frame_0_u)
root.mainloop()