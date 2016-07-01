from Tkinter import *
import ttk
#from PIL import Image, ImageTk
import os
import sys
import subprocess

#background image
global myvar


class Frames:

#Used to pass users selected species and region to the shell script

    speciesList = []
    cnum = 0
    rStart = 0
    rEnd = 0
    outputValues = [cnum, rStart, rEnd]
    counter = 0


    def __init__(self, master):

#Frames used in main window

        speciesSelection = Frame(master)
        specFrame = Frame(master)
        self.confPage = Frame(master)
        self.buildPage = Frame(master)
        self.frameList = [speciesSelection, specFrame, self.confPage, self.buildPage]
        self.frameCounter = 0


#Text labels and buttons for main menu

        self.fgLabel = Label(master, text = "VCFtoTree", font = ('Times', 30), fg = 'brown', bg = 'papaya whip')
        self.vLabel = Label(master, text = "V 1.0.0", font = ('Times', 15), fg = 'brown', bg = 'papaya whip')

        self.Begin = Button(master, text = "Begin", font = ('Times', 18), fg = 'brown', command = self.begin, borderwidth = 3, bg = 'papaya whip')
        #self.About = Button(master, text = "About", font = ('Times', 15), fg = 'brown')

        self.fgLabel.place(relx = .5, rely = .1, anchor = CENTER)
        self.vLabel.place(relx = .5, rely = .17, anchor = CENTER)

        self.Begin.place(relx = .57, rely = .6, anchor = E)
        #self.About.place(relx = .1, rely = .6, anchor = W)

#speciesSelection Frame

        Label(speciesSelection, text = "\n\n\nPlease select the species you \n would like to compare  \n", font = ('Times', 20), fg = 'brown').pack(side = TOP)

        self.DropDown = Listbox(speciesSelection, height = 5, width = 25, selectmode = MULTIPLE, font = ('Times', 15), activestyle = 'none')
        self.DropDown.pack(side = TOP)
        self.DropDown.yview()

        self.DropDown.insert(1, 'Human')
        self.DropDown.insert(2, 'Neandertal')
        self.DropDown.insert(3, 'Denisova')
        self.DropDown.insert(4, 'Chimp')
        self.DropDown.insert(5, 'Rhesus macaque')

        self.Next = Button(speciesSelection, text = "Next", font = ('Times', 12), fg = 'brown', command = self.oneSet, borderwidth = 4)


        self.Next.pack(side = RIGHT, pady = 45)


#specsFrame

        #Variables for ch no and region
        self.c = StringVar()
        self.rS = StringVar()
        self.rE = StringVar()


#Entry boxes for spec frame

        Label(specFrame, text = "\n Please select the chromosome and region \n to be analyzed: \n", font = ('Times', 20), fg = 'brown').pack(side = TOP)

        Label(specFrame, text = "\n Chromosome Number:", font = ('Times', 15), fg = 'brown').pack(side = TOP)
        self.c_num = Entry(specFrame, textvariable = self.c)
        self.c_num.pack(side = TOP)

        Label(specFrame, text = "\n Start of region:", font = ('Times', 15), fg = 'brown').pack(side = TOP)
        self.r_Start = Entry(specFrame, textvariable = self.rS)
        self.r_Start.pack(side = TOP)

        Label(specFrame, text = "\n End of region:", font = ('Times', 15), fg = 'brown').pack(side = TOP)
        self.r_End = Entry(specFrame, textvariable = self.rE)
        self.r_End.pack(side = TOP)

        self.Next = Button(specFrame, text = "Next", font = ('Times', 12), fg = 'brown', command = self.oneSet, borderwidth = 4)
        self.Previous = Button(specFrame, text = "Back", font = ('Times', 12), fg = 'brown', command = self.previousFrame, borderwidth = 4)

        self.Next.pack(side = RIGHT, pady = 45, padx = 100)
        self.Previous.pack(side = LEFT, pady = 45, padx = 100)

#Download Page

    #Stores selected species types and chromosome data for use in Shell script
    #Handles instances where no selection is made
    def storeInfo(self, counter):


        if self.frameCounter == 0:

            self.speciesList = [self.DropDown.get(selected) for selected in self.DropDown.curselection()]
            if len(self.speciesList) > 0:
                self.speciesList2 = ','.join(self.speciesList)


            else:
                self.DropDown.configure(bg = 'tomato')
                return

        elif self.frameCounter == 1:
            try:

                cnum = int(self.c.get())
                rStart = int(self.rS.get())
                rEnd = int(self.rE.get())

                self.outputValues[0] = (cnum)
                self.outputValues[1] = (rStart)
                self.outputValues[2] = (rEnd)

                #To produce only one set of widgets
                if(self.counter == 0):
                    #Conf Page Defined here to access updated output values
                    Label(self.confPage, text = "\n Building tree using chromosome %d \n on region %d to %d for species \n %s" % (self.outputValues[0], self.outputValues[1], self.outputValues[2], self.speciesList2), font = ('Times', 15), fg = 'brown').pack(side = TOP)
                    Label(self.confPage, text = "\n\n\n If this is correct, click confirm below.\n\n", font = ('Times', 12), fg = 'brown').pack(side = TOP)


#ERICA: this should return an error message to the screen if the user's selected region falls in the complex indel region

                #If parameters fall in complex indel region, output warning to GUI
                complex_indels = open('Code/complex_indelregions.txt', 'r')
                for indel in complex_indels:
                    indel = indel.strip()
                    if indel.startswith('#'):
                        continue
                    fields = indel.split('\t')
                    indel_chr = int(fields[0][3:])
                    indel_start = int(fields[1])
                    indel_end = int(fields[2])

                    #print cnum, str(indel_chr)
                    if not cnum == indel_chr:
                        continue
                    else:
                        #print cnum, str(indel_chr), indel_start, int(rStart)
                        if indel_start >= int(rStart) and indel_start <= int(rEnd):
                            print cnum, str(indel_chr), indel_start, int(rStart), int(rEnd)
                            warningLabel1 = Label(self.confPage, text = "\n WARNING: Your selected region contains complex indels, \n this may effect the tree.", font = ('Times', 12), fg = 'red')
                            warningLabel1.pack(side = TOP)
                        # TYPO, here should be >=, I guess I did this wrong from the beginning.
                        elif indel_end >= int(rStart) and indel_end <= int(rEnd):
                            print cnum, str(indel_chr), indel_end, int(rStart), int(rEnd)
                            warningLabel2 = Label(self.confPage, text = "\n WARNING: Your selected region contains complex indels, \n this may effect the tree.", font = ('Times', 12), fg = 'red')
                            warningLabel2.pack(side = TOP)

                if(self.counter == 0):

                    self.counter += 1

                    self.fix = Button(self.confPage, text = "Back", font = ('Times', 12), fg = 'brown', command = self.previousFrame, borderwidth = 4)
                    self.confirm = Button(self.confPage, text = "Confirm", font = ('Times', 12), fg = 'brown', command = self.confirmAll, borderwidth = 4)

                    self.fix.pack(side = LEFT, pady = 120, padx = 10)
                    self.confirm.pack(side = RIGHT, pady = 20, padx = 10)


            except:
                self.setRed(self.c, self.c_num)
                self.setRed(self.rS, self.r_Start)
                self.setRed(self.rE, self.r_End)
                return

        self.nextFrame()

    #Handles glitch where two sets of widgets are added to final frame
    def oneSet(self):
        self.storeInfo(self.counter)

    def confirmAll(self):

        self.nextFrame()
        Label(self.buildPage, text = '\n\n\nYour tree is being built. This may take a few moments. \n\n', font = ('Times', 15), fg = 'brown').pack(side = TOP)

        progressbar = ttk.Progressbar(self.buildPage, orient = HORIZONTAL, len=200, mode = 'determinate')
        progressbar.pack()
        progressbar.start()
        Label(self.buildPage, text = '\n', font = ('Times', 15), fg = 'brown').pack(side = TOP)

#ERICA: These addresses have to be changed to the ones that correspond to the mac
        #evo = Image.open('Code/evolution.jpg')

        # tkimage = ImageTk.PhotoImage(evo)
        # evoImage = Label(self.buildPage, image = tkimage)
        # evoImage.pack()

        os.system('chmod +x Code/buildTree_1click_erica.sh')
        # TYPO, add "self."
        os.system('Code/buildTree_1click_erica.sh %s %s %s %s &' % (self.outputValues[0], self.outputValues[1], self.outputValues[2], self.speciesList2))

    #Used to handle empty entry box instances
    #red if empty, reset to white if corrected
    def setRed(self, sVar, entryBox, ):
        try:
            int(sVar.get())
            if len(sVar.get()) == 0:
                entryBox.configure(bg = 'tomato')
            else:
                entryBox.configure(bg = 'white')
        except:
            entryBox.configure(bg = 'tomato')



 #Button Functions

    #Clears labels and buttons from Title Frame and initializes frameList
    def begin(self):

        self.fgLabel.place_forget()
        self.vLabel.place_forget()
        self.Begin.place_forget()
        #self.About.place_forget()
        #myvar.pack_forget()
        self.frameList[0].pack()

    #Sets next frame to main window
    def nextFrame(self):

        self.frameList[self.frameCounter].pack_forget()
        self.frameCounter = self.frameCounter + 1
        self.frameList[self.frameCounter].pack()
        return self.frameCounter

    #Sets previous frame to main window
    def previousFrame(self):

        self.frameList[self.frameCounter].pack_forget()
        self.frameCounter = self.frameCounter - 1
        self.frameList[self.frameCounter].pack()
        return self.frameCounter

#Class Definition End


#Makes sure code is operating inside of VCFtoTree_1.0.0 folder
#ERICA: I can't call os.system() on windows, so I'm not sure if this is going to work, but I just copied it from the last code we did on
global path
#TYPO
path = os.popen('find ~ -iname "VCFtoTree_1.0.0"').read()
print 'the path is ' + path
os.system('cd ' + path)
os.system('pwd')

#Main Window Setup
#ERICA: This address has to be changed to the one that corresponds to the mac, its the background image

root = Tk()

#root.wm_iconbitmap("C://Users/Yousef/Downloads/favicon (2).ico")
root.title("VCFtoTree")
#im = Image.open('Code/Dtree.jpg')
#tkimage = ImageTk.PhotoImage(im)
#myvar = Label(root, image = tkimage)
#myvar.pack()


root.minsize(width = 500, height = 500)
root.maxsize(width = 500, height = 500)

Frames = Frames(root)

#mainloop() keeps the application running, without which it dissappears
root.mainloop()
