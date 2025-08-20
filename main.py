import tkinter
import pyrebase
import PIL
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from PIL import Image, ImageTk
import cv2

config = {
  "apiKey": "AIzaSyDRq6JqMAtQiKvOg6mgILsr7ZQ42gMBV5A",
  "authDomain": "cangar-europa-server.firebaseapp.com",
  "databaseURL": "https://cangar-europa-server-default-rtdb.firebaseio.com",
  "projectId": "cangar-europa-server",
  "storageBucket": "cangar-europa-server.appspot.com",
  "messagingSenderId": "671201908053",
  "appId": "1:671201908053:web:99765d65cbb131dda2cbdc"
};

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#color
bg = '#52734D'
side = '#FEFFDE'
menu = '#DDFFBC'
ot = '#91C788'

#font
p18 = 'poppins 18 bold'
p16 = 'poppins 16 bold'
p14 = 'poppins 14 bold'
p12 = 'poppins 12 bold'
p10 = 'poppins 10 bold'

root = Tk()
root.geometry('1020x600')
root.config(bg=menu)
root.title('AGROTECHNO PARK UB APPS')
media = Frame(root)

class MenuFrame(Frame):
    def __init__(self, the_window):
        super().__init__()
        self['width']=780
        self['height']=520
        self['bg']=ot

class WebcamChoose():
    def __init__(self, window, cap):
        super().__init__()
        self.window = window
        self.cap = cap
        # self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.interval = 20 
        self.label = Label(self.window)
        self.label.place(x=10, y=10)
        self.update_image()

    def update_image(self):
        _, self.frame = self.cap.read()
        self.frame = cv2.flip(self.frame, 0)
        self.frame = cv2.resize(self.frame, (480, 270))
        self.image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 
        self.image = Image.fromarray(self.image) 
        self.image = ImageTk.PhotoImage(self.image) 
        self.label.imgtk = self.image
        self.label.configure(image=self.image)
        self.window.after(self.interval, self.update_image)

class ColorPicker():
    def __init__(self, window):
        super().__init__()
        self.window = window

        Button(self.window, text='Pick Color', width=10, border=0, bd=0, font=p12, command=self.color).place(x=10, y=300)      

    def color(self):
        my_color = colorchooser.askcolor()
        string_color = my_color[1]
        r = int(my_color[0][0])
        g = int(my_color[0][1])
        b = int(my_color[0][2])
        rgb = '( ' + str(r) + ' , ' + str(g) + ' , ' + str(b) + ' )'
        rgb_mode = Label(self.window, text=rgb, width=15, height=2, bg=string_color)
        rgb_mode.place(x=10, y=350)
        hex_mode = Label(self.window, text=my_color[1], width=15,height=2, bg=string_color)
        hex_mode.place(x=10, y=390)
        data = {"rgb" : rgb , "hex" : my_color[1]}
        db.child("pameran").child("set color").set(data)

class Setting():
    def __init__(self, window):
        super().__init__()
        self.window = window

        move = Label(self.window, text='Move Robot', width=10, font=p14, bg=ot)
        move.place(x=200, y=303)
        
        pump = Label(self.window, text='PUMP', width=10, font=p14, bg=ot)
        pump.place(x=500, y=303)
        
    def move(self):
        mov1 = Button(self.window, text='MEDIA 1', border=0, cursor='hand2', bd=0, font=p12, width=10, command=self.media1)
        mov1.place(x=200, y=350)

        mov2 = Button(self.window, text='MEDIA 2', border=0, cursor='hand2', bd=0, font=p12, width=10, command=self.media2)
        mov2.place(x=200, y=400)

        mov3 = Button(self.window, text='MEDIA 3', border=0, cursor='hand2', bd=0, font=p12, width=10, command=self.media3)
        mov3.place(x=350, y=350)

        mov2 = Button(self.window, text='HOME', border=0, cursor='hand2', bd=0, font=p12, width=10, command=self.home)
        mov2.place(x=350, y=400)
        
        pump_on = Button(self.window, text='ON', border=0, cursor='hand2', bd=0, font=p12, width=5, command=self.on_pump)
        pump_on.place(x=600, y=350)
        
        pump_off = Button(self.window, text='OFF', border=0, cursor='hand2', bd=0, font=p12, width=5, command=self.off_pump)
        pump_off.place(x=600, y=400)
    
    def media1(self):
        db.child("pameran").child('move').set(1)
    def media2(self):
        db.child("pameran").child('move').set(2)   
    def media3(self):
        db.child("pameran").child('move').set(3)
    def home(self):
        db.child("pameran").child('move').set(0)
    def on_pump(self):
        db.child("pameran").child('pump').set(1)
    def off_pump(self):
        db.child("pameran").child('pump').set(0)

class ReadSensor():
    def __init__(self, window, media):
        super().__init__()
        self.window = window
        self.media = media
        
        self.frame = Frame(self.window, width=270, height=270, bg=menu) 
        self.frame.place(x=500, y=10)
        
        self.label_media = Label(self.frame, text=self.media, font="poppins 20 bold", bg=menu)
        self.label_media.place(x=10, y=5)
        
        self.label_lux = Label(self.frame, text="LUX", font=p14, bg=menu, width=9)
        self.label_lux.place(x=5, y=50)

        self.label_hum = Label(self.frame, text="Humidity", font=p14, bg=menu, width=9)
        self.label_hum.place(x=130, y=50)
        
        self.label_lux = Label(self.frame, text="Suhu", font=p14, bg=menu, width=9)
        self.label_lux.place(x=5, y=125)
        
        self.label_tdsin = Label(self.frame, text="TDS-in", font=p14, bg=menu, width=9)
        self.label_tdsin.place(x=5, y=200)

        self.label_tdsout = Label(self.frame, text="TDS-out", font=p14, bg=menu, width=9)
        self.label_tdsout.place(x=130, y=200)
        
    def read(self):
        self.read_lux = (db.child('pameran').child('lux').get()).val()
        self.label_lux = Label(self.frame, text=self.read_lux, font=p14, bg=menu, width=9)
        self.label_lux.place(x=5, y=80)

        self.read_hum = (db.child('pameran').child('hum').get()).val()
        self.label_hum = Label(self.frame, text=self.read_hum, font=p14, bg=menu, width=9)
        self.label_hum.place(x=130, y=80)
        
        self.read_temp = (db.child('pameran').child('temp').get()).val()
        self.label_temp = Label(self.frame, text=self.read_temp, font=p14, bg=menu, width=9)
        self.label_temp.place(x=5, y=155)
        
        self.read_tdsin = (db.child('pameran').child('tdsin').get()).val()
        self.label_tdsin = Label(self.frame, text=self.read_tdsin, font=p14, bg=menu, width=9)
        self.label_tdsin.place(x=5, y=230)
        
        self.read_tdsout = (db.child('pameran').child('tdsout').get()).val()
        self.label_tdsout = Label(self.frame, text=self.read_tdsout, font=p14, bg=menu, width=9)
        self.label_tdsout.place(x=130, y=230)
        
        root.after(2000, self.read)
        

def sec1():
    global media
    media.destroy()
    screen1 = MenuFrame(root)
    screen1.place(x=230, y=70)
    WebcamChoose(screen1, cv2.VideoCapture(2))
    ColorPicker(screen1)
    set = Setting(screen1)
    set.move()
    read = ReadSensor(screen1, "MEDIA 1")
    read.read()
    media = screen1

def sec2():
    global media
    media.destroy()
    screen2 = MenuFrame(root)
    screen2.place(x=230, y=70)
    WebcamChoose(screen2, cv2.VideoCapture(4))
    ColorPicker(screen2)
    set = Setting(screen2)
    set.move()
    read = ReadSensor(screen2, "MEDIA 2")
    read.read()
    media = screen2

def sec3():
    global media
    media.destroy()
    screen3 = MenuFrame(root)
    screen3.place(x=230, y=70)
    WebcamChoose(screen3, cv2.VideoCapture(0))
    ColorPicker(screen3)
    set = Setting(screen3)
    set.move()
    read = ReadSensor(screen3, "MEDIA 3")
    read.read()
    media = screen3

#sidemenu
sidemenu = Frame(root, bg=side)
sidemenu.place(x=0, y=0, width=220, height=600)
ub = ImageTk.PhotoImage(Image.open('/home/pi/ATPCangar/Pameran/ub.png').resize((80,80), Image.ANTIALIAS))
Label(sidemenu, image=ub, bg=side).place(x=(220/2)-30, y=30)
iot = ImageTk.PhotoImage(Image.open('/home/pi/ATPCangar/Pameran/iot black.png').resize((60,60), Image.ANTIALIAS))
Label(sidemenu, image=iot, bg=side).place(x=(220/2)-80, y=130)
ubtech = ImageTk.PhotoImage(Image.open('/home/pi/ATPCangar/Pameran/ubtech.png').resize((60,60), Image.ANTIALIAS))
Label(sidemenu, image=ubtech, bg=side).place(x=(220/2)+20, y=130)

#media
y = 240
info = "Media 1", "Media 2", "Media 3"
cmd = sec1, sec2, sec3
for i in range(3):
    Button(sidemenu, text=info[i], border=0, font=p14, bg= bg, fg=side, width=13, cursor='hand2', command=cmd[i]).place(x=10, y=y)
    y +=60

#topframe
topframe = Frame(root, bg=bg)
topframe.place(x=220, y=0, width=1020-220, height=60)
Label(topframe, text="AGROTECHNOPARK", font=p18, bg=bg, fg=side).pack(side=RIGHT, padx=20, pady=10)

root.mainloop()