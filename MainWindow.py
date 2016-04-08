import os.path
import Tkinter
import ImageTk
import Image
from Boeing747 import *
from DataViewer import *


# definition of special string characters (greek etc.)
degstr = u'\N{DEGREE SIGN}'
phistr = u'\u03C6'
lambdastr = u'\u03BB'

# global list with selected airport indices
airportindices = [-1, -1]

# main method which forms GUI and prints it on the screen
def open(airportstuple):
    mainTkWindow = Tkinter.Tk()
    mainTkWindow.title("Flight recorder simulator (" + u"\u00a9 Rafal Sikora)")
    mainTkWindow.resizable(width=Tkinter.FALSE, height=Tkinter.FALSE)
    # loading a background image
    filepath = "util/init.jpg"
    if os.path.isfile(filepath):
        img = ImageTk.PhotoImage(Image.open(filepath))
    else:
        print "Couldn't find a file " + filepath + "\nAborting execution"
        exit()
    # calculation of window size and position
    w = img.width()
    h = img.height()
    ws = mainTkWindow.winfo_screenwidth()
    hs = mainTkWindow.winfo_screenheight()
    x = (ws-w)/2
    y = (hs-h)/2
    # setting up
    mainTkWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
    can = Tkinter.Canvas(mainTkWindow, bg='black')
    can.pack(fill=Tkinter.BOTH, expand=1)
    can.create_image(0, 0, image=img, anchor="nw")

    frameleft = Tkinter.Frame(mainTkWindow)
    frameright = Tkinter.Frame(mainTkWindow)

    Tkinter.Label(frameleft, text="Start:").pack(side=Tkinter.TOP)
    Tkinter.Label(frameright, text="Destination:").pack(side=Tkinter.TOP)

    scrollbar = Tkinter.Scrollbar(frameleft, orient=Tkinter.VERTICAL)
    listbox = Tkinter.Listbox(frameleft, yscrollcommand=scrollbar.set, bg='black')
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
    listbox.pack()

    scrollbar2 = Tkinter.Scrollbar(frameright, orient=Tkinter.VERTICAL)
    listbox2 = Tkinter.Listbox(frameright, yscrollcommand=scrollbar2.set, bg='black')
    scrollbar2.config(command=listbox2.yview)
    scrollbar2.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
    listbox2.pack()

    labelstart = Tkinter.Label(mainTkWindow, text="", bg="black", fg="white")
    labelend = Tkinter.Label(mainTkWindow, text="", bg="black", fg="white")
    labelstart.place(x=w/4, y=h-h/6, anchor='center')
    labelend.place(x=3*w/4, y=h-h/6, anchor='center')

    listbox.bind('<<ListboxSelect>>', lambda action: currentlistselection(listbox, labelstart, airportstuple, 0))
    listbox2.bind('<<ListboxSelect>>', lambda action: currentlistselection(listbox2, labelend, airportstuple, 1))

    for item in airportstuple:
        listbox.insert(Tkinter.END, item[0]+" ("+item[1]+", "+item[2]+")")
        listbox2.insert(Tkinter.END, item[0]+" ("+item[1]+", "+item[2]+")")

    frameleft.place(x=w/4, y=2.5*h/4, anchor='center')
    frameright.place(x=3*w/4, y=2.5*h/4, anchor='center')

    flybutton = Tkinter.Button(mainTkWindow, text="Fly!", width="10", command=lambda: flyaction(listbox, listbox2, airportstuple))
    flybutton.place(x=w/2, y=h-h/10, anchor='center')

    quitbutton = Tkinter.Button(mainTkWindow, text="Quit", width="10", command=lambda: exit())
    quitbutton.place(x=w/2, y=h-h/25, anchor='center')

    # drawing the window on the screen
    mainTkWindow.mainloop()


# action method once some list element is chosen (printing a text)
def currentlistselection(listboxarg, label, airportstuple, listnum):
        index = listboxarg.index(listboxarg.curselection())
        value = airportstuple[index]
        airportindices[listnum] = index
        firstline = value[0]+" ("+value[1]+", "+value[2]+")"
        secondline = "Coordinates: " + phistr + "=" + str("%.2f" % float(value[3]))+degstr + " " +\
                     lambdastr + "=" + str("%.2f" % float(value[4]))+degstr
        thirdline = "Height (m.a.s.l): " + str("%.0f" % (float(value[5])*0.3048))
        label.config(text=firstline+"\n"+secondline+"\n"+thirdline)
        return index


# action method once a "Fly!" button is clicked (flight simulation)
def flyaction(listbox, listbox2, airportstuple):
    # first check if anything on the list has been chosen
    if (airportindices[0] > 0) and (airportindices[1] > 0):
        # check if start differs from destination
        if airportindices[0] != airportindices[1]:
            print "Starting flight simulation..."
            start = (float(airportstuple[airportindices[0]][3]), float(airportstuple[airportindices[0]][4]),
                     float(airportstuple[airportindices[0]][5]))
            destination = (float(airportstuple[airportindices[1]][3]), float(airportstuple[airportindices[1]][4]),
                     float(airportstuple[airportindices[1]][5]))
            airplane = Boeing747()  # type of the plane should be possible to choose in the future
            airplane.fly(start, destination)
            data = airplane.flightdata()
            print "...done!"
            viewer = DataViewer(data)
            viewer.start()
        else:
            print "Start and destination are identical!"
            return
    else:
        print "Must choose start and destination!"
        return
