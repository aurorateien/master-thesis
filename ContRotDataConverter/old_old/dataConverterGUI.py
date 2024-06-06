# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:00:27 2017

@author: jong1047
"""

import dataconverter
import six

if six.PY3 == True:
    import tkinter as tk
    from tkinter import ttk, N, W, E, S
    from tkinter.filedialog import askopenfilename

if six.PY2 == True:
    import Tkinter as tk
    import ttk
    from Tkinter import N, W, E, S
    from tkFileDialog import askopenfilename



"""
These are the default values, please change if you want to save time
"""

options = {}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
options["MRC"] = True
options["fMRC"] = True
options["IMG"] = True
options["quiet"] = False
options["smooth"] = True
options["fixDist"] = True #probably ok

options["path"] = "E:/TEMdata/Bi(TCPB)/170123/5/"

options["gear"] = 2
options["CRS"] = 0
options["startangle"] = -40
options["camerlength"] = 30
options["exptime"] = 0.25

options["wavelength"] = 0.0251
options["rotationaxis"] =  -139
options["strechamp"] = 1.3
options["strechazimuth"] = 180
options["direction"] = 1

options["factor"] = 1 #for cross. probably 2.5 if not already corrected else 1




def browsePath(path):
    try:
        newPath = askopenfilename(initialdir=path.get(), filetypes=[("Tiff file", "*.tiff")])
        
        path.set(removeFileFromPath(newPath))

    except ValueError:
        try:
            newPath = askopenfilename(filetypes=[("Tiff file", "*.tiff")])
        
            path.set(removeFileFromPath(newPath))
        except ValueError:
            pass



def removeFileFromPath(newPath):
    n = 0
    p = n
    for char in newPath:
        if char == "/":
            p = n
        n += 1
    
    return newPath[:p+1]

def run(options,path,gear,CRS,cameraLenght,MRC,fMRC,IMG,smooth,fixDist,quiet,startangle,direction,expttime,factor):   
    options["path"]        = path.get()+'/'
    options["gear"]        = gear.get()
    options["CRS"]         = CRS.get()
    options["camerlength"] = cameraLenght.get()
    options["MRC"]         = MRC.get()
    options["fMRC"]        = fMRC.get()
    options["IMG"]         = IMG.get()
    options["smooth"]      = smooth.get()
    options["fixDist"]     = fixDist.get()
    options["quiet"]       = quiet.get()
    options["startangle"]  = float(startangle.get())
    options["direction"]   = -1 + 2*direction.get()
    options["exptime"]     = float(expttime.get())
    options["factor"]      = float(factor.get())
    
    dataconverter.mainLoop(options)
    
    if options["quiet"] == False:
        print("#######################################")
        print("Successful run with parameters:")
        for option in options:
            print(option +"    " + str(options[option]))

def main(options):
    root = tk.Tk()
    root.title("DataConverter")
    
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    
    """
    browse file
    """
    path = tk.StringVar()
    path.set(options["path"])
    path_entry = ttk.Entry(mainframe, width=50, textvariable=path)
    path_entry.grid(column=1, row=1, sticky=W)
    ttk.Button(mainframe, text="Browse", command= lambda: browsePath(path)).grid(column=3, row=1, sticky=W)
    
    """
    exposure time
    """
    expttime = tk.StringVar()
    expttime.set(str(options["exptime"]))
    ttk.Label(mainframe, text="exposure time/s:").grid(column=1, row=2, sticky=W)
    expttime_entry = ttk.Entry(mainframe, width=5, textvariable=expttime)
    expttime_entry.grid(column=1, row=2)
    
    """
    select gear
    """
    gear = tk.IntVar()
    ttk.Label(mainframe, text="gear:").grid(column=1, row=2, sticky=E)
    ttk.OptionMenu(mainframe,gear,options["gear"],1,2,3).grid(column=2, row=2, sticky=W)
    
    """
    CRS
    """
    CRS = tk.IntVar()
    CRS.set(options["CRS"])
    ttk.Checkbutton(mainframe, text="CRS", variable=CRS).grid(column=3, row=2, sticky=W)
    
    """
    start angle
    """
    startangle = tk.StringVar()
    startangle.set(str(options["startangle"]))
    ttk.Label(mainframe, text="start angle").grid(column=1, row=3, sticky=W)
    expttime_entry = ttk.Entry(mainframe, width=5, textvariable=startangle)
    expttime_entry.grid(column=1, row=3)
    
    """
    camera length
    """
    cameraLenght = tk.IntVar()
    ttk.Label(mainframe, text="camera length:").grid(column=1, row=3, sticky=E)
    ttk.OptionMenu(mainframe,cameraLenght,options["camerlength"],15,25,20,30,40,50,60,80).grid(column=2, row=3, sticky=W)
    
    """
    direction
    """
    direction = tk.IntVar()
    direction.set(options["direction"])
    ttk.Checkbutton(mainframe, text="positive rotation", variable=direction).grid(column=3, row=3, sticky=W)
    
    """
    file export options
    """
    ttk.Label(mainframe, text="export as:").grid(column=1, row=4, sticky=W)
    
    MRC = tk.BooleanVar()
    MRC.set(options["MRC"])
    ttk.Checkbutton(mainframe, text=".mrc", variable=MRC).grid(column=1, row=5, sticky=W)
    
    fMRC = tk.BooleanVar()
    fMRC.set(options["fMRC"])
    ttk.Checkbutton(mainframe, text="fixed cross .mrc", variable=fMRC).grid(column=1, row=6, sticky=W)

    factor = tk.StringVar()
    factor.set(str(options["factor"]))
    ttk.Label(mainframe, text="cross correction factor:").grid(column=1, row=6, sticky = E)
    factor_entry = ttk.Entry(mainframe, width=6, textvariable=factor)
    factor_entry.grid(column=2, row=6, sticky = W)
   
    IMG = tk.BooleanVar()
    IMG.set(options["IMG"])
    ttk.Checkbutton(mainframe, text=".img", variable=IMG).grid(column=1, row=7, sticky = W)
    
    """
    .img export options
    """
    
    ttk.Label(mainframe, text=".img file options:").grid(column=1, row=8, sticky=W)
    
    smooth = tk.BooleanVar()
    smooth.set(options["smooth"])
    ttk.Checkbutton(mainframe, text="smooth direct beam positions (fit to 2nd ° polynomial)", variable=smooth).grid(column=1, row=9, sticky = W)
    
    fixDist = tk.BooleanVar()
    fixDist.set(options["fixDist"])
    ttk.Checkbutton(mainframe, text="correct elliptical distortion", variable=fixDist).grid(column=1, row=10, sticky = W)
    
    """
    fixDist = tk.BooleanVar()
    fixDist.set(options["fixDist"])
    ttk.Checkbutton(mainframe, text="correct elliptical distortion", variable=fixDist).grid(column=1, row=11, sticky = W)
    """
    """
    Quiet mode
    """    
    quiet = tk.BooleanVar()
    quiet.set(options["quiet"])
    ttk.Checkbutton(mainframe, text="quiet mode", variable=quiet).grid(column=2, row=12, sticky = W)
    
    """
    Run
    """
    ttk.Button(mainframe, text="Run", command= lambda: run(options,path,gear,CRS,cameraLenght,MRC,fMRC,IMG,smooth,fixDist,quiet,startangle,direction,expttime,factor)).grid(column=3, row=12, sticky=W)
    
    
    #ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
    """
    ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
    ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)
    ttk.Label(mainframe, text="meters").grid(column=3, row=5, sticky=W)
    ttk.Label(mainframe, text="meters").grid(column=3, row=5, sticky=W)
    """
    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
    
    path_entry.focus()
    root.bind('<Return>', browsePath)
    
    root.mainloop()
    
main(options)