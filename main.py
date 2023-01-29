
from tkinter import *
from pathlib import Path
import pyqrcode
import png
from pyqrcode import QRCode
from PIL import Image ,ImageTk
import base64
import pyzbar.pyzbar as pyzbar
import cv2
import numpy
import tkinter.messagebox as msg1


PATH = Path("Icons").resolve().parent / "Icons"


root = Tk()

root.geometry("850x475+300+100")
root.resizable(0, 0)
root.configure(bg="#181824")

root.overrideredirect(True)

def move_app(e):
    root.geometry(f"+{e.x_root }+{e.y_root}")


    
def Home():

    Label1.configure(text = "Secure QR-Code Generator" , padx = 35)
    main_frame.destroy()
    page_frame = Frame(root , width=850 , height=428 , bg="#181824")
    page_frame.place(x=0 , y=47)
    
    global sqr_img
    sqr_img = PhotoImage(file=PATH  / "sqr.PNG")
    sqr_label = Label(page_frame , image=sqr_img , border=0)
    sqr_label.place(x=0 , y=3)
    
    global text_img
    text_img = PhotoImage(file=PATH / "entrytext.PNG")
    text_label = Label(page_frame ,image =text_img , border=0 )
    text_label.place(x=38 , y=233)
    
    text_entry_value = StringVar()
    text_entry = Entry(page_frame , textvariable= text_entry_value, width=28  ,border=0 , bg="#313841" , fg="#ffffff" ,font=("cabin" ,12 , "bold") )
    text_entry.place(x=75 , y=251)
    text_entry.focus()


    def Generateqr(name = ".//display.png"):
        if (len(text_entry_value.get())!=0):
            global image
            global canvas
            canvas = Canvas(width = 220, height = 220, bg = '#181824' , border= -2)
            canvas.place(x=550 , y=190)
    
            en=(text_entry_value.get()).encode("ascii")
            base64_bytes=base64.b64encode(en)       #Encoding entered string
            base64_string=base64_bytes.decode("ascii")
            print(f"{base64_string}")
    
            global qr,qr_data
            qr_data=(f"{base64_string}")
            qr = pyqrcode.create(qr_data)
            qr.png(name,scale = 5)
            qrimage = Image.open(".//display.png")
            new_image = qrimage.resize((220,220))
            new_image.save('.//display.png')
            image = ImageTk.PhotoImage(Image.open(".//display.png"))
            canvas.create_image(110,110,image=image)

            global gen_str_value
            gen_str_value = StringVar()
            gen_str = Entry(page_frame , textvariable= gen_str_value, width=30  ,border=0 ,bg="#181824" , fg="#ffffff" ,font=("cabin" ,20 , "bold"))
            gen_str.place(x=170  ,y=380)

            gen_str_value.set(f"Encoded Text : {base64_string}")
        else:
            msg = "Enter text to generate secure QR!"
            msg1.showinfo("Warning",msg)


    def clear_entry_text():
       text_entry_value.set("")
       canvas.delete("all")
       gen_str_value.set("")
       


    global qr_gen_btn_img
    qr_gen_btn_img = PhotoImage(file=PATH / "GenerateButton.PNG")
    qr_gen_btn = Button(page_frame ,image=qr_gen_btn_img , border=0 , relief=FLAT ,bg="#181824" , activebackground="#181824" ,command=Generateqr)
    qr_gen_btn.place(x= 60 , y=308)
    
    global clear_btn_img
    clear_btn_img = PhotoImage(file=PATH / "ClearButton.PNG")
    clear_btn  = Button(page_frame , image=clear_btn_img , border=0 , relief=FLAT ,bg="#181824" , activebackground="#181824" , command=clear_entry_text)
    clear_btn.place(x=230 , y = 308)


def Decode():
    Label1.configure(text = "Decode" , padx = 100)
    main_frame.destroy()
    page_frame = Frame(root , width=850 , height=428 , bg="#181824")
    page_frame.place(x=0 , y=47)

    global dcd_img
    dcd_img = PhotoImage(file=PATH  / "dcd.PNG")
    dcd_label = Label(page_frame , image=dcd_img , border=0)
    dcd_label.place(x=0 , y=5)

    global text2_img
    text2_img = PhotoImage(file=PATH / "entrytext.PNG")
    text2_label = Label(page_frame ,image =text2_img , border=0 )
    text2_label.place(x=140 , y=235)

    text2_entry_value = StringVar()
    text2_entry = Entry(page_frame , textvariable= text2_entry_value, width=28  ,border=0  , bg="#313841", fg="#ffffff" ,font=("cabin" ,12 , "bold") )
    text2_entry.place(x=178 , y=255)
    text2_entry.focus()


    def Decode_str():
        global decoded_str
        dcd = (text2_entry_value.get()).encode("ascii")
        dcd_string_bytes = base64.b64decode(dcd) 
        decoded_str = dcd_string_bytes.decode("ascii")
        print(f"{decoded_str}")

        display_dcd_str_value = StringVar()
        display_dcd_str = Entry(page_frame , textvariable= display_dcd_str_value, width=30  ,border=0 ,bg="#181824" , fg="#ffffff" ,font=("cabin" ,20 , "bold"))
        display_dcd_str.place(x=180  ,y=350)

        display_dcd_str_value.set(f"Decoded Text : {decoded_str}")


    global decode_btn_img
    decode_btn_img = PhotoImage(file=PATH / "decodebutton.PNG")
    decode_btn = Button(page_frame ,image=decode_btn_img , border=0 , relief=FLAT ,bg="#181824" , activebackground="#181824" , command=Decode_str)
    decode_btn.place(x= 500 , y=238)

def SCAN():
    Label1.configure(text = "Scan-QR" , padx=100)
    main_frame.destroy()
    page_frame = Frame(root , width=850 , height=428 , bg="#181824")
    page_frame.place(x=0 , y=47)

    global scan_img
    scan_img = PhotoImage(file=PATH /"qrimage.PNG")
    scan_label = Label(page_frame , image=scan_img , border=0)
    scan_label.place(x=60 , y=9)

    global scan_text_img
    scan_text_img = PhotoImage(file=PATH / "scanqr.PNG")
    scan_text_label = Label(page_frame , image=scan_text_img , border=0)
    scan_text_label.place(x=400 , y=17)

    

    def scanqr():
        i = 0
        cap = cv2.VideoCapture(0 ,cv2.CAP_DSHOW)
        while i<1:
            _, frame = cap.read()

            decoded = pyzbar.decode(frame)
            for obj in decoded:
                print(obj.data.decode("utf-8"))
                i = i+1
                global text_img
                text_img = PhotoImage(file=PATH / "entrytext.PNG")
                text_label = Label(page_frame,image =text_img , border=0 )
                text_label.place(x=360,y=330)           
                global scanentry_1
                scanentry_1=StringVar()
                scanentry_1.set(obj.data.decode("utf-8"))
                decodeentry=Entry (page_frame,textvariable=scanentry_1,font="cabin 12  bold",bg="#313841", fg="#ffffff",border=0,width=30)
                decodeentry.place(x=390,y=350)
                scanlabel = Label(page_frame,text="Output:-",font="cabin 14  bold",bg="#181824",fg="#ffffff",padx=5)
                scanlabel.place(x=260,y=350)

            cv2.imshow("Qrcode" , frame)
            cv2.waitKey(5)
            cv2.destroyAllWindows
            

            
    

    global scan_btn_img
    scan_btn_img = PhotoImage(file=PATH / "scanbutton.PNG")
    scan_btn = Button(page_frame , image=scan_btn_img , border=0 , relief=FLAT ,bg="#181824" , activebackground="#181824" ,command=scanqr)
    scan_btn.place(x=400 , y=250 )




def About():
    Label1.configure(text="About-us" , padx=100)
    main_frame.destroy()
    page_frame = Frame(root , width=850 , height=428 , bg="#181824")
    page_frame.place(x=0 , y=47)

    global about_img
    about_img = PhotoImage(file=PATH  / "about_us.PNG")
    about_label = Label(page_frame , image=about_img , border=0)
    about_label.place(x=30 , y=20)

    about_text = Label(page_frame , text="Hello there!,\nThis is secure QR-Code generator which takes input string from you and the input string is encoded\nwith ascii which makes it difficult to read.Thus by using decode, the encoded string converts into\nredable format or converting it into the input-string entered by you.\nHope you had a wonderful experience using our Secure QR-Code Generator" , fg ="#ffffff",bg="#181824" , justify="left" , font = ("Cabin" , 11 , "bold") )
    about_text.place(x=42 , y=200)

    aboutlabel2 = Label(page_frame,text= "Regards\n-Team COE\nShreyash Jawalkar,Snehal Kedia,Palak Modi and Pratik Pandey",fg ="#ffffff",bg="#181824" , justify="left",font="cabin 11 bold")
    aboutlabel2.place(x=42,y=300)


    


def change_on_hover(button , onhover , onleave):

    def on_enter(e):
        button["background"] = onhover

    def on_leave(e):
        button["background"] = onleave

    button.bind("<Enter>" , on_enter)
    button.bind("<Leave>" , on_leave)



# slide bar
def slide_bar():
    global main_frame
    main_frame = Frame(root, width=300, height=475, bg="#09050D")
    main_frame.place(x=0, y=0)

    def dele():
        main_frame.destroy()

    global back_btn_img
    back_btn_img = PhotoImage(file=PATH / "chevron-left.png")
    back_btn = Button(main_frame, command=dele, image=back_btn_img, height=20, width=20,
                      border=0, bg="#09050D", relief="flat", activebackground="#09050D")
    back_btn.place(x=265, y=10)   
    menulabel = Label(main_frame,text="Menu",font="cabin 14  bold",bg="#09050D",fg="#ffffff",padx=5)
    menulabel.place(x=0,y=10,) 


#########################################################################################################################################
        #Home Button 
         
    global Home_btn_img
    Home_btn_img = PhotoImage(file=PATH / "home.png")
    Home_btn = Button(main_frame , text="Home" , fg ='#ffffff' , image=Home_btn_img ,
                              compound=LEFT , command=Home ,  width = 300 , height=35 ,border=0 , activebackground="#181824", activeforeground='#ffffff', relief="flat", 
                               bg = "#09050D" , padx=7 ,font = ("Cabin" , 12 , "bold"),anchor="w")
    Home_btn.place(x=0,y=50)

    change_on_hover(Home_btn , "#181824" , "#09050D")



        #Decode Button

    global decode_btn_img
    decode_btn_img = PhotoImage(file=PATH / "shield-off.png")
    decode_btn = Button(main_frame , text="Decode" , fg ='#ffffff' , image=decode_btn_img ,
                              compound=LEFT , command=Decode ,  width = 300 , height=35 ,border=0 , activebackground="#181824", activeforeground='#ffffff', relief="flat", 
                               bg = "#09050D" , padx=7,font = ("Cabin" , 12 , "bold") , anchor="w")
    decode_btn.place(x=0 , y= 100)
    change_on_hover(decode_btn , "#181824" , "#09050D")


    global scan_btn_img
    scan_btn_img = PhotoImage(file=PATH / "camera.png")
    scan_btn = Button(main_frame , text="Scan" , fg ='#ffffff' , image=scan_btn_img ,
                              compound=LEFT , command=SCAN ,  width = 300 , height=35 ,border=0 , activebackground="#181824", activeforeground='#ffffff', relief="flat", 
                               bg = "#09050D" , padx=10,font = ("Cabin" , 12 , "bold") , anchor="w")
    scan_btn.place(x=0 , y=150)
    change_on_hover(scan_btn , "#181824" , "#09050D")
            #About Us Button

    global about_us_button_img
    about_us_button_img = PhotoImage(file=PATH / "info.png")
    about_us_button = Button(main_frame , text="About" , fg ='#ffffff' , image=about_us_button_img ,
                              compound=LEFT , command=About ,  width = 300 , height=35 ,border=0 , activebackground="#181824", activeforeground='#ffffff', relief="flat", 
                               bg = "#09050D" , padx=7,font = ("Cabin" , 12 , "bold") , anchor="w")
    about_us_button.place(x=0 , y=200)
    change_on_hover(about_us_button , "#181824" , "#09050D")


#########################################################################################################################################


# New Title Bar
title_bar = Frame(root, bg="#09050D")
title_bar.place(x=0, y=0, width=850, height=47)
title_bar.bind("<B1-Motion>" , move_app)
Label1 = Label(title_bar,text = "Secure QR-Code Generator",font="cabin 17  bold",fg="#ffffff",bg="#09050D" , anchor=CENTER)
Label1.place(x=270,y=5)

# Close Button
close_btn_img = PhotoImage(file=PATH / "x1.png")
close_btn = Button(title_bar, image=close_btn_img, height=20, width=20, border=0,
                   bg="#09050D", relief="flat", activebackground="#09050D" , command=quit)
close_btn.place(x=817, y=13)

# Menu Button (To open slide menu)
menu_btn_img = PhotoImage(file=PATH / "menu_resized.png")
menu_btn = Button(title_bar, image=menu_btn_img, height=20, width=20,  command=slide_bar,
                  border=0, bg="#09050D", relief="flat", activebackground="#09050D")
menu_btn.place(x=10, y=10)


sqr_img = PhotoImage(file=PATH  / "sqr.PNG")
sqr_label = Label(root , image=sqr_img , border=0)
sqr_label.place(x=0 , y=50)

text_img = PhotoImage(file=PATH / "entrytext.PNG")
text_label = Label(root ,image =text_img , border=0 )
text_label.place(x=38 , y=280)

text_entry_value = StringVar()
text_entry = Entry(root , textvariable= text_entry_value, width=28  ,border=0 , bg="#313841" , fg="#ffffff" ,font=("cabin" ,12 , "bold") )
text_entry.place(x=75 , y=300)
text_entry.focus()



def Generateqr(name = ".//display.png"):
    if (len(text_entry_value.get())!=0):
        global image
        global canvas
        canvas = Canvas(width = 220, height = 220, bg = '#181824' , border= -2)
        canvas.place(x=550 , y=190)

        en=(text_entry_value.get()).encode("ascii")
        base64_bytes=base64.b64encode(en)       #Encoding entered string
        base64_string=base64_bytes.decode("ascii")
        print(f"{base64_string}")

        global qr,qr_data , gen_str_value
        qr_data=(f"{base64_string}")
        qr = pyqrcode.create(qr_data)
        qr.png(name,scale = 5)
        qrimage = Image.open(".//display.png")
        new_image = qrimage.resize((220,220))
        new_image.save('.//display.png')
        image = ImageTk.PhotoImage(Image.open(".//display.png"))
        canvas.create_image(110,110,image=image)
        gen_str_value = StringVar()
        gen_str = Entry(root , textvariable= gen_str_value, width=30  ,border=0 ,bg="#181824" , fg="#ffffff" ,font=("cabin" ,20 , "bold"))
        gen_str.place(x=170  ,y=430)

        gen_str_value.set(f"Encoded Text : {base64_string}")
    else:
        msg = "Enter text to generate secure QR!"
        msg1.showinfo("Warning",msg)

def clear_entry_text():
    text_entry_value.set("")
    canvas.delete("all")
    gen_str_value.set("")



qr_gen_btn_img = PhotoImage(file=PATH / "GenerateButton.PNG")
qr_gen_btn = Button(root ,image=qr_gen_btn_img , border=0 , relief=FLAT ,bg="#181824" , activebackground="#181824" , command=Generateqr)
qr_gen_btn.place(x= 60 , y=358)

clear_btn_img = PhotoImage(file=PATH / "ClearButton.PNG")
clear_btn  = Button(root , image=clear_btn_img , border=0 , relief=FLAT ,bg="#181824" , activebackground="#181824" , command=clear_entry_text)
clear_btn.place(x=230 , y = 356)


root.mainloop()