from skimage.io import imread
import numpy as np

def calcRealCameralength(camerlength):
    lengthToLength = {15: 237.71,
                      20: 319.75,
                      25: 399.20,
                      30: 483.50,
                      40: 672.98,
                      50: 836.99,
                      60: 1006.08,
                      80: 1345.97}
    realCameraLenght = lengthToLength[camerlength]
    return realCameraLenght

def makeEd3d(completePath, options, onlyTiffFiles):
    with open(completePath, 'w') as f:
        speed =     ((0.114, 0.45),
                     (0.45, 1.8),
                     (1.126, 4.5))
        lengthopix = {15: 0.00838,
                      20: 0.00623,
                      25: 0.00499,
                      30: 0.00412,
                      40: 0.00296,
                      50: 0.00238,
                      60: 0.00198,
                      80: 0.00148}

        try:
            pixelsize = lengthopix[options["camerlength"]]
        except:
            print("Invalid camera length, 15 is used instead")
            pixelsize = lengthopix[15]

        topdata = [options["wavelength"],
                   options["rotationaxis"],
                   pixelsize,
                   options["strechamp"],
                   options["strechazimuth"]]

        topname = ['WAVELENGTH',
                   'ROTATIONAXIS',
                   'CCDPIXELSIZE',
                   'STRETCHINGAMP',
                   'STRETCHINGAZIMUTH']

        for name, data in zip(topname, topdata):
            f.write(name + '\t' + str(data) + '\n')
        f.write('\nFILELIST\n')
        #make filelists
        angnum = 0

        for tiffFile in onlyTiffFiles:
                f.write("FILE ")
                f.write(tiffFile[:-5] + ".mrc")
                angle = (options["startangle"] + options["direction"] * angnum *
                         speed[options["gear"]-1][options["CRS"]] *
                         options["exptime"])

                angle = " " + str("%.3f" % angle)
                f.write(angle+'\t0\t'+angle+'\n')
                angnum += 1
        
        f.write('ENDFILELIST')	            
        


def smoothDirectBeam(options,onlyTiffFiles):
    xys = []
    for tiffFile in onlyTiffFiles:
        if options["quiet"] == False:
            print("Finding direct beam in: "+tiffFile)
            
        image = imread(options["path"]+tiffFile).astype(np.int16)[::-1,:]
        above95 = np.where(image[::-1,:].T>np.max(image)*0.95)
        directXY = np.average(above95[0]),np.average(above95[1])
        xys.append(directXY)
        
    if options["quiet"] == False:
        print("Smoothing...")
        
    x = np.array(xys)[:,0]
    y = np.array(xys)[:,1]
    
    xs = np.linspace(0,x.shape[0]-1,x.shape[0])
    
    xPoly = np.polyfit(xs,x,2)
    yPoly = np.polyfit(xs,y,2)
    
    smoothX = xPoly[0]*xs**2+xPoly[1]*xs+xPoly[2]
    smoothY = yPoly[0]*xs**2+yPoly[1]*xs+yPoly[2]
    
    smoothXY = np.array([smoothX,smoothY])
    return smoothXY

def write_XDS_inp_file(last_file, start_angle, origin_x, origin_y,
                       dect_dist, os_angle, wavelength, path):
    with open("XDS_template.txt", "r") as file:
        template = file.read()
    format_dict = {"data_begin": 1,
                   "data_end": last_file,
                   "starting_angle": start_angle,
                   "dmin": 20.0,
                   "dmax": 0.80,
                   "origin_x": origin_x,
                   "origin_y": origin_y,
                   "sign": "+",
                   "detdist": dect_dist,
                   "osangle": os_angle,
                   "rot_x": 0.782608156852,
                   "rot_y": 0.622514636638,
                   "rot_z": 0.0,
                   "wavelength": wavelength}
    XDSinp = template.format(di=format_dict)
    with open(path+"/img/XDS.inp", "w") as file:
        file.write(XDSinp)

