
"""15260556 MUCAHIT KAYA  13260551 ONDER POLAT"""
import cv2
import os
import face_recognition	
import pickle
import smtplib
import numpy as np
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import image
import sqlite3
from tkinter import *
from tkinter import messagebox as ms
import datetime
now = datetime.datetime.now()



DOSYAYOLU = "Dataset1/" 
det = False
font = cv2.FONT_HERSHEY_SIMPLEX
c = 0
video = ""

insan = os.listdir(DOSYAYOLU) 

TumKodlar = []
TumEtiketler = []

avgKodlar = []
avgEtiketler = []

GirisYapanlar = []

for kisi in insan: 
    print(kisi)
    GoruntuYolu = DOSYAYOLU + '/' + kisi
    goruntuler = os.listdir(GoruntuYolu) 
    for image in goruntuler: 
        img = cv2.imread(GoruntuYolu + '/' + image) 
        LM = face_recognition.api.face_landmarks(img, face_locations=None, model='small') 
        if len(LM) == 0: 
            continue 
        encoding = face_recognition.face_encodings(img)[0] 
        TumKodlar.append(encoding) 
        TumEtiketler.append(kisi) 
    avgKodlar.append(sum(TumKodlar)/len(TumKodlar))
    avgEtiketler.append(kisi)
print(avgEtiketler)


def sinif1():
    global video
    video = "sinif1.mp4" 
    baslatVideo(video) 

def sinif2():
    global video
    video = "sinif2.mp4"
    baslatVideo(video)

def sinif3():
    global video
    video = "sinif3.MOV"
    baslatVideo(video)
	
def YuzleriKarsilastir(crop_img, left, bottom): 
    global TumKodlar, font, gray, GirisYapanlar
    distList = []
    for n, i in enumerate(avgKodlar): 
      
        bilinmeyen = face_recognition.face_encodings(crop_img)[0] 
        sonuclar = face_recognition.compare_faces([i], bilinmeyen, tolerance = 0.4) 

        new = True
        if sonuclar[0]: 

            for i in range(len(GirisYapanlar)): 
                if avgEtiketler[n] == GirisYapanlar[i]: 
                    new = False
                    break
            if new:
                GirisYapanlar.append(avgEtiketler[n])
            cv2.putText(gray, avgEtiketler[n],(left,bottom+30), font, 0.5, (255, 0, 0), 2, cv2.LINE_AA) 
            break
  
def drawboxes(Loc, i, det):  
    global gray
    lab = ""
    top = Loc[i][0] 
    right = Loc[i][1]
    bottom = Loc[i][2]
    left = Loc[i][3]
    cv2.rectangle(gray, (left, top), (right, bottom), (255,0,0), 2) 
    crop_img = gray[top:bottom, left:right] 
    LM = face_recognition.api.face_landmarks(crop_img, face_locations=None, model='small') 
    
    if len(LM) != 0 and det == False: 
        
        YuzleriKarsilastir(crop_img, left, bottom) 
        
        
    cv2.putText(gray,lab,(left,bottom+30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
    

def capture(det, c, cap): 
    global gray
    
    ret, frame = cap.read() 
    if not ret: 
        email()
        return True, c
    if video != "sinif3.MOV":
    	out=cv2.transpose(frame) 
    	frame=cv2.flip(out,flipCode=1)
    row, col, Z = frame.shape 
    row, col, Z = frame.shape
    
    gray = frame

    Loc = face_recognition.face_locations(gray, number_of_times_to_upsample=1, model='hog') 
    faces = len(Loc)
    if faces != 0:
        for i in range(0, faces):
            drawboxes(Loc, i, det) 
    else:
        det = False
    
    cv2.imshow("Frame", gray)
    return False, c

def email(): 
    global GirisYapanlar
    print(GirisYapanlar)
    email = 'bilalahmetdemir132@gmail.com' 
    sifre = '25704483Km.'
    gonderilen_email = 'onderpolattt@gmail.com' 
    Konu = 'Sınıfa Giriş Yapan Kişilerin Listesi' 
    Mesaj = 'Sınıfa Giriş Yapan Kişiler: ' 
    for kisi in GirisYapanlar:
        Mesaj = Mesaj + ', ' + str(kisi)
    print(Mesaj)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = gonderilen_email
    msg['Konu'] = Konu

 
    msg.attach(MIMEText(Mesaj, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.starttls() 

    server.login(email, sifre) 
    text = msg.as_string()
    server.sendmail(email, gonderilen_email , text) 
    server.quit() 
    


def baslatVideo(video): 
    global c
    cap = cv2.VideoCapture(video) 
    while True:
        
        exit, c = capture(det, c, cap) 
        if (cv2.waitKey(1) & 0xFF == ord('q')) or exit: 
            cap.release() 
            cv2.destroyAllWindows() 
            break





win=Tk()
win.title("Fırat Üniversitesi Yüz Tanıma Sistemi")
win.geometry("1000x500")


canvas_end = Canvas(win,width=1000,height=60)
canvas_end.place(x=0,y=305)

final_message=Label(win,text="",font=("Grange",10))
final_message_window = canvas_end.create_window(34, 10, window=final_message,anchor=NW)

canvas1 = Canvas(win,width=1000,height=35,bg="Orange")
canvas1.place(x=0,y=0)

img_fb = PhotoImage(file="GUI/Icons/fb_s.png")
btn_fb = Button(win,bg='Orange',relief = SUNKEN,image=img_fb,borderwidth=0,cursor="hand2")
btn_fb.configure(width=25,height=25)
fb_window = canvas1.create_window(26, 18, window=btn_fb)


img_tw = PhotoImage(file="GUI/Icons/twitter_s.png")
btn_tw = Button(win,bg='Orange',relief = SUNKEN,image=img_tw,borderwidth=0,cursor="hand2")
btn_tw.configure(width=25,height=25)
tw_window = canvas1.create_window(63, 18, window=btn_tw)


img_insta = PhotoImage(file="GUI/Icons/insta_s.png")
btn_ig = Button(win,bg='Orange',relief = SUNKEN,image=img_insta,borderwidth=0,cursor="hand2")
btn_ig.configure(width=28,height=28)
ig_window = canvas1.create_window(103, 18, window=btn_ig)


img_yt = PhotoImage(file="GUI/Icons/yt_s.png")
btn_yt = Button(win,bg='Orange',relief = SUNKEN, image=img_yt,borderwidth=0,cursor="hand2")
btn_yt.configure(width=28,height=28)
yt_window = canvas1.create_window(142, 18, window=btn_yt)

canvas1.create_line(400,13,400,28,fill="white")

canvas1.create_line(512,13,512,28,fill="white")

img_msg = PhotoImage(file="GUI/Icons/msg.png")
canvas1.create_image(530,19,image=img_msg)
btn_gmail_open = Button(win,text="15260556@firat.edu.tr",fg="White",bg='Orange',relief=SUNKEN,borderwidth=0,cursor="hand2")
btn_gmail_open.configure(width=17,height=1)
canvas1.create_window(625,19,window=btn_gmail_open)


canvas_middle = Canvas(win,width=1000,height=120)
canvas_middle.place(x=0,y=40)

canvas_middle.create_text(500,30,text="Fırat Üniversitesi Bitirme Ödevi",font=("Boulder Bold",28))

img_edit=PhotoImage(file="GUI/Icons/edit.png")
canvas_middle.create_image(270,70,image=img_edit)

canvas_middle.create_text(450,75,text="Sınıf giriş bildirim sistemi",font=("Myriad Pro Light",18))
canvas_middle.create_text(410,101,text="Takibini yapmak istediğiniz sınıfı seçiniz.  ",fill="Black")

canvas3 = Canvas(win,width=1000,height=100)#,bg="Orange")
canvas3.place(x=20,y=195)


canvas4=Canvas(win,width=700,height=170)
canvas4.place(x=380,y=150)
img_face=PhotoImage(file="GUI/Icons/face_m.png")
canvas4.create_image(60,80,image=img_face)


canvas5=Canvas(win,width=700,height=170)
canvas5.place(x=30,y=350)

btn_class1 = Button(win,text="Sınıf-1",fg="White",bg='Orange',relief=SUNKEN,borderwidth=1,cursor="hand2", command=sinif1)
btn_class1.configure(width=17,height=1)
canvas5.create_window(250,19,window=btn_class1)

btn_class2 = Button(win,text="Sınıf-2",fg="White",bg='Orange',relief=SUNKEN,borderwidth=1,cursor="hand2", command=sinif2)
btn_class2.configure(width=17,height=1)
canvas5.create_window(400,19,window=btn_class2)

btn_class3 = Button(win,text="Sınıf-3",fg="White",bg='Orange',relief=SUNKEN,borderwidth=1,cursor="hand2", command=sinif3)
btn_class3.configure(width=17,height=1)
canvas5.create_window(550,19,window=btn_class3)


win.mainloop()




















