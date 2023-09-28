
def crop_Image_To_Regular_Spec(original_Frame):
        #croping values 
        x = 742
        y = 263

        #ingredient Frame Height
        width = 511
        height = 513

        croppedImage = original_Frame[y:y + height, x:x + width]

        return croppedImage