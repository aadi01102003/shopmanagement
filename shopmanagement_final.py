from tkinter import ttk
from tkinter import *
from tkcalendar import DateEntry
from tkinter import messagebox
import mysql.connector as db
import tkinter.scrolledtext as st
from datetime import *

def connection():
    connectObj=db.connect(host='localhost',user='root',password='root123',database="shopmanagement",auth_plugin='mysql_native_password')
    cur = connectObj.cursor()
    sql = '''
    create table if not exists sellings (
        date char(255),
        product char(255),
        price int,
        quantity int,
        total int
        )
    '''
    cur.execute(sql)
    connectObj.commit()   

connection()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#=============================================================================Billing Tab Functions===========================================================================================
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
id_of_user=False
def billing():
    row_value=bill.focus()
    value=bill.item(row_value)
    content=value['values']
    if product.get()!='':
        bill.insert('',END,values=(len(bill.get_children())+1,product.get(),quantity.get(),price.get()))
    else:
        messagebox.showerror('No value', 'No item selected')
    total()
    clear()



def print_bill():
    connection_Obj=db.connect(host='localhost',user='root',password='root123',database="shopmanagement",auth_plugin='mysql_native_password')
    cur=connection_Obj.cursor()
    cur.execute("insert into orders(total,ID) values(%s,'%s')"%(total(),id_of_user))
    connection_Obj.commit()
    connection_Obj.close()
    bill_file=open('Bill.txt','w')
    time=datetime.now()
    bill_file.write('\t\t\t\t\t\t\t||Shop Management Project ||')
    bill_file.write('\n__Date:%s_________________________________________________________________________Time:%s:%s______________________________________\n'%(date.today(),time.hour,time.minute))
    bill_file.write('\nSno\t\tProducts\t\t\tPrice\t\t\t\tQTY\t\t\t\tTotal')
    bill_file.write('\n====================================================================================================================================')
    bill_file.write('\n')
    for values in bill.get_children():
        print(bill.item(values)["values"])
        for  value in bill.item(values)["values"]:
            bill_file.write(str(value)+'\t\t\t\t')
        bill_file.write('\n')
    bill_file.write('SGST=2.5%\nCGST=2.5%')
    bill_file.write('\nTotal:%s'%(total()*1.05))
    import os
    os.startfile('Bill.txt','print')
        
def delete_1():
    if len(bill.selection())==0:
        messagebox.showerror('No value', 'No item selected')
    else:
        selected_item=bill.selection()[0]
        bill.delete(selected_item)
        total()
        clear()

def data_display():
    connection_Obj=db.connect(host='localhost',user='root',password='root123',database="shopmanagement",auth_plugin='mysql_native_password')
    cur=connection_Obj.cursor()
    cur.execute('select * from sellings')
    result=cur.fetchall()
    if len(result)!=0:
        for item in item_table.get_children():
            item_table.delete(item)
        for i in result:
            item_table.insert('',END,values=i)

    connection_Obj.commit()
    connection_Obj.close()
    
def get_values_2(ev):
    row_value=bill.focus()
    value=bill.item(row_value)
    content=value['values']
    product.set(content[1])
    price.set(content[3])
    quantity.set(content[2])

def get_values(ev):
    row_value=item_table.focus()
    value=item_table.item(row_value)
    content=value['values']
    product.set(content[1])
    price.set(content[2])
    quantity.set(content[3])
    data_display_1()
    
def total():
    bill_amt=0
    for item in bill.get_children():
        bill_amt=bill_amt+(bill.item(item)["values"][2]*bill.item(item)["values"][3])
    total_bill.set('Total:%s'%bill_amt)
    return bill_amt
        
def clear():
    product.set('')
    price.set(0)
    quantity.set(0)

def update_1():
    if len(bill.selection())==0:
        messagebox.showerror('No value', 'No item selected')
    else:
        selected_item=bill.selection()[0]
        bill.item(selected_item, text="blub",values=(1,product.get(),quantity.get(),price.get()*quantity.get()))
        total()
        clear()
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#==============================================================================Stock Tab Functions===========================================================================================    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_values_1(ev):
    row_value=item_table_1.focus()
    value=item_table_1.item(row_value)
    content=value['values']
    product_1.set(content[1])
    price_1.set(content[2])
    quantity_1.set(content[3])
    data_display()
    
def data_display_1():
    connection_Obj=db.connect(host='localhost',user='root',password='root123',database="shopmanagement",auth_plugin='mysql_native_password')
    cur=connection_Obj.cursor()
    cur.execute('select * from sellings')
    result=cur.fetchall()
    if len(result)!=0:
        for item in item_table_1.get_children():
            item_table_1.delete(item)
        for i in result:
            print(i)
            item_table_1.insert('',END,values=i)

    connection_Obj.commit()
    connection_Obj.close()

def delete():
    connection_Obj=db.connect(host='localhost',user='root',password='root123',database="shopmanagement",auth_plugin='mysql_native_password')
    cur=connection_Obj.cursor()
    row_value=item_table_1.focus()
    value=item_table_1.item(row_value)
    content=value['values']
    if len(content)!=0:
        cur.execute('delete from sellings where sno=%s'%(content[0]))
    else:
        messagebox.showerror('No value', 'No item selected')
    connection_Obj.commit()
    connection_Obj.close()
    data_display_1()
    data_display()
    clear_1()
    
def update():
    connection_Obj=db.connect(host='localhost',user='root',password='root123',database="shopmanagement",auth_plugin='mysql_native_password')
    cur=connection_Obj.cursor()
    cur.execute('select * from sellings')
    result=cur.fetchall()
    row_value=item_table_1.focus()
    value=item_table_1.item(row_value)
    content=value['values']
    print(content)
    if len(content)!=0:
        cur.execute("update sellings set product=%s,quantity=%s,price=%s where sno=%s",(product_1.get(),quantity_1.get(),price_1.get(),content[0]))
    else:
        messagebox.showerror('No value', 'No item selected')
    connection_Obj.commit()
    connection_Obj.close()
    data_display_1()
    data_display()
    clear_1()
    
def clear_1():
    product_1.set('')
    price_1.set(0)
    quantity_1.set(0)
    data_display_1()
    data_display()
    
def add():
    connection_Obj=db.connect(host='localhost',user='root',password='root123',database="shopmanagement",auth_plugin='mysql_native_password')
    cur=connection_Obj.cursor()
    cur.execute('select * from sellings')
    result=cur.fetchall()
    cur.execute("insert into sellings values(%s,'%s',%s,%s)"%(len(result)+1,product_1.get(),price_1.get(),quantity_1.get()))
    connection_Obj.commit()
    connection_Obj.close()
    data_display_1()
    clear_1()
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#===========================================================================Employee Tab Functions===========================================================================================
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def data_display_2():
    connection_Obj=db.connect(host='localhost',user='root',password='root123',database="shopmanagement",auth_plugin='mysql_native_password')
    cur=connection_Obj.cursor()
    cur.execute('select * from employees')
    result=cur.fetchall()
    if len(result)!=0:
        for item in item_table_2.get_children():
            item_table_2.delete(item)
        for i in result:
            print(i)
            item_table_2.insert('',END,values=i)

    connection_Obj.commit()
    connection_Obj.close()

def get_values_3(ev):
    row_value=item_table_2.focus()
    value=item_table_2.item(row_value)
    content=value['values']
    ID.set(content[0])
    name.set(content[1])
    age.set(content[2])
    salary.set(content[3])
    no_of_holidays.set(content[4])
    phone_number.set(content[5])
    data_display()
    
def clear_2():
    ID.set('')
    name.set('')
    phone_number.set('')
    age.set(0)
    salary.set(0)
    no_of_holidays.set(0)
    data_display_1()
    data_display()
    
def update_2():
    connection_Obj=db.connect(host='localhost',user='root',password='root123',database="shopmanagement",auth_plugin='mysql_native_password')
    cur=connection_Obj.cursor()
    cur.execute('select * from employees')
    result=cur.fetchall()
    row_value=item_table_2.focus()
    value=item_table_2.item(row_value)
    content=value['values']
    if len(content)!=0:
        cur.execute("update employees set Name='%s',Salary=%s,Age=%s,No_of_Holidays_this_Month=%s,Phone_Number='%s' where ID='%s'"%(name.get(),salary.get(),age.get(),no_of_holidays.get(),phone_number.get(),ID.get()))
    else:
        messagebox.showerror('No value', 'No item selected')
    connection_Obj.commit()
    connection_Obj.close()
    data_display_2()
    clear_2()
    
def delete_2():
    connection_Obj=db.connect(host='localhost',user='root',password='root123',database="shopmanagement",auth_plugin='mysql_native_password')
    cur=connection_Obj.cursor()
    row_value=item_table_2.focus()
    value=item_table_2.item(row_value)
    content=value['values']
    if len(content)!=0:
        cur.execute('delete from employees where ID="%s"'%(content[0]))
    else:
        messagebox.showerror('No value', 'No item selected')
    connection_Obj.commit()
    connection_Obj.close()
    data_display_2()
    clear_2()
    
def ID_generate():
    connection_Obj=db.connect(host='localhost',user='root',password='root123',database="shopmanagement",auth_plugin='mysql_native_password')
    cur=connection_Obj.cursor()
    cur.execute('select * from employees')
    result=cur.fetchall()
    import random
    lst=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    p1=random.choice(lst)
    p2=random.choice(lst)
    p3=random.choice(lst)
    p4=random.choice(lst)
    IDgen=p1+p2+p3+p4
    for i in result:
        if i[0]!=IDgen:
            primary=False
            continue
        else:
            primary=True
            break
    if primary==False:
        return IDgen
    elif primary==True:
        ID_generate()

def add_1():
    connection_Obj=db.connect(host='localhost',user='root',password='root123',database="shopmanagement",auth_plugin='mysql_native_password')
    cur=connection_Obj.cursor()
    cur.execute('select * from employees')
    result=cur.fetchall()
    primary=False
    for i in result:
        if len(ID.get())==0:
            primary=True
            break
        if i[0]!=ID.get():
            primary=False
            continue
        elif i[0]==ID.get():
            primary=True
            break 
    if primary==False:
        cur.execute("insert into employees values('%s','%s',%s,%s,%s,'%s')"%(ID.get(),name.get(),age.get(),salary.get(),no_of_holidays.get(),phone_number.get()))
    elif primary==True:
        cur.execute("insert into employees values('%s','%s',%s,%s,%s,'%s')"%(ID_generate(),name.get(),age.get(),salary.get(),no_of_holidays.get(),phone_number.get()))
    connection_Obj.commit()
    connection_Obj.close()
    data_display_2()
    clear_2()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#==============================================================================Tkinter tab creation===========================================================================================
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def manager():
    login_window.destroy()
    global window
    window=Tk()
    window.title("Shop Management Project")
    window.geometry('1350x700+0+0')
    
    tabs=ttk.Notebook(window)
    root=ttk.Frame(tabs)
    root2=ttk.Frame(tabs)
    root3=ttk.Frame(tabs)
    tabs.add(root,text='Sell')
    tabs.add(root2,text='Stock')
    tabs.add(root3,text='Employees')
    tabs.pack(expand=1,fill ="both")

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #==============================================================================Billing Tab Tkinter===========================================================================================
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    global sno,product,quantity,price,total_bill
    sno=IntVar()
    product=StringVar()
    quantity=IntVar()
    price=IntVar()
    total_bill=StringVar()

    frame1=ttk.Frame(root,relief=RIDGE)
    frame1.place(x=15,y=70,width=340,height=560)

    label1=Label(frame1,text='BILL',font=('verdana',20,'bold'))
    label1.grid(row=0,columnspan=2,pady=2,padx=4)

    global item_entry,price_entry,quantity_entry

    label_item=Label(frame1,text='Item',font=('verdana',12))
    label_item.grid(row=1,column=0,padx=10,pady=20)
    item_entry=Entry(frame1,textvariable=product,font=('verdana',12))
    item_entry.grid(row=1,column=1,padx=10,pady=20)

    label_quantity=Label(frame1,text='Quantity',font=('verdana',12))
    label_quantity.grid(row=2,column=0,padx=10,pady=20)
    quantity_entry=Entry(frame1,textvariable=quantity,font=('verdana',12))
    quantity_entry.grid(row=2,column=1,padx=10,pady=20)

    label_price=Label(frame1,text='Price',font=('verdana',12))
    label_price.grid(row=3,column=0,padx=10,pady=20)
    price_entry=Entry(frame1,textvariable=price,font=('verdana',12))
    price_entry.grid(row=3,column=1,padx=10,pady=20)

    frame2=ttk.Frame(root,relief=RIDGE)
    frame2.place(x=360,y=70,width=500,height=560)

    table_frame=ttk.Frame(frame2,relief=RIDGE)
    table_frame.place(x=10,y=50,height=500,width=480)

    scrollbar_x=Scrollbar(table_frame,orient=HORIZONTAL)
    scrollbar_y=Scrollbar(table_frame,orient=VERTICAL)
    global item_table
    item_table=ttk.Treeview(table_frame,columns=('Sno','Product','Price','Quantity'),xscrollcommand=scrollbar_x.set,yscrollcommand=scrollbar_y.set)
    scrollbar_x.pack(side=BOTTOM,fill=X)
    scrollbar_y.pack(side=RIGHT,fill=Y)
    scrollbar_x.config(command=item_table.xview)
    scrollbar_y.config(command=item_table.yview)
    item_table.heading('Sno',text='Sno')
    item_table.heading('Product',text='Product')
    item_table.heading('Price',text='Price')
    item_table.heading('Quantity',text='Quantity')
    item_table['show']='headings'
    item_table.column('Sno',width=120)
    item_table.column('Product',width=120)
    item_table.column('Price',width=120)
    item_table.column('Quantity',width=120)
    item_table.pack(fill=BOTH,expand=1)
    item_table.bind('<ButtonRelease-1>',get_values)
    data_display()

    frame3=ttk.Frame(root,relief=RIDGE)
    frame3.place(x=865,y=70,width=470,height=560)
    bill_frame=ttk.Frame(frame3,relief=RIDGE)
    bill_frame.place(x=10,y=50,height=500,width=460)
    scrollbar_x_bill=Scrollbar(bill_frame,orient=HORIZONTAL)
    scrollbar_y_bill=Scrollbar(bill_frame,orient=VERTICAL)
    global bill
    bill=ttk.Treeview(bill_frame,columns=('Sno','Product','Quantity','Price'),xscrollcommand=scrollbar_x_bill.set,yscrollcommand=scrollbar_y_bill.set)
    scrollbar_x_bill.pack(side=BOTTOM,fill=X)
    scrollbar_y_bill.pack(side=RIGHT,fill=Y)
    scrollbar_x_bill.config(command=bill.xview)
    scrollbar_y_bill.config(command=bill.yview)
    bill.heading('Sno',text='Sno')
    bill.heading('Product',text='Product')
    bill.heading('Price',text='Price')
    bill.heading('Quantity',text='Quantity')
    bill['show']='headings'
    bill.column('Sno',width=100)
    bill.column('Product',width=100)
    bill.column('Price',width=120)
    bill.column('Quantity',width=100)
    bill.pack(fill=BOTH,expand=1)
    bill.bind('<ButtonRelease-1>',get_values_2)

    frame1_button=ttk.Frame(frame1,relief=RIDGE)
    frame1_button.place(x=10,y=350)

    bill_button=ttk.Button(frame1_button,text='Bill',width=18,command=billing)
    bill_button.grid(row=0,column=0,pady=10,padx=10)

    clear_button=ttk.Button(frame1_button,text='Clear',width=18,command=clear)
    clear_button.grid(row=1,column=1,pady=10,padx=10)

    frame2_button=ttk.Frame(frame3,relief=RIDGE)
    frame2_button.place(x=0,y=0,width=470,height=50)

    update_button_1=ttk.Button(frame2_button,text='Update',width=18,command=update_1)
    update_button_1.grid(row=0,column=0,pady=10,padx=10)

    delete_button_1=ttk.Button(frame2_button,text='Delete',width=18,command=delete_1)
    delete_button_1.grid(row=0,column=1,pady=10,padx=10)

    print_button_1=ttk.Button(frame1_button,text='Print',width=18,command=print_bill)
    print_button_1.grid(row=1,column=0,pady=10,padx=10)
    
    sign_out_button=Button(root,text='Sign Out',width=18,command=destroy)
    sign_out_button.place(x=15,y=30)

    total_label=Label(root,textvariable=total_bill,font=('verdana',16))
    total_label.place(x=1200,y=30)
                      

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #==============================================================================Stock Tab Tkinter===========================================================================================
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    global sno_1,product_1,quantity_1,price_1
    sno_1=IntVar()
    product_1=StringVar()
    quantity_1=IntVar()
    price_1=IntVar()

    frame1_1=ttk.Frame(root2,relief=RIDGE)
    frame1_1.place(x=20,y=70,width=350,height=560)

    label1=Label(frame1_1,text='Manage',font=('verdana',20,'bold'))
    label1.grid(row=0,columnspan=2,pady=2,padx=4)

    global item_entry_1,quantity_entry_1,price_entry_1
    
    label_item=Label(frame1_1,text='Item',font=('verdana',12))
    label_item.grid(row=1,column=0,padx=10,pady=20)
    item_entry_1=Entry(frame1_1,textvariable=product_1,font=('verdana',12))
    item_entry_1.grid(row=1,column=1,padx=10,pady=20)

    label_quantity=Label(frame1_1,text='Quantity',font=('verdana',12))
    label_quantity.grid(row=2,column=0,padx=10,pady=20)
    quantity_entry_1=Entry(frame1_1,textvariable=quantity_1,font=('verdana',12))
    quantity_entry_1.grid(row=2,column=1,padx=10,pady=20)

    label_price=Label(frame1_1,text='Price',font=('verdana',12))
    label_price.grid(row=3,column=0,padx=10,pady=20)
    price_entry_1=Entry(frame1_1,textvariable=price_1,font=('verdana',12))
    price_entry_1.grid(row=3,column=1,padx=10,pady=20)

    frame2_1=ttk.Frame(root2,relief=RIDGE)
    frame2_1.place(x=400,y=70,width=720,height=560)

    table_frame_1=ttk.Frame(frame2_1,relief=RIDGE)
    table_frame_1.place(x=10,y=50,height=500,width=700)

    scrollbar_x_1=Scrollbar(table_frame_1,orient=HORIZONTAL)
    scrollbar_y_1=Scrollbar(table_frame_1,orient=VERTICAL)
    global item_table_1
    item_table_1=ttk.Treeview(table_frame_1,columns=('Sno','Product','Price','Quantity'),xscrollcommand=scrollbar_x_1.set,yscrollcommand=scrollbar_y_1.set)
    scrollbar_x_1.pack(side=BOTTOM,fill=X)
    scrollbar_y_1.pack(side=RIGHT,fill=Y)
    scrollbar_x_1.config(command=item_table_1.xview)
    scrollbar_y_1.config(command=item_table_1.yview)
    item_table_1.heading('Sno',text='Sno')
    item_table_1.heading('Product',text='Product')
    item_table_1.heading('Price',text='Price')
    item_table_1.heading('Quantity',text='Quantity')
    item_table_1['show']='headings'
    item_table_1.column('Sno',width=120)
    item_table_1.column('Product',width=120)
    item_table_1.column('Price',width=120)
    item_table_1.column('Quantity',width=120)
    item_table_1.pack(fill=BOTH,expand=1)
    item_table_1.bind('<ButtonRelease-1>',get_values_1)
    data_display_1()

    frame1_1_button=ttk.Frame(frame1_1,relief=RIDGE)
    frame1_1_button.place(x=10,y=350)

    add_button=ttk.Button(frame1_1_button,text='add',width=18,command=add)
    add_button.grid(row=0,column=0,pady=10,padx=10)

    update_button=ttk.Button(frame1_1_button,text='Update',width=18,command=update)
    update_button.grid(row=0,column=1,pady=10,padx=10)

    delete_button=ttk.Button(frame1_1_button,text='Delete',width=18,command=delete)
    delete_button.grid(row=1,column=0,pady=10,padx=10)

    clear_button_1=ttk.Button(frame1_1_button,text='Clear',width=18,command=clear_1)
    clear_button_1.grid(row=1,column=1,pady=10,padx=10)

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #==============================================================================Employee Tab Tkinter===========================================================================================
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    global ID,name,salary,age,no_of_holidays,phone_number
    ID=StringVar()
    name=StringVar()
    salary=IntVar()
    age=IntVar()
    no_of_holidays=IntVar()
    phone_number=StringVar()


    frame1_2=ttk.Frame(root3,relief=RIDGE)
    frame1_2.place(x=30,y=70,width=500,height=600)

    label2=Label(frame1_2,text='Employees',font=('verdana',20,'bold'))
    label2.grid(row=0,columnspan=2,pady=2,padx=4)

    global name_entry,age_entry,salary_entry,phone_entry,phone_holiday,name_entry

    label_ID=Label(frame1_2,text='ID',font=('verdana',12))
    label_ID.grid(row=1,column=0,padx=10,pady=20)
    name_entry=Entry(frame1_2,textvariable=ID,font=('verdana',12))
    name_entry.grid(row=1,column=1,padx=10,pady=20)

    label_name=Label(frame1_2,text='Name',font=('verdana',12))
    label_name.grid(row=2,column=0,padx=10,pady=20)
    name_entry=Entry(frame1_2,textvariable=name,font=('verdana',12))
    name_entry.grid(row=2,column=1,padx=10,pady=20)

    label_age=Label(frame1_2,text='Age',font=('verdana',12))
    label_age.grid(row=3,column=0,padx=10,pady=20)
    age_entry=Entry(frame1_2,textvariable=age,font=('verdana',12))
    age_entry.grid(row=3,column=1,padx=10,pady=20)

    label_salary=Label(frame1_2,text='Salary',font=('verdana',12))
    label_salary.grid(row=4,column=0,padx=10,pady=20)
    salary_entry=Entry(frame1_2,textvariable=salary,font=('verdana',12))
    salary_entry.grid(row=4,column=1,padx=10,pady=20)

    label_phone=Label(frame1_2,text='Phone Number',font=('verdana',12))
    label_phone.grid(row=5,column=0,padx=10,pady=20)
    phone_entry=Entry(frame1_2,textvariable=phone_number,font=('verdana',12))
    phone_entry.grid(row=5,column=1,padx=10,pady=20)

    label_holiday=Label(frame1_2,text='No of Holidays',font=('verdana',12))
    label_holiday.grid(row=6,column=0,padx=10,pady=20)
    phone_holiday=Entry(frame1_2,textvariable=no_of_holidays,font=('verdana',12))
    phone_holiday.grid(row=6,column=1,padx=10,pady=20)

    frame2_2=ttk.Frame(root3,relief=RIDGE)
    frame2_2.place(x=400,y=70,width=720,height=600)

    table_frame_2=ttk.Frame(frame2_2,relief=RIDGE)
    table_frame_2.place(x=10,y=70,height=500,width=700)

    scrollbar_x_2=Scrollbar(table_frame_2,orient=HORIZONTAL)
    scrollbar_y_2=Scrollbar(table_frame_2,orient=VERTICAL)
    global item_table_2
    item_table_2=ttk.Treeview(table_frame_2,columns=('ID','Name','Age','Salary','Number of Holidays','Phone Number'),xscrollcommand=scrollbar_x_2.set,yscrollcommand=scrollbar_y_2.set)
    scrollbar_x_2.pack(side=BOTTOM,fill=X)
    scrollbar_y_2.pack(side=RIGHT,fill=Y)
    scrollbar_x_2.config(command=item_table_2.xview)
    scrollbar_y_2.config(command=item_table_2.yview)
    item_table_2.heading('ID',text='ID')
    item_table_2.heading('Name',text='Name')
    item_table_2.heading('Age',text='Age')
    item_table_2.heading('Salary',text='Salary')
    item_table_2.heading('Number of Holidays',text='Number of Holidays')
    item_table_2.heading('Phone Number',text='Phone Number')
    item_table_2['show']='headings'
    item_table_2.column('ID',width=85)
    item_table_2.column('Name',width=85)
    item_table_2.column('Age',width=85)
    item_table_2.column('Salary',width=90)
    item_table_2.column('Number of Holidays',width=85)
    item_table_2.column('Phone Number',width=100)
    item_table_2.pack(fill=BOTH,expand=1)
    item_table_2.bind('<ButtonRelease-1>',get_values_3)
    data_display_2()

    frame1_2_button=ttk.Frame(frame1_2,relief=RIDGE)
    frame1_2_button.place(x=15,y=450)

    add_button_1=ttk.Button(frame1_2_button,text='add',width=18,command=add_1)
    add_button_1.grid(row=0,column=0,pady=10,padx=10)

    name_button=ttk.Button(frame1_2_button,text='Update',width=18,command=update_2)
    name_button.grid(row=0,column=1,pady=10,padx=10)

    delete_button_2=ttk.Button(frame1_2_button,text='Delete',width=18,command=delete_2)
    delete_button_2.grid(row=1,column=0,pady=10,padx=10)

    clear_button_2=ttk.Button(frame1_2_button,text='Clear',width=18,command=clear_2)
    clear_button_2.grid(row=1,column=1,pady=10,padx=10)

    total_label=Label(root,textvariable=total_bill,font=('verdana',16))
    total_label.place(x=1200,y=30)

    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #/\/\/\/\/\/\//\/\/\/\/\/\/\/\//\\//\/\/\/\/\/\/\\//\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\\//\/\/\/\/\/\/\/\/\/\/\/\\//\/\/\/\/\/\/\/\/\
    #==============================================================================================================================================================================================
    #\/\/\/\//\/\\/\//\/\\//\/\/\/\/\/\/\/\/\/\\//\\//\/\/\/\/\/\\/\//\\/\//\\//\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\\/\/\/\/\/\/\/\/\/\/\\/\/\/\/\/\/\/\/\/\/\/\
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    window.mainloop()

def employee():
    global window
    login_window.destroy()
    window=Tk()
    window.title("Shop Management Project")
    window.geometry('1350x700+0+0')
    
    tabs=ttk.Notebook(window)
    root=ttk.Frame(tabs)
    root2=ttk.Frame(tabs)
    tabs.add(root,text='Sell')
    tabs.add(root2,text='Stock')
    tabs.pack(expand=1,fill ="both")

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #==============================================================================Billing Tab Tkinter===========================================================================================
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    global sno,product,quantity,price,total_bill
    sno=IntVar()
    product=StringVar()
    quantity=IntVar()
    price=IntVar()
    total_bill=StringVar()

    frame1=ttk.Frame(root,relief=RIDGE)
    frame1.place(x=15,y=70,width=340,height=560)

    label1=Label(frame1,text='BILL',font=('verdana',20,'bold'))
    label1.grid(row=0,columnspan=2,pady=2,padx=4)

    global item_entry,price_entry,quantity_entry

    label_item=Label(frame1,text='Item',font=('verdana',12))
    label_item.grid(row=1,column=0,padx=10,pady=20)
    item_entry=Entry(frame1,textvariable=product,font=('verdana',12))
    item_entry.grid(row=1,column=1,padx=10,pady=20)

    label_quantity=Label(frame1,text='Quantity',font=('verdana',12))
    label_quantity.grid(row=2,column=0,padx=10,pady=20)
    quantity_entry=Entry(frame1,textvariable=quantity,font=('verdana',12))
    quantity_entry.grid(row=2,column=1,padx=10,pady=20)

    label_price=Label(frame1,text='Price',font=('verdana',12))
    label_price.grid(row=3,column=0,padx=10,pady=20)
    price_entry=Entry(frame1,textvariable=price,font=('verdana',12))
    price_entry.grid(row=3,column=1,padx=10,pady=20)

    frame2=ttk.Frame(root,relief=RIDGE)
    frame2.place(x=360,y=70,width=500,height=560)

    table_frame=ttk.Frame(frame2,relief=RIDGE)
    table_frame.place(x=10,y=50,height=500,width=480)

    scrollbar_x=Scrollbar(table_frame,orient=HORIZONTAL)
    scrollbar_y=Scrollbar(table_frame,orient=VERTICAL)
    global item_table
    item_table=ttk.Treeview(table_frame,columns=('Sno','Product','Price','Quantity'),xscrollcommand=scrollbar_x.set,yscrollcommand=scrollbar_y.set)
    scrollbar_x.pack(side=BOTTOM,fill=X)
    scrollbar_y.pack(side=RIGHT,fill=Y)
    scrollbar_x.config(command=item_table.xview)
    scrollbar_y.config(command=item_table.yview)
    item_table.heading('Sno',text='Sno')
    item_table.heading('Product',text='Product')
    item_table.heading('Price',text='Price')
    item_table.heading('Quantity',text='Quantity')
    item_table['show']='headings'
    item_table.column('Sno',width=120)
    item_table.column('Product',width=120)
    item_table.column('Price',width=120)
    item_table.column('Quantity',width=120)
    item_table.pack(fill=BOTH,expand=1)
    item_table.bind('<ButtonRelease-1>',get_values)
    data_display()

    frame3=ttk.Frame(root,relief=RIDGE)
    frame3.place(x=865,y=70,width=470,height=560)
    bill_frame=ttk.Frame(frame3,relief=RIDGE)
    bill_frame.place(x=10,y=50,height=500,width=460)
    scrollbar_x_bill=Scrollbar(bill_frame,orient=HORIZONTAL)
    scrollbar_y_bill=Scrollbar(bill_frame,orient=VERTICAL)
    global bill
    bill=ttk.Treeview(bill_frame,columns=('Sno','Product','Quantity','Price'),xscrollcommand=scrollbar_x_bill.set,yscrollcommand=scrollbar_y_bill.set)
    scrollbar_x_bill.pack(side=BOTTOM,fill=X)
    scrollbar_y_bill.pack(side=RIGHT,fill=Y)
    scrollbar_x_bill.config(command=bill.xview)
    scrollbar_y_bill.config(command=bill.yview)
    bill.heading('Sno',text='Sno')
    bill.heading('Product',text='Product')
    bill.heading('Price',text='Price')
    bill.heading('Quantity',text='Quantity')
    bill['show']='headings'
    bill.column('Sno',width=100)
    bill.column('Product',width=100)
    bill.column('Price',width=120)
    bill.column('Quantity',width=100)
    bill.pack(fill=BOTH,expand=1)
    bill.bind('<ButtonRelease-1>',get_values_2)

    frame1_button=ttk.Frame(frame1,relief=RIDGE)
    frame1_button.place(x=10,y=350)

    bill_button=ttk.Button(frame1_button,text='Bill',width=18,command=billing)
    bill_button.grid(row=0,column=0,pady=10,padx=10)

    clear_button=ttk.Button(frame1_button,text='Clear',width=18,command=clear)
    clear_button.grid(row=1,column=1,pady=10,padx=10)

    frame2_button=ttk.Frame(frame3,relief=RIDGE)
    frame2_button.place(x=0,y=0,width=470,height=50)

    update_button_1=ttk.Button(frame2_button,text='Update',width=18,command=update_1)
    update_button_1.grid(row=0,column=0,pady=10,padx=10)

    delete_button_1=ttk.Button(frame2_button,text='Delete',width=18,command=delete_1)
    delete_button_1.grid(row=0,column=1,pady=10,padx=10)

    print_button_1=ttk.Button(frame1_button,text='Print',width=18,command=print_bill)
    print_button_1.grid(row=1,column=0,pady=10,padx=10)

    sign_out_button=Button(root,text='Sign Out',width=18,command=destroy)
    sign_out_button.place(x=15,y=30)

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #==============================================================================Stock Tab Tkinter===========================================================================================
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    global sno_1,product_1,quantity_1,price_1
    sno_1=IntVar()
    product_1=StringVar()
    quantity_1=IntVar()
    price_1=IntVar()

    frame1_1=ttk.Frame(root2,relief=RIDGE)
    frame1_1.place(x=20,y=70,width=350,height=560)

    label1=Label(frame1_1,text='Manage',font=('verdana',20,'bold'))
    label1.grid(row=0,columnspan=2,pady=2,padx=4)

    global item_entry_1,quantity_entry_1,price_entry_1
    
    label_item=Label(frame1_1,text='Item',font=('verdana',12))
    label_item.grid(row=1,column=0,padx=10,pady=20)
    item_entry_1=Entry(frame1_1,textvariable=product_1,font=('verdana',12))
    item_entry_1.grid(row=1,column=1,padx=10,pady=20)

    label_quantity=Label(frame1_1,text='Quantity',font=('verdana',12))
    label_quantity.grid(row=2,column=0,padx=10,pady=20)
    quantity_entry_1=Entry(frame1_1,textvariable=quantity_1,font=('verdana',12))
    quantity_entry_1.grid(row=2,column=1,padx=10,pady=20)

    label_price=Label(frame1_1,text='Price',font=('verdana',12))
    label_price.grid(row=3,column=0,padx=10,pady=20)
    price_entry_1=Entry(frame1_1,textvariable=price_1,font=('verdana',12))
    price_entry_1.grid(row=3,column=1,padx=10,pady=20)

    frame2_1=ttk.Frame(root2,relief=RIDGE)
    frame2_1.place(x=400,y=70,width=720,height=560)

    table_frame_1=ttk.Frame(frame2_1,relief=RIDGE)
    table_frame_1.place(x=10,y=50,height=500,width=700)

    scrollbar_x_1=Scrollbar(table_frame_1,orient=HORIZONTAL)
    scrollbar_y_1=Scrollbar(table_frame_1,orient=VERTICAL)
    global item_table_1
    item_table_1=ttk.Treeview(table_frame_1,columns=('Sno','Product','Price','Quantity'),xscrollcommand=scrollbar_x_1.set,yscrollcommand=scrollbar_y_1.set)
    scrollbar_x_1.pack(side=BOTTOM,fill=X)
    scrollbar_y_1.pack(side=RIGHT,fill=Y)
    scrollbar_x_1.config(command=item_table_1.xview)
    scrollbar_y_1.config(command=item_table_1.yview)
    item_table_1.heading('Sno',text='Sno')
    item_table_1.heading('Product',text='Product')
    item_table_1.heading('Price',text='Price')
    item_table_1.heading('Quantity',text='Quantity')
    item_table_1['show']='headings'
    item_table_1.column('Sno',width=120)
    item_table_1.column('Product',width=120)
    item_table_1.column('Price',width=120)
    item_table_1.column('Quantity',width=120)
    item_table_1.pack(fill=BOTH,expand=1)
    item_table_1.bind('<ButtonRelease-1>',get_values_1)
    data_display_1()

    frame1_1_button=ttk.Frame(frame1_1,relief=RIDGE)
    frame1_1_button.place(x=10,y=350)

    add_button=ttk.Button(frame1_1_button,text='add',width=18,command=add)
    add_button.grid(row=0,column=0,pady=10,padx=10)

    update_button=ttk.Button(frame1_1_button,text='Update',width=18,command=update)
    update_button.grid(row=0,column=1,pady=10,padx=10)

    delete_button=ttk.Button(frame1_1_button,text='Delete',width=18,command=delete)
    delete_button.grid(row=1,column=0,pady=10,padx=10)

    clear_button_1=ttk.Button(frame1_1_button,text='Clear',width=18,command=clear_1)
    clear_button_1.grid(row=1,column=1,pady=10,padx=10)
    window.mainloop()

def destroy():
    window.destroy()
    login_page()

def login_page():
    def user_check():
        connectObj=db.connect(host='localhost',user='root',password='root123',database="shopmanagement",auth_plugin='mysql_native_password')
        cur=connectObj.cursor()
        cur.execute('select * from user')
        global id_of_user
        for i in cur.fetchall():
            print(i)
            if i[0]==user.get() and i[1]==passwrd.get():
                if i[2]=='Manager':
                    id_of_user=i[3]
                    manager()
                elif i[2]=='Employee':
                    id_of_user=i[3]
                    employee()
            else:
                continue
    def login_clear():
        user.set('')
        passwrd.set('')
        
    global login_window
    login_window=Tk()
    login_window.geometry('1350x700+0+0')

    user=StringVar()
    passwrd=StringVar()
    
    Login=Label(login_window,text='Login',font=('verdana',30))
    Login.place(x=650,y=50)
    
    username=Label(login_window,text='Username:',font=('verdana',16))
    username.place(x=575,y=350)
    username_entry=Entry(login_window,textvariable=user)
    username_entry.place(x=695,y=358)
    
    password=Label(login_window,text='Password:',font=('verdana',16))
    password.place(x=575,y=400)
    password_entry=Entry(login_window,show='*',textvariable=passwrd)
    password_entry.place(x=695,y=408)

    login_button=Button(login_window,text='Login',font=('verdana',16),command=user_check)
    login_button.place(x=595,y=460)

    clear_button=Button(login_window,text='Clear',font=('verdana',16),command=login_clear)
    clear_button.place(x=720,y=460)
    
    login_window.mainloop()
login_page()
