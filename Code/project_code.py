import tkinter as tk
from tkinter.filedialog import *
from PIL import Image, ImageTk


openedImage=None
binaryImage=None
framedImage=None
nCol, nRow, orNRow, orNCol = 0,0,0,0
leviPixel2String= ""


#Creating Gui
userGui = tk.Tk()
xSize, ySize=675,1100
size=str(ySize)+"x"+str(xSize)
userGui.geometry(size)
userGui.title("To Binary Image")
userGui.configure(bg="deep sky blue")
#Creating Gui Grids
for r in range(3):
    for c in range(3):
        if r == 0:
            Label(userGui, bg="deep sky blue").grid(row=r, column=c, padx=(xSize / 6) - 15, pady=20)
        elif r==1:
            Label(userGui, bg="deep sky blue").grid(row=r, column=c, padx=0, pady=(ySize * 2 / 9))
        else:
            Label(userGui, bg="deep sky blue").grid(row=r, column=c, padx=0, pady=0)


#Opening an Image from system explorer
def openImage():
    try:
        openFileFormats = (("all files", "*.*"), ("png files", "*.png"))  # File formats for easy search
        path = askopenfilename(parent=userGui, filetypes=openFileFormats)  # Basic file pick gui
        fp = open(path, "rb")  # Read file as a byte map

        global openedImage
        openedImage = Image.open(fp).convert('1', dither=Image.NONE)  # Convert byte map to Image then grayscaling of the image
    except:
        reset()

    imageProcess()

#levialdi parallel shrink algorithm
def levialdi():
    global binaryImageTwo
    global ncc
    global iter
    ncc=0
    iter=0
    binaryImageOldOne=[[0 for i in range(len(binaryImage[0])+2)]for j in range(len(binaryImage)+2)]

    for i in range(0,len(binaryImage)):
       for j in range(0,len(binaryImage[0])):
           binaryImageOldOne[i+1][j+1]=binaryImage[i][j]



    binaryImageTwo=[[0 for i in range(len(binaryImageOldOne[0]))]for y in range(len(binaryImageOldOne))]
    for i in range(0,len(binaryImageOldOne)):
        for j in range(0,len(binaryImageOldOne[0])):
            binaryImageTwo[i][j]=binaryImageOldOne[i][j]

    flag=True
    while(flag):
        flag=False
        for i in range(len(binaryImageOldOne)-2,0,-1):
            for j in range(1,len(binaryImageOldOne[0])-1):
                if binaryImageOldOne[i][j]==1:
                    if binaryImageOldOne[i-1][j-1]==0 and binaryImageOldOne[i-1][j]==0 and binaryImageOldOne[i-1][j+1]==0 and binaryImageOldOne[i][j+1]==0 and binaryImageOldOne[i+1][j+1]==0 and binaryImageOldOne[i+1][j]==0 and binaryImageOldOne[i+1][j-1]==0 and binaryImageOldOne[i][j-1]==0:
                        binaryImageTwo[i][j]=0
                        ncc=ncc+1
                        flag=True
                    elif binaryImageOldOne[i][j-1]==0 and binaryImageOldOne[i+1][j-1]==0 and binaryImageOldOne[i+1][j]==0:
                        binaryImageTwo[i][j]=0
                        flag = True
                elif binaryImageOldOne[i][j]==0:
                    if binaryImageOldOne[i][j-1]==1 and binaryImageOldOne[i+1][j]==1:
                        binaryImageTwo[i][j]=1
                        flag = True

        iter=iter+1
        print("Number One:")
        for i in range(0,len(binaryImageOldOne)):
            for j in range(0,len(binaryImageOldOne[0])):
                print(binaryImageOldOne[i][j], end="")
            print("")

        for i in range(0,len(binaryImageOldOne)):
            for j in range(0,len(binaryImageOldOne[0])):
                binaryImageOldOne[i][j]=binaryImageTwo[i][j]

        print("")
        print("Number Two:")
        print("")
        for i in range(0,len(binaryImageOldOne)):
            for j in range(0,len(binaryImageOldOne[0])):
                print(binaryImageTwo[i][j], end="")
            print("")
        levialdi2Screen()
    print("ncc: ", ncc)
    print("iter: ", iter)

#Image process for input image to make it right form
def imageProcess():
    global openedImage
    nCol, nRow = openedImage.size
    print("-------------------------------------------")
    print("Image size : \nHorizontal : ",nCol,"\nVertical : ", nRow)
    print("-------------------------------------------")

    colorMap = openedImage.load() # Images to pixel map because of converting return average of RGB

    global framedImage

    framedImage = Image.new('RGB', ((nCol+2), (nRow+2)), color='black').convert('1', dither=Image.NONE)


    for r in range(1,nRow+1):
        for c in range(1,nCol+1):
            framedImage.putpixel((c,r), colorMap[c-1,r-1]) #Coloring framed image

    colorMap = framedImage.load() # Images to pixel map
    orNCol,orNRow=nCol,nRow

    nCol, nRow = framedImage.size
    print("-------------------------------------------")
    print("Framed Image size : \nHorizontal : ", nCol, "\nVertical : ", nRow)
    print("-------------------------------------------")

    global binaryImage
    binaryImage = [[0 for x in range(nCol)] for y in range(nRow)]  # Set pixelValue sizes

    global leviPixel2String


    for r in range(nRow):
        for c in range(nCol):
            if colorMap[c,r] > 200:
                binaryImage[r][c] = 1
            else:
                binaryImage[r][c] = 0




    # Printing image to Gui
    global img1
    defImg = ImageTk.PhotoImage(framedImage)
    img1.config(image=defImg)
    img1.image = defImg
    img1.update()


def reset():
    print("ERROR!")
#Printing binary Image to Gui
def binaryImage2Screen():
    global img2Binary
    global binaryPixel2String
    binaryPixel2String = ""
    fontSize4binary = 2

    img2Binary.select_clear()

    for i in range (0,len(binaryImage)):
        for j in range(0,len(binaryImage[0])):
            binaryPixel2String += str(binaryImage[i][j])
        binaryPixel2String += "\n"

    img2Binary.delete("lyTag")
    img2Binary.create_text(10, 10, text=binaryPixel2String, font=("Ariel", fontSize4binary, "bold"), tag="lvTag", anchor=NW)

    img2Binary.update()

#Printing live levialdi to screen
def levialdi2Screen():
    global binary2Levialdi
    global leviPixel2String
    leviPixel2String = ""
    fontSize4levialdi = 2

    binary2Levialdi.select_clear()

    for i in range(len(binaryImageTwo)):
        for j in range(len(binaryImageTwo[0])):
            leviPixel2String += str(binaryImageTwo[i][j])
        leviPixel2String+= "\n"

    #Fot see the every iteration
    binary2Levialdi.delete("lvTag")
    binary2Levialdi.create_text(10, 10, text=leviPixel2String, font=("Ariel", fontSize4levialdi, "bold"), tag="lvTag", anchor=NW)


    binary2Levialdi.update()

#To see the number of component on Gui
def numberOfComponents2Screen():
    global componentCanvas
    fontSize4Component= 35
    componentText="Number of Components: "+str(ncc)
    componentCanvas.select_clear()

    componentCanvas.create_text(5, 5, text=componentText, font=("Ariel", fontSize4Component, "bold"), tag="lvTag", anchor=NW)

    componentCanvas.update()

#To see the number iteraton on screen
def numberOfIterations2Screen():
    global iterationCanvas
    fontSize4Iteration = 35
    iterationText="Iterations: "+str(iter)
    iterationCanvas.select_clear()

    iterationCanvas.create_text(5, 5, text=iterationText, font=("Ariel", fontSize4Iteration, "bold"), tag="lvTag", anchor=NW)

    iterationCanvas.update()

#For levialdi function button
toLevialdiButton = Button(userGui, text='With Levialdi', borderwidth=1, command=levialdi, relief=RAISED, fg="red")
toLevialdiButton.grid(row=0, column=2, sticky=NW, padx=0, pady=20)
#Prints number of iteration
iterButton = Button(userGui, text="Number of Iteration", borderwidth=1, relief=RAISED, fg="green4", command=numberOfIterations2Screen)
iterButton.grid(row=0, column=2, sticky=NW, padx=200, pady=20)
#Prints number of components
nccButton = Button(userGui, text="Number of Components", borderwidth=1, relief=RAISED, fg="green4", command=numberOfComponents2Screen)
nccButton.grid(row=0, column=2, sticky=NE, padx=0, pady=20)
#It input image button
selectButton = Button(userGui, text='Open a File', borderwidth=1, command=openImage, relief=RAISED)
selectButton.grid(row=0, column=0, sticky=NW, padx=65, pady=20)
#Print binary image to Gui
binaryButton= Button(userGui, text="Binary Image", borderwidth=1, relief=RAISED, fg='blue', command=binaryImage2Screen)
binaryButton.grid(row=0, column=1, sticky=NE,padx=100,pady=20)
#Canvas for binary to screen
img2Binary= Canvas(userGui, borderwidth=2, bg="white", bd=3, relief="groove")
img2Binary.grid(row=1, column=1, sticky=W + E + N + S, padx=0)
#Canvas for live levialdi
binary2Levialdi = Canvas(userGui, borderwidth=2, bg="white", bd=3, relief="groove")
binary2Levialdi.grid(row=1, column=2, sticky=W + E + N + S)
#Canvas for number of components
componentCanvas = Canvas(userGui, borderwidth=2, bg="white", bd=3, relief="groove")
componentCanvas.grid(row=2, column=2, sticky=W + E + N + S)
#Canvas for number of iterations
iterationCanvas = Canvas(userGui, borderwidth=2, bg="white", bd=3, relief="groove")
iterationCanvas.grid(row=2, column=1, sticky=W + E + N + S)

img1 = Label(userGui, borderwidth=2, bg="white", bd=2, relief="groove")
img1.grid(row=1, column=0, sticky=W + E + N + S)

userGui.mainloop()
