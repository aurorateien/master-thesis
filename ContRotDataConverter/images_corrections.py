import numpy as np
from scipy import ndimage

def affine_transform_ellipse_to_circle(azimuth, stretch, inverse=False):
    """Usage: 
    r = circle_to_ellipse_affine_transform(azimuth, stretch):
    np.dot(x, r) # x.shape == (n, 2)
    
    http://math.stackexchange.com/q/619037
    """
    sin = np.sin(azimuth)
    cos = np.cos(azimuth)
    sx    = 1 - stretch
    sy    = 1 + stretch
    
    # apply in this order
    rot1 = np.array((cos, -sin,  sin, cos)).reshape(2,2)
    scale = np.array((sx, 0, 0, sy)).reshape(2,2)
    rot2 = np.array((cos,  sin, -sin, cos)).reshape(2,2)
    
    composite = rot1.dot(scale).dot(rot2)
    
    if inverse:
        return np.linalg.inv(composite)
    else:
        return composite

def affine_transform_circle_to_ellipse(azimuth, stretch):
    """Usage: 
    r = circle_to_ellipse_affine_transform(azimuth, stretch):
    np.dot(x, r) # x.shape == (n, 2)
    """
    return affine_transform_ellipse_to_circle(azimuth, stretch, inverse=True)

def apply_transform_to_image(img, transform, center=None):
    """Applies transformation matrix to image and recenters it
    http://docs.sunpy.org/en/stable/_modules/sunpy/image/transform.html
    http://stackoverflow.com/q/20161175
    """
    
    if center is None:
        center = (np.array(img.shape)[::-1]-1)/2.0
    
    displacement = np.dot(transform, center)
    shift = center - displacement
    
    img_tf = ndimage.interpolation.affine_transform(img, transform, offset=shift, mode="constant", order=3, cval=0.0)
    return img_tf

def fixCross(image, factor):
    """
    Adds missing pixels in cross
    """
    newImage = np.zeros([516,516],dtype=np.int16)
    newImage[0:256,0:256]   = image[0:256,0:256]
    newImage[256+4:,256+4:] = image[256:,256:]
    newImage[0:256,256+4:]  = image[0:256,256:]
    newImage[256+4:,0:256]  = image[256:,0:256]
        
    for n in range(0,2):
        newImage[255:258,:] = newImage[255,:]/factor
        newImage[258:261,:] = newImage[260,:]/factor
        newImage = newImage.T
    return newImage

def fixFixCross(newImage):
    """
    Removes added pixels in cross
    """
    fixFixImage = np.zeros([512,512],dtype=np.int16)
    fixFixImage[0:256,0:256] = newImage[0:256,0:256]
    fixFixImage[256:,256:]   = newImage[256+4:,256+4:]
    fixFixImage[0:256,256:]  = newImage[0:256,256+4:]
    fixFixImage[256:,0:256]  = newImage[256+4:,0:256]
    
    return fixFixImage

def fixDistortion(options,image,directXY):
    
    radianAzimuth = np.radians(options["strechazimuth"])
    stretch = options["strechamp"] * 0.01
                
    newImage = fixCross(image,options["factor"]) 
                
    center = np.copy(directXY)
    if directXY[0]>(255):
        center[0] += 1
    if directXY[0]>(256):
        center[0] += 2
    if directXY[0]>(257):
        center[0] += 1
            
    if directXY[1]>(255):
        center[1] += 1
    if directXY[1]>(256):
        center[1] += 2
    if directXY[1]>(257):
        center[1] += 1
    c2e = affine_transform_circle_to_ellipse(radianAzimuth, stretch)
    newImage = apply_transform_to_image(newImage[::-1,:], c2e, center)[::-1,:]
    fixFixImage = fixFixCross(newImage)
    
    return fixFixImage

def fix_cross_interpol(image, factor):
    half_x = image.shape[0]//2
    half_y = image.shape[1]//2
    factor = 1/factor
    center_factor = factor
    larger_image = make_larger_image(image, half_x, half_y)
    for n in range(4):
        larger_image = fix_one_quadrant(image, larger_image, factor)
        larger_image = larger_image[::-1]
        image = image[::-1]
        larger_image = fix_one_quadrant(image, larger_image, factor)
        image = image.T
        larger_image = larger_image.T
    for n in range(4):
        larger_image = fix_one_quadrant_center(image, larger_image, center_factor)
        larger_image = larger_image[::-1]
        image = image[::-1]
        larger_image = fix_one_quadrant_center(image, larger_image, center_factor)
        image = image.T
        larger_image = larger_image.T
    return larger_image

def make_larger_image(image, half_x, half_y):
    larger_image = np.zeros([image.shape[0]+4, image.shape[0]+4])
    larger_image[:half_x-1, :half_y-1] = image[:half_x-1, :half_y-1]
    larger_image[:half_x-1, half_y+5:] = image[:half_x-1, half_y+1:]
    larger_image[half_x+5:, :half_y-1] = image[half_x+1:, :half_y-1]
    larger_image[half_x+5:, half_y+5:] = image[half_x+1:, half_y+1:]
    return larger_image

def fix_one_quadrant(image, larger_image, factor):
    half_x = image.shape[0]//2
    half_y = image.shape[1]//2
    larger_image[half_x-1, :half_y-1] = (image[half_x-1, :half_y-1] * 0.75 * factor +
                                         image[half_x-2, :half_y-1] * 0.25)
    larger_image[half_x, :half_y-1] = image[half_x-1, :half_y-1] * factor
    larger_image[half_x+1, :half_y-1] = ((image[half_x-1, :half_y-1] * 0.75 +
                                          image[half_x, :half_y-1] * 0.25) * factor)
    return larger_image

def fix_one_quadrant_center(image, larger_image, center_factor):
    half_x = image.shape[0]//2
    half_y = image.shape[1]//2
    larger_image[half_x-1, half_y-1] = (image[half_x-1, half_y-1] * 0.5 * center_factor +
                                        larger_image[half_x-2, half_y-1] * 0.25 + 
                                        larger_image[half_x-1, half_y-2] * 0.25)
    larger_image[half_x, half_y-1] = (image[half_x-1, half_y-1] * 0.75 * center_factor + 
                                     larger_image[half_x, half_y-2] * 0.25)
    larger_image[half_x, half_y] = image[half_x-1, half_y-1] * center_factor
    larger_image[half_x-1, half_y+1] = (image[half_x-1, half_y-1] * center_factor * 0.5 + 
                                        image[half_x-1, half_y] * center_factor * 0.25 + 
                                        larger_image[half_x-2, half_y+1] * 0.25)
    larger_image[half_x, half_y+1] = (image[half_x-1, half_y-1] * center_factor * 0.75 + 
                                      image[half_x-1, half_y] * center_factor * 0.25)
    larger_image[half_x+1, half_y+1] = ((image[half_x-1, half_y-1] * 0.5 +
                                         image[half_x, half_y-1] * 0.25 + 
                                         image[half_x-1, half_y] * 0.25)*center_factor)
    return larger_image
    
