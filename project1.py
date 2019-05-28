import tkinter as tk
from tkinter.filedialog import *
from PIL import Image, ImageTk
from copy import deepcopy
import csv

openedImage=None
binaryImage=None
imgarray = None
framedImage=None
nCol, nRow, orNRow, orNCol = 0,0,0,0
pixelMapAsString=""
stringpixel=""

root = tk.Tk()
xSize,ySize = 1920,1080
size = str(xSize)+"x"+str(ySize)
root.geometry(size)
root.title("Object Counting")
root.configure(bg='white')

for r in range(2):
    for c in range(2):
        if r == 0:
            Label(root, bg='white').grid(row=r, column=c, padx=(xSize/6)-15, pady=20)
        else:
            Label(root, bg='white', text="test").grid(row=r, column=c, padx=(xSize*2/9)-15, pady=(ySize*2/6))

def openImage():
    reset()
    label1 = Label(root)
    label1.place(relx=0.951, rely=0.1, height=21, width=20)
    label1.configure(background="#d9d9d9", text="")

    label3 = Label(root)
    label3.place(relx=0.97, rely=0.15, height=21, width=20)
    label3.configure(background="#d9d9d9", text="")
    try:
        openFileFormats = (("all files", "*.*"), ("png files", "*.png"))  # File formats for easy search
        path = askopenfilename(parent=root, filetypes=openFileFormats)  # Basic file pick gui
        global fp
        fp = open(path, "rb")  # Read file as a byte map


        global openedImage
        openedImage = Image.open(fp).convert('1', dither=Image.NONE)  # Convert byte map to Image then grayscaling of the image
    except:
        reset()

    imageProcess()


def imageProcess():
    global openedImage
    global nCol, nRow
    global colorMap
    nCol, nRow = openedImage.size
    print("-------------------------------------------")
    print("Image size : \nHorizontal : ",nCol,"\nVertical : ", nRow)
    print("-------------------------------------------")

    colorMap = openedImage.load()

    global framedImage
    framedImage = Image.new('RGB', ((nCol+2), (nRow+2)), color='black').convert('1', dither=Image.NONE)

    for r in range(1,nRow+1):
        for c in range(1,nCol+1):
            framedImage.putpixel((c,r), colorMap[c-1,r-1])

    colorMap = framedImage.load()
    orNCol,orNRow=nCol,nRow

    nCol, nRow = framedImage.size
    print("-------------------------------------------")
    print("Framed Image size : \nHorizontal : ", nCol, "\nVertical : ", nRow)
    print("-------------------------------------------")

    global binaryImage
    binaryImage = [[0 for x in range(nCol)] for y in range(nRow)]  # Set pixelValue sizes

    global pixelMapAsString

    for r in range(nRow):
        for c in range(nCol):
            if colorMap[c,r] > 200:
                binaryImage[r][c] = 1
            else:
                binaryImage[r][c] = 0
            pixelMapAsString +=  str(binaryImage[r][c])
        pixelMapAsString += "\n"

    print(pixelMapAsString)
    writeBinaryToScreen

    global img1
    defImg = ImageTk.PhotoImage(framedImage)
    img1.config(image=defImg)
    img1.image = defImg
    img1.update()

def tsfAlgorithm():
    #ÇOK UGRASTIM OLMADI
    reset()

def saveReport():
    global nccLev
    global fp
    global iterLev
    with open('report.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['File Name ',fp])
        writer.writerow(['File Size: ',str(nCol-2),'x',str(nRow-2)])
        writer.writerow(['NCC: ',str(nccLev)])
        writer.writerow(['Iteration LEV',str(iterLev)])




def reset():
    global levialdiCanvas
    global tsfCanvas
    levialdiCanvas.select_clear()
    levialdiCanvas.delete("lvTag")
    tsfCanvas.select_clear()
    tsfCanvas.delete("tsfTag")

    levialdiCanvas.update()
    tsfCanvas.update()

def levialdiAlgorithm():
    global binaryImage, imgarray
    global nRow,nCol
    global stringpixel
    global nccLev
    global iterLev
    nccLev = 0
    iterLev = 0
    imgarray = deepcopy(binaryImage)
    imgarray2 = deepcopy(binaryImage)

    print(nRow,nCol)
    print("-----------------------------------------------------------------------------------------111")
    for r in range(nRow):
        for c in range(nCol):
            print(binaryImage[r][c], end="")
        print("")

    check = True
    while check:
        check = False
        for i in range(1, nRow-1):
            for j in range(1,nCol-1):

                ul = imgarray[i-1][j-1]
                up = imgarray[i-1][j]
                ur = imgarray[i-1][j+1]
                ri = imgarray[i][j+1]
                le = imgarray[i][j-1]
                dr = imgarray[i+1][j+1]
                d = imgarray[i+1][j]
                dl = imgarray[i+1][j-1]

                if imgarray[i][j] == 1:
                    if le == 0 and dl == 0 and d == 0: #Deletion Condition
                        imgarray2[i][j] = 0
                        check = True

                        if ul == 0 and up == 0 and ur == 0 and ri == 0 and dr == 0: #Termination Condition
                            nccLev += 1
                else:
                    if le == 1 and d == 1: #Augmentation Condition
                        imgarray2[i][j] = 1
                        check = True

        if check:
            iterLev += 1
            imgarray = deepcopy(imgarray2)

        global levialdiCanvas
        levialdiCanvas.select_clear()
        levialdiCanvas.delete("lvTag")

        stringpixel=""
        for r in range(nRow):
            for c in range(nCol):
                stringpixel += str(imgarray[r][c])
                print(imgarray[r][c], end="")
            stringpixel += "\n"
            print("")


        levialdiCanvas.create_text(0, 0, text=stringpixel, font=("Ariel", 1 , "bold"), tag="lvTag", anchor=NW)
        levialdiCanvas.update()

    label1 = Label(root)
    label1.place(relx=0.951, rely=0.1, height=21, width=20)
    label1.configure(background="#d9d9d9", text=nccLev)

    label3 = Label(root)
    label3.place(relx=0.97, rely=0.15, height=21, width=20)
    label3.configure(background="#d9d9d9", text=iterLev)

    print("ncc : ", nccLev)
    print("iter : ", iterLev)

def createImage():
    reset()

def writeBinaryToScreen():

    global nccLev, iterLev
    global levialdiCanvas
    global pixelMapAsString
    fontSize = 20

    levialdiCanvas.create_text(0,0, text=pixelMapAsString, font=("Ariel", fontSize, "bold"), tag="lvTag", anchor=NW)
    levialdiCanvas.update()



tsfbutton = Button(root)
tsfbutton.place(relx=0.93, rely=0.50, height=24, width=59)
tsfbutton.configure(activebackground="#ececec", background="#d9d9d9",highlightbackground="#d9d9d9",text="TSF", width=65, command=tsfAlgorithm)

levbutton = Button(root)
levbutton.place(relx=0.93, rely=0.05, height=24, width=59)
levbutton.configure(activebackground="#ececec", background="#d9d9d9",highlightbackground="#d9d9d9",text="Levialdi", width=65, command=levialdiAlgorithm)

label1 = Label(root)
label1.place(relx=0.93, rely=0.1, height=21, width=55)
label1.configure(background="#d9d9d9", text="NCC:")

label2 = Label(root)
label2.place(relx=0.93, rely=0.55, height=21, width=55)
label2.configure(background="#d9d9d9", text="NCC:")

label3 = Label(root)
label3.place(relx=0.93, rely=0.15, height=21, width=90)
label3.configure(background="#d9d9d9", text="ITERATION:")

label4 = Label(root)
label4.place(relx=0.93, rely=0.60, height=21, width=90)
label4.configure(background="#d9d9d9", text="ITERATION:")

savebutton = Button(root)
savebutton.place(relx=0.05, rely=0.01, height=24, width=59)
savebutton.configure(activebackground="#ececec", background="#d9d9d9",highlightbackground="#d9d9d9",text="Save", width=65, command=saveReport)

selectbutton = Button(root)
selectbutton.place(relx=0.01, rely=0.01, height=24, width=59)
selectbutton.configure(activebackground="#ececec", background="#d9d9d9",highlightbackground="#d9d9d9",text="Select", width=65, command=openImage)

createbutton = Button(root)
createbutton.place(relx=0.09, rely=0.01, height=24, width=59)
createbutton.configure(activebackground="#ececec", background="#d9d9d9",highlightbackground="#d9d9d9",text="Create", width=65, command=createImage)

levialdiCanvas = Canvas(root, width=800, height=650, bg = '#afeeee')
levialdiCanvas.place(relx=0.480, rely=0.043, relheight=0.437, relwidth=0.445)
levialdiCanvas.configure(background="#d9d9d9",width=263)

tsfCanvas = tk.Canvas(root)
tsfCanvas.place(relx=0.480, rely=0.480, relheight=0.637, relwidth=0.445)
tsfCanvas.configure(background="#d9d9d9",width=263,insertbackground="black",relief='ridge',selectbackground="#c4c4c4",selectforeground="black")

img1 = Label(root, borderwidth=2, bg="white", fg="black", bd=3, relief="groove")
img1.grid(row=1, column=0, sticky=W + E + N + S)



root.mainloop()
