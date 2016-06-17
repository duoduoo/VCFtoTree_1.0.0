#Handles python 2 vs 3 module names
try:
    from tkinter import *
    import tkinter.font

except ImportError:
    from Tkinter import *
    import tkFont

import time
import sys
import os
import string
#os.system(environ[/FolderName])

#Stores selected species from DropDown
speciesList = []


#Tracks amount of times back is used
switchCount = 0

#Specs
specs = []

#Output values
outputValues = []
cnum = 0
rStart = 0
rEnd = 0

#Creates window, sets dimension, title, and icon
TreeBuilder = Tk()
TreeBuilder.title("Tree Builder")
TreeBuilder.geometry('400x400')
TreeBuilder.wm_iconbitmap("C://Users/Yousef/Downloads/favicon (2).ico")


#Main Menu Frame
mainFrame = Frame(TreeBuilder)
mainFrame.pack()

#Specs Frame
specFrame = Frame(TreeBuilder)

#Confirmation Page

#Font Incompatibility handler
try:
    Label(mainFrame, text = "\n Welcome To Tree Builder! \n", font = tkinter.font.Font(family = 'Times', size = 15, weight = 'bold')).pack(side = TOP)
except:
    Label(mainFrame, text = "\n Welcome To Tree Builder! \n", font = tkFont.Font(family = 'Times', size = 15, weight = 'bold')).pack(side = TOP)

Label(mainFrame, text = "Please select the species you would like to compare : \n").pack(side = TOP)

#ListBox for Main Menu
DropDown = Listbox(mainFrame, height = 6, selectmode = MULTIPLE)
DropDown.pack(side = TOP)
DropDown.yview()

DropDown.insert(1, 'Human')
DropDown.insert(2, 'Neandertal')
DropDown.insert(3, 'Denisova')
DropDown.insert(4, 'Chimp')
DropDown.insert(5, 'Rhesus macaque')

#Variables for ch no and region
c = StringVar()
rS = StringVar()
rE = StringVar()

#Entry boxes for spec frame
Label(specFrame, text = "\n Please select the chromosome and region to be analyzed: \n").pack(side = TOP)

Label(specFrame, text = "\n Chromosome Number:").pack(side = TOP)
c_num = Entry(specFrame, textvariable = c).pack(side = TOP)

Label(specFrame, text = "\n Start of region:").pack(side = TOP)
r_Start = Entry(specFrame, textvariable = rS).pack(side = TOP)

Label(specFrame, text = "\n End of region:").pack(side = TOP)
r_End = Entry(specFrame, textvariable = rE).pack(side = TOP)


#Removes spec frame, adds main menu frame
def goBack():
    specFrame.pack_forget()
    mainFrame.pack()

#Removes main menu, adds spec frame
def switchFrame():

    speciesList = [DropDown.get(selected) for selected in DropDown.curselection()]
    print(speciesList)
    #for species in speciesList:
    global speciesList2
    speciesList2 = ','.join(speciesList)
    print('Species in the species string are: ' + speciesList2)

    mainFrame.pack_forget()
    specFrame.pack()

    return speciesList2

def confPage():

    #Handles invalid input exception
    Invalid = Label(specFrame, text = "\n Invalid Input")


    try:

        cnum = int(c.get())
        rStart = int(rS.get())
        rEnd = int(rE.get())

        outputValues.append(cnum)
        outputValues.append(rStart)
        outputValues.append(rEnd)
        
        complex_indels = open('Code/complex_indelregions.txt','r')
        for indel in complex_indels:
            #print ' in for loop'
            indel=indel.strip()
            if indel.startswith('#'):
                continue
            fields = indel.split('\t')
            indel_chr = int(fields[0][3:])
            indel_start = int(fields[1])
            indel_end = int(fields[2])

            print cnum, str(indel_chr)
            if not cnum == indel_chr:
                continue
            else:
                #print 'its a match!'
                if indel_start >= int(rStart) and indel_start <= int(rEnd):
                    print 'indels start in input region'
                elif indel_end <= int(rStart) and indel_end <= int(rEnd):
                    print 'indels end site in input region'

        print(outputValues)
        specFrame.pack_forget()
        Label(TreeBuilder, text = "\n Building Tree using chromosome %d on region %d to %d " % (cnum, rStart, rEnd)).pack(side = TOP)


    except:

        #Invalid.pack(side = LEFT)
        outputValues.clear()

    print('Species selected are: ' + speciesList2)
    os.system('chmod +x /Users/Erica/Study/Gokcumen_Lab/GUI/Code/buildTree_1click_erica.sh')
    os.system('/Users/Erica/Study/Gokcumen_Lab/GUI/Code/buildTree_1click_erica.sh %s %s %s %s' % (outputValues[0], outputValues[1], outputValues[2], speciesList2))


#Main Frame Buttons
Button(mainFrame, text = 'Continue', command = switchFrame).pack(side = RIGHT or BOTTOM, padx = 5, pady = 30)
print(speciesList)
Button(mainFrame, text = 'Quit', command = TreeBuilder.quit).pack(side = RIGHT or BOTTOM, padx = 5, pady = 30)

print(speciesList)

#Spec Frame Buttons
Quit = Button(specFrame, text = 'Quit', command = TreeBuilder.quit).pack(side = RIGHT or BOTTOM, padx = 5, pady = 16)
Continue = Button(specFrame, text = 'Continue', command = confPage).pack(side = RIGHT or BOTTOM, padx = 5)
Back = Button(specFrame, text = 'Back', command = goBack).pack(side = RIGHT or BOTTOM, padx = 5)


#TODO
#Swapping Frames in Window
#Unpacking entire frames, including contents
#OS module, calling linux commands from python file
#Estimated Download Time
#Returning Paramters from GUI
#Getting GUI to interact with code
#Creating one setup folder including Tree Builder app,
#samtools, any additional modules if necessary, and README


#map filter and reduce
mainloop()
