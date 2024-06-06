from skimage.io import imread, imsave
import numpy as np
from images_corrections import *
import tifffile

def read_and_write_images(tiffFile, header, options, angle, rotSpeed,
                          realCameraLenght, directXY):
    """
    Opens one tiff file and writes the files specified in the options
    """
    if options["quiet"] == False:
        print("Reading " + tiffFile)
    image = imread(options["path"]+tiffFile).astype(np.int16)[::-1,:]
    if options["MRC"] == True:
        writeFileName = "mrc\\" + tiffFile[:-5] + ".mrc"
        if options["quiet"] == False:
            print("Writing " + writeFileName)
        with open(options["path"]+writeFileName, "wb") as f:
            f.write(header)
            f.write(image.tobytes())
    if options["fMRC"] == True:
        writeFileName = "fmrc\\" + tiffFile[:-5] + ".mrc"
        if options["quiet"] == False:
            print("Writing " + writeFileName)
        if options["inter_cross"]:
            newImage = fix_cross_interpol(image, options["factor"])
        else:
            newImage = fixCross(image, options["factor"])

        with open(options["path"]+writeFileName, "wb") as f:
            for n in range(0,256):
                byte = header[n*4:n*4+4]

                if n in [0,1,7,8]:
                    f.write(b'\x04\x02\x00\x00')
                else:
                    f.write(byte)
            f.write(newImage.astype(np.int16).tobytes())
    if options["IMG"] == True:
        writeFileName = "img\\" + tiffFile[:-5] + ".img"

        if options["quiet"] == False:
            print("Writing " + writeFileName)
        if options["smooth"] == False:
            above95 = np.where(image[::-1,:].T>np.max(image)*0.95)
            directXY = np.average(above95[0]),np.average(above95[1])
        if options["fixDist"] == True:
            image = fixDistortion(options,image,directXY)

        headerList = makeIMGHeader(options["wavelength"], directXY[0],
                                   directXY[1], rotSpeed, angle, angle,
                                   realCameraLenght)

        with open(options["path"]+writeFileName, "w") as f:
            for n in range(0,len(headerList)):
                f.write(headerList[n] + "\n")
            f.write("}")

        with open(options["path"]+writeFileName, "r+b") as f:
            for n in range(0,512):
                chunk = f.read(1)
                if chunk == b'':
                    f.write(b'\x00')
            f.write(image[::-1,:].tobytes())
    return image

def makeIMGHeader(wavelength, beamCenterX, beamCenterY, oscRange, oscStart, phi,
                  realCameraLenght):

    headerList = ["{",
                  "HEADER_BYTES=  512;",
                  "DIM=2;",
                  "BYTE_ORDER=little_endian;",
                  "TYPE=unsigned_short;",
                  "SIZE1=512;",
                  "SIZE2=512;",
                  "PIXEL_SIZE=0.050000;",
                  "BIN=1x1;",
                  "BIN_TYPE=HW;",
                  "ADC=fast;",
                  "CREV=1;",
                  "BEAMLINE=ALS831;",
                  "DETECTOR_SN=926;",
                  "DATE=Tue Jun 26 09:43:09 2007;",
                  "TIME=0.096288;",
                  "DISTANCE="      + str("%.2f" % realCameraLenght)  + ";",
                  "TWOTHETA=0.00;",
                  "PHI="           + str("%.2f" % phi)               + ";",
                  "OSC_START="     + str("%.2f" % oscStart)          + ";",
                  "OSC_RANGE="     + str("%.2f" % oscRange)          + ";",
                  "WAVELENGTH="    + str("%.6f" % wavelength)        + ";",
                  "BEAM_CENTER_X=" + str("%.2f" % beamCenterX)       + ";",
                  "BEAM_CENTER_Y=" + str("%.2f" % beamCenterY)       + ";",
                  "DENZO_X_BEAM="  + str("%.2f" % (beamCenterX*0.05))+ ";",
                  "DENZO_Y_BEAM="  + str("%.2f" % (beamCenterY*0.05))+ ";",
                  ]
    return headerList

def write_tiff_file(image, added_image, angnum, n_add_tiff, factor, path,
                    quiet):
    if ((angnum+1)%int(n_add_tiff)) != 0:
        added_image += fix_cross_interpol(image, factor).astype(int)
        return added_image
    else:
        added_image += fix_cross_interpol(image, factor).astype(int)
        n = angnum//n_add_tiff
        filename = str(1000000+n)[1:]+".tiff"
        full_path = path + "/tiff/" + filename
        if not quiet:
            print("Writing: " + filename)
        imsave(full_path, ((added_image+1)//(n_add_tiff)).astype(np.uint16)[::-1])
        return np.zeros(added_image.shape)

 
