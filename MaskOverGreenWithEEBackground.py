#A advanced but simple function that takes a frame and runs it through the 
#De-greening algorythm and the image remasking for the EASY EATS background image
import cv2
import numpy as np
import skimage.exposure


def maskOverGreenWithBackground(frame, size):
    backgroundImage = cv2.imread(r"Resources/top-down-background_Upright.jpg", cv2.COLOR_RGBA2BGRA)
    #rescale to fit dimensions
    if size == "small":
        #ingredients, food images, 
        backgroundImage = cv2.resize(backgroundImage, (1920,1080))
    elif size == "steps":
        backgroundImage = cv2.resize(backgroundImage, (1080,1920))
    else:
        raise Exception("No valid rescale given")
    
    # convert frame to LAB
    lab = cv2.cvtColor(frame,cv2.COLOR_BGR2LAB)

    # extract A channel
    a = lab[:,:,1]

    # threshold A channel
    thresh = cv2.threshold(a, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # blur threshold image
    blur = cv2.GaussianBlur(thresh, (0,0), sigmaX=5, sigmaY=5, borderType = cv2.BORDER_DEFAULT)

    # stretch so that 255 -> 255 and 127.5 -> 0
    mask = skimage.exposure.rescale_intensity(blur, in_range=(127.5,255), out_range=(0,255)).astype(np.uint8)
    backgroundResult = cv2.bitwise_and(frame, frame, mask=mask)


    inverse_mask = cv2.bitwise_not(mask)

    preserved_frame = cv2.bitwise_and(backgroundImage, backgroundImage, mask=inverse_mask)
    #adds thhe background result with the mask with the preserved frame, now with the inverse mask
    backgroundResult = cv2.add(backgroundResult,preserved_frame)
    
    return backgroundResult


