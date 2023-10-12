from tkinter import *
from tkinter.font import Font
from tkinter import filedialog
from PIL import Image, ImageTk
import imutils
from PIL.Image import ImageTransformHandler
import cv2

import pytesseract
import numpy as np

window = Tk()
window.geometry('900x650')
window.title("Number-Plate Recognition")
sign_image = Label(window, bd=10)
myfont = Font(family="times", size=13)
heading = Font(family="times", size=15)
pytesseract.pytesseract.tesseract_cmd="C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"
cascade= cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

def select_image():
    try:
        file_path = filedialog.askopenfilename()
        image = Image.open(file_path)
        resized = image.resize((300, 400))
        myImage = ImageTk.PhotoImage(resized)
        sign_image.configure(image=myImage)
        sign_image.image = myImage
        show_classify_button(file_path)
    except:
        pass


def show_classify_button(file_path):
    classify = Button(window, text="Classify Image", bg="green", fg="white", width=15, font=myfont,
                      command=lambda: classify_image(file_path))
    classify.pack()
    classify.place(x=500, y=100)


def classify_image(file_path):
    print("Hello World")
    global myImage1,myImage
    img = cv2.imread(file_path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (600, 400))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)

    edged = cv2.Canny(gray, 30, 200)
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None
    for c in contours:

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print("No contour detected")
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
    new_image = cv2.bitwise_and(img, img, mask=mask)

    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    #print("programming_fever's License Plate Recognition\n")
    #print("Detected license plate Number is:", text)
    img = cv2.resize(img, (500, 300))
    Cropped = cv2.resize(Cropped, (400, 200))
    cv2.imwrite("highlighted.png",img)
    cv2.imwrite("number_plate.png",Cropped)
    
    #highlight_img = ImageTk.PhotoImage(Image.open("highlighted.png"))
    #cropped_img = ImageTk.PhotoImage(Image.open("number_plate.png"))
    image = Image.open("number_plate.png")
    resized = image.resize((300, 100))
    myImage = ImageTk.PhotoImage(resized)
    mylbl_1 = Label(window,image=myImage)
    mylbl_1.pack()
    mylbl_1.place(x=500,y=200)

    image1 = Image.open("highlighted.png")
    resized1 = image1.resize((300,200))
    myImage1 = ImageTk.PhotoImage(resized1)
    mylbl_2 = Label(window,image=myImage1)
    mylbl_2.pack()
    mylbl_2.place(x=500,y=400)

    

mylbl = Label(window, text="Automatic Number-Plate Recognition Using Python", font=heading)
mylbl.pack()
select = Button(window, text="Select Image", bg="green", fg="white", width=15, font=myfont, command=select_image)
select.pack()
select.place(x=80, y=100)
sign_image.pack()
sign_image.place(x=70, y=200)

window.mainloop()
