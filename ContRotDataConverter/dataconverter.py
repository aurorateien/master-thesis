# -*- coding: utf-8 -*-

from skimage.io import imread
from scipy import ndimage
import os
import numpy as np
from image_io import read_and_write_images, write_tiff_file
from misc_functions import *

def mainLoop(options):

    with open("header.bin", "rb") as file:
        header = file.read()

    onlyTiffFiles = []
    for fileOrFolder in os.listdir(options["path"]):
        if fileOrFolder[-5:]==".tiff":
            onlyTiffFiles.append(fileOrFolder)
    if options["MRC"] == True:
        if not os.path.exists(options["path"]+"mrc"):
            os.makedirs(options["path"]+"mrc")
        makeEd3d(options["path"] + "\\mrc\\" + "mrc.ed3d",
                 options,
                 onlyTiffFiles
                 )
    if options["fMRC"] == True:
        if not os.path.exists(options["path"]+"fmrc"):
            os.makedirs(options["path"]+"fmrc")
        makeEd3d(options["path"] + "\\fmrc\\" + "fmrc.ed3d",
                 options,
                 onlyTiffFiles
                 )
    if options["IMG"] == True:
        if not os.path.exists(options["path"]+"img"):
            os.makedirs(options["path"]+"img")
    if options["write_tiff"]:
        if not os.path.exists(options["path"]+"tiff"):
            os.makedirs(options["path"]+"tiff")

    speed = ((0.114,0.45),
             (0.45, 1.8),
             (1.126,4.5))
    realCameraLenght = calcRealCameralength(options["camerlength"])
    directXY = [256.0,256.0]
    if options["smooth"] == True:
        smoothXY = smoothDirectBeam(options, onlyTiffFiles)

    if options["write_tiff"]:
        added_image = np.zeros([512,512], dtype=int)

    for angnum, tiffFile in enumerate(onlyTiffFiles):
        angle = (options["startangle"] + options["direction"] * angnum *
                 speed[options["gear"]-1][options["CRS"]] * options["exptime"])
        rotSpeed = (speed[options["gear"]-1][options["CRS"]] *
                    options["exptime"] * options["direction"])
        if options["smooth"] == True:
            directXY = smoothXY[:,angnum]
        image = read_and_write_images(tiffFile,
                                      header,
                                      options,
                                      angle,
                                      rotSpeed,
                                      realCameraLenght,
                                      directXY)
        if options["write_tiff"]:
            added_image = write_tiff_file(image, added_image, angnum,
                                          options["n_add_tiff"],
                                          options["factor"],
                                          options["path"],
                                          options["quiet"])
    if options["IMG"]:
        os_angle = (options["direction"] *
                    speed[options["gear"]-1][options["CRS"]] *
                    options["exptime"])
        dect_dist = calcRealCameralength(options["camerlength"])

        write_XDS_inp_file(last_file=angnum, start_angle=options["startangle"],
                           origin_x=smoothXY[0][0], origin_y=smoothXY[0][1],
                           dect_dist=dect_dist, os_angle=os_angle,
                           wavelength=options["wavelength"],
                           path=options["path"])

