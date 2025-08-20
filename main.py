from random import randint
import pyrebase
import tkinter 
from tkinter import *
from tkinter import ttk
from turtle import right
from PIL import Image, ImageTk
import cv2

config = {
  "apiKey": "AIzaSyAd2SetY7zJmQNWECi3f6CjOJXE0bm75ik",
  "authDomain": "cangar-9e508.firebaseapp.com",
  "databaseURL": "https://cangar-9e508-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "cangar-9e508",
  "storageBucket": "cangar-9e508.appspot.com",
  "messagingSenderId": "972857343706",
  "appId": "1:972857343706:web:8741c85ea60dba80c66fe3",
  "measurementId": "G-XLS917ZKX4"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#color
dark = '#2C3333'
grey = '#395B64'
smooth = '#A5C9CA'
light = '#E7F6F2'
white = 'white'
bg_side = white
bg_menu = white

#font
judul= "poppins 18 bold"
sub = "poppins 12 bold"
desk = "poppins 10 bold"

#size 
height_top_frame = 60
width_top_frame = 720
width_side_menu = 200
height_side_menu = 600
height_menu_frame = 520
width_menu_frame = 700

root = Tk()
root.geometry('1050x600')
root.state('zoomed')
root.config(bg=smooth)

root.title('ARGROTECHNO PARK UB APPS')

def profile():
    global menu
    menu.destroy()
    profile = Frame(root,bg=bg_menu, width=width_menu_frame, height=height_menu_frame)
    profile.place(x=310, y=70)
    e1 = Label(profile, text="PROFILE", font="System 30", bg=bg_menu, fg=grey).place(x=650/2,y=400/2)
    menu = profile

def monitoring():
    global menu
    menu.destroy()
    monitoring= Frame(root,bg=bg_menu, width=width_menu_frame, height=height_menu_frame)
    monitoring.place(x=310, y=70)

    items = "Cam1", "Cam2","Cam3","Cam4"
    change_cam = ttk.Combobox(monitoring, values=items, font="Poppins 10 bold")
    change_cam.current(0)
    change_cam.place(x=50, y=25, width=150)

    vid_cam = Label(monitoring)

    def pil_cam(img, vid_cam):
        img = cv2.resize(img, (480,270))
        img = cv2.flip(img, 1)
        image = Image.fromarray(img)
        pic = ImageTk.PhotoImage(image)
        vid_cam.configure(image=pic)
        vid_cam.image = pic
        vid_cam.place(x=50, y=100)

    def choose():
        global cap1, cap2, cap3, cap4
        if change_cam.get() == "Cam1":
            cap1 = cv2.VideoCapture(1)
            cap2 = cv2.VideoCapture()
            cap3 = cv2.VideoCapture()
            cap4 = cv2.VideoCapture()

        if change_cam.get() == "Cam2":
            cap2 = cv2.VideoCapture(0)
            cap1 = cv2.VideoCapture()
            cap3 = cv2.VideoCapture()
            cap4 = cv2.VideoCapture()

        if change_cam.get() == "Cam3":
            cap3 = cv2.VideoCapture(3)
            cap2 = cv2.VideoCapture()
            cap1 = cv2.VideoCapture()
            cap4 = cv2.VideoCapture()

        if change_cam.get() == "Cam4":
            cap4 = cv2.VideoCapture(4)
            cap2 = cv2.VideoCapture()
            cap3 = cv2.VideoCapture()
            cap1 = cv2.VideoCapture()
        show()

    switch_btn = Button(monitoring, text="SWITCH", font="Poppins 10", command=choose)
    switch_btn.place(x=250, y=25, width=100)

    mode = "RGB", "GRAY", "LAB", "HVS", "HLS", "Canny"
    change_mode = ttk.Combobox(monitoring, values=mode, font="Poppins 10 bold")
    change_mode.place(x=400, y=25, width=150)
    change_mode.current(0)

    def show():
        if change_cam.get() == "Cam1":
            _, frame = cap1.read()
        if change_cam.get() == "Cam2":
            _, frame = cap2.read()
        if change_cam.get() == "Cam3":
            _, frame = cap3.read()
        if change_cam.get() == "Cam4":
            _, frame = cap4.read()
            
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        lab = cv2.cvtColor(rgb, cv2.COLOR_BGR2Lab)
        hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
        hls = cv2.cvtColor(rgb, cv2.COLOR_BGR2HLS)
        canny = cv2.Canny(gray,100,200)

        if change_mode.get()=="RGB":
            pil_cam(rgb, vid_cam)
        if change_mode.get()=="GRAY":
            pil_cam(gray, vid_cam)    
        if change_mode.get()=="LAB":
            pil_cam(lab, vid_cam)    
        if change_mode.get()=="HSV":
            pil_cam(hsv, vid_cam)    
        if change_mode.get()=="HLS":
            pil_cam(hls, vid_cam)    
        if change_mode.get()=="Canny":
            pil_cam(canny, vid_cam)
        vid_cam.after(30, show)

    menu = monitoring

def control():
    global menu
    global e3
    menu.destroy()
    control = Frame(root,bg=bg_menu, width=width_menu_frame, height=height_menu_frame)
    control.place(x=310, y=70)

    b1_true = Button(control, text="ON",font="poppins 10 bold", width=5)
    b1_true.place(x=20, y=20)

    b1_false = Button(control, text="OFF", font="poppins 10 bold", width=5)
    b1_false.place(x=20, y=70)

    l1_cond = Label(control, text="NO CONDITION", font="poppins 10 bold", width=15, height=3)
    l1_cond.place(x=100, y=20)
    def update():
        global read
        read = (db.child('data').get()).val()
        print(read)
        e3['text'] = str(read)
        menu_frame.after(1000, update)
    # b1 = Button(control, text="TEXT A", )
    e3 = Label(control, text="saya", font="System 5", bg=white, fg=dark)
    e3.place(x=650/2,y=400/2)

    update()
    menu = control

#top_frame
top_frame = Frame(root, bg=dark)
top_frame.place(x=300, y=0, width=width_top_frame, height=height_top_frame)
Label(top_frame, text="AGROTECHNOPARK", font=judul, bg=dark, fg=white).pack(side=RIGHT, padx=20, pady=10)

#side_menu
side_menu = Frame(root, bg=bg_side)
side_menu.place(x=0, y=0, width=width_side_menu, height=height_side_menu)
logo = Image.open("/home/pi/ATPCangar/ub.png")
logo = logo.resize((100,100), Image.ANTIALIAS)
ub = ImageTk.PhotoImage(logo)
Label(side_menu, image=ub, bg=bg_side).place(x=100, y=50)
name_user = Label(side_menu, text="USERNAME", font=sub, bg=bg_side, fg=dark)
name_user.place(x=100, y=170)

#menu
#profile
profile_icon = ImageTk.PhotoImage(Image.open('/home/pi/ATPCangar/profile.png').resize((40,40), Image.ANTIALIAS))
l_profilico = Label(side_menu, image=profile_icon, bg=bg_side)
l_profilico.place(x=50, y=250)
btn_profile = Button(side_menu, text="PROFILE", font=sub, bg=bg_side, fg=dark, border=0, bd=0, cursor='hand2', command=profile)
btn_profile.place(x=110, y=250)
#monitoring
monitor_icon = ImageTk.PhotoImage(Image.open('/home/pi/ATPCangar/monitoring.png').resize((40,40), Image.ANTIALIAS))
l_profilico = Label(side_menu, image=monitor_icon, bg=bg_side)
l_profilico.place(x=50, y=320)
btn_profile = Button(side_menu, text="MONITORING", font=sub, bg=bg_side, fg=dark, border=0, bd=0, cursor='hand2', command=monitoring)
btn_profile.place(x=110, y=320)
#control
control_icon = ImageTk.PhotoImage(Image.open('/home/pi/ATPCangar/control.png').resize((40,40), Image.ANTIALIAS))
l_profilico = Label(side_menu, image=control_icon, bg=bg_side)
l_profilico.place(x=50, y=390)
btn_profile = Button(side_menu, text="CONTROL", font=sub, bg=bg_side, fg=dark, border=0, bd=0, cursor='hand2', command=control)
btn_profile.place(x=110, y=390)

#menu_frame
menu_frame = Frame(root,bg=bg_menu, width=width_menu_frame, height=height_menu_frame)
menu_frame.place(x=310, y=70)
menu = menu_frame

root.mainloop()